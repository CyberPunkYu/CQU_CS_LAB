`timescale 1ns / 1ps
module branch_predict_local (
    input wire clk, 
	input wire rst,
    input wire flushD, 
	input wire stallD, 
	input wire flushE, //为了处理预测错误加上
    input wire [31:0] pcF, 
	input wire [31:0] pcE, //在EX阶段需要判断是否预测错误
	input wire [31:0] pcM,
    input wire branchD, // ID阶段是否是跳转指令(因为controller会判断branchD，这里改为input)
	input wire branchE, // 执行阶段是否是跳转指令 
	input wire branchM,// M阶段是否是分支指令
    input wire actual_takeE, 
	input wire actual_takeM,// 实际是否跳转
    output wire pred_takeD,// 预测是否跳转
    output wire pred_resM // 预测是否冲刷
);

wire pred_takeF;
reg pred_takeFr;
// 定义参数
parameter Strongly_not_taken = 2'b00,Weakly_not_taken = 2'b01, Weakly_taken = 2'b11, Strongly_taken = 2'b10;
// 定义表深度
parameter PHT_DEPTH = 6; 
parameter BHT_DEPTH = 10; 

// BHR长6位
reg [5:0] BHT [(1<<BHT_DEPTH)-1 : 0];
reg [1:0] PHT [(1<<PHT_DEPTH)-1 : 0];

integer i,j;
wire [(PHT_DEPTH-1):0] PHT_index;
wire [(BHT_DEPTH-1):0] BHT_index;
wire [(PHT_DEPTH-1):0] BHR_v;

// ---------------------------------------预测逻辑---------------------------------------

assign BHT_index = pcF[11:2]; //BHT表的索引是pc的11-2共十位
assign BHR_v = BHT[BHT_index]; //BHR的值共6位将作为PHT表的索引
assign PHT_index = BHR_v ^ pcF[7:2]; //PHT表的索引就是BHR的值和pc的按位异或，是对pc进行哈希
assign pred_takeF = PHT[PHT_index][1];//根据二位饱和计数器的性质，可根据第二位判断taken or not taken

// --------------------------pipeline------------------------------
always @(posedge clk) begin
    if(rst | flushD) begin
        pred_takeFr <= 0;
    end
    else if(~stallD) begin
        pred_takeFr <= pred_takeF;
    end
	else
		pred_takeFr <= pred_takeFr;
    end

// --------------------------pipeline------------------------------

// ---------------------------------------预测逻辑---------------------------------------

// ---------------------------------------BHT初始化以及更新---------------------------------------
wire [(PHT_DEPTH-1):0] update_PHT_index;
wire [(BHT_DEPTH-1):0] update_BHT_index;
wire [(PHT_DEPTH-1):0] update_BHR_v;

assign update_BHT_index = pcM[11:2];
assign update_BHR_v = BHT[update_BHT_index];  
assign update_PHT_index = update_BHR_v ^ pcM[7:2];

always@(posedge clk) begin
    if(rst) begin
    //初始化为0
        for(j = 0; j < (1<<BHT_DEPTH); j=j+1) begin
            BHT[j] <= 0;
        end
    end
    else if(branchM) begin
        // 移位赋值,BHR循环左移
        BHT[update_BHT_index] <= {BHT[update_BHT_index][4:0], actual_takeM};
    end
    else
		BHT[update_BHT_index] <= BHT[update_BHT_index];
end

// ---------------------------------------BHT初始化以及更新---------------------------------------


// ---------------------------------------PHT初始化以及更新---------------------------------------
    always @(posedge clk) begin
        if(rst) begin
        //初始化为weakly taken
            for(i = 0; i < (1<<PHT_DEPTH); i=i+1) begin
                PHT[i] <= Weakly_taken;
            end
        end
        else begin
            case(PHT[update_PHT_index])
                // 状态机更新PHT
                Strongly_not_taken: PHT[update_PHT_index] <= (actual_takeM)? Weakly_not_taken: Strongly_not_taken;
                Weakly_not_taken: PHT[update_PHT_index] <= (actual_takeM)? Weakly_taken: Strongly_not_taken;
                Weakly_taken: PHT[update_PHT_index] <= (actual_takeM)? Strongly_taken: Weakly_not_taken;
                Strongly_taken: PHT[update_PHT_index] <= (actual_takeM)? Strongly_taken: Weakly_taken;
            endcase 
        end
    end
// ---------------------------------------PHT初始化以及更新---------------------------------------

    // 译码阶段输出最终的预测结果
    assign pred_takeD = branchD & pred_takeFr;  

// ---------------------------------------预测错误处理阶段---------------------------------------
    
    reg pred_resE;
    always @(posedge clk ) begin
        //如果这条指令本身被冲刷了
        if(rst | flushE)
            pred_resE <= 1'b0;
        //执行阶段是branch，且预测错误
        else if (branchE && PHT[BHT[pcE[11:2]] ^ pcE[7:2]][1] != actual_takeE)
            pred_resE <= 1'b1;
        //default
        else
            pred_resE <= 1'b0;
    end
    // MEM阶段输出是否冲刷
    assign pred_resM = pred_resE;

endmodule
