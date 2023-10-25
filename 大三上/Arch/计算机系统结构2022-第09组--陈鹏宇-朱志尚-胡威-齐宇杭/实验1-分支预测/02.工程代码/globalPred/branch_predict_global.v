`timescale 1ns / 1ps
module branch_predict_global(
    input wire clk, 
	input wire rst,
    input wire flushD, 
	input wire stallD, 
	input wire flushE, 
    input wire [31:0] pcF, 
	input wire [31:0] pcE, 
	input wire [31:0] pcM,
    input wire branchD, 
	input wire branchE, 
	input wire branchM,
    input wire actual_takeE, 
	input wire actual_takeM,
    output wire pred_takeD,
    output wire pred_resM
);

wire pred_takeF;

parameter Strongly_not_taken = 2'b00, Weakly_not_taken = 2'b01, Weakly_taken = 2'b11, Strongly_taken = 2'b10;
parameter GHR_LENGTH = 8;

reg [GHR_LENGTH-1:0] GHR_v;
reg [GHR_LENGTH-1:0] GHR_v_retire; 
reg [1:0] PHT [(1<<GHR_LENGTH)-1 : 0]; 
wire [(GHR_LENGTH-1):0] PHT_index;

assign PHT_index = GHR_v ^ pcF[9:2];  //查询PHT的索引是GHR
assign pred_takeF = PHT[PHT_index][1]; 

reg pred_takeFr;
always @(posedge clk) begin
    if(rst | flushD) pred_takeFr <= 0;
    else if(~stallD) pred_takeFr <= pred_takeF;
	else             pred_takeFr <= pred_takeFr;
end

reg pred_resE;
always @(posedge clk) 
    begin
        if(rst | flushE) pred_resE <= 1'b0;
        else if (branchE && PHT[GHR_v_retire ^ pcE[9:2]][1] != actual_takeE) pred_resE <= 1'b1;
        else pred_resE <= 1'b0;
    end

//GHT的初始化和更新
always @(posedge clk) 
    begin
        //GHT初始化为0
        if (rst) begin
            GHR_v <= 0;
            GHR_v_retire <= 0;
        end else if (~stallD && branchD) begin
        //在预测阶段，先将预测的值更新入GHT表中
            GHR_v <= {GHR_v[GHR_LENGTH-2:0], pred_takeF};
            GHR_v_retire <= GHR_v;
        end
    end
//在访存阶段，将真实的跳转替换到GHT_retire中，再对GHT进行更新
always@(posedge clk)
    begin
        if(branchM) begin
            GHR_v_retire[0] <= actual_takeM; 
            GHR_v <= GHR_v_retire;
        end
    end

//更新PHT时，用的是GHR_retire
assign pred_resM = pred_resE;
wire [(GHR_LENGTH-1):0] update_PHT_index;
assign update_PHT_index = GHR_v_retire ^ pcM[9:2];

integer i;
always @(posedge clk) begin
    if(rst) begin
        for(i = 0; i < (1<<GHR_LENGTH); i=i+1) begin
            PHT[i] <= Weakly_taken;
        end
    end
    else if (branchM) begin
        case(PHT[update_PHT_index])
                Strongly_not_taken: PHT[update_PHT_index] <= (actual_takeM)? Weakly_not_taken:Strongly_not_taken;
                Weakly_not_taken: PHT[update_PHT_index] <= (actual_takeM)? Weakly_taken:Strongly_not_taken;
                Weakly_taken: PHT[update_PHT_index] <= (actual_takeM)? Strongly_taken:Weakly_not_taken;
                Strongly_taken: PHT[update_PHT_index] <= (actual_takeM)? Strongly_taken:Weakly_taken;
        endcase 
    end
end
assign pred_takeD = branchD & pred_takeFr;  
endmodule