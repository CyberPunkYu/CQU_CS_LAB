`timescale 1ns / 1ps
module branch_predict_local (
    input wire clk, 
	input wire rst,
    input wire flushD, 
	input wire stallD, 
	input wire flushE, //Ϊ�˴���Ԥ��������
    input wire [31:0] pcF, 
	input wire [31:0] pcE, //��EX�׶���Ҫ�ж��Ƿ�Ԥ�����
	input wire [31:0] pcM,
    input wire branchD, // ID�׶��Ƿ�����תָ��(��Ϊcontroller���ж�branchD�������Ϊinput)
	input wire branchE, // ִ�н׶��Ƿ�����תָ�� 
	input wire branchM,// M�׶��Ƿ��Ƿ�ָ֧��
    input wire actual_takeE, 
	input wire actual_takeM,// ʵ���Ƿ���ת
    output wire pred_takeD,// Ԥ���Ƿ���ת
    output wire pred_resM // Ԥ���Ƿ��ˢ
);

wire pred_takeF;
reg pred_takeFr;
// �������
parameter Strongly_not_taken = 2'b00,Weakly_not_taken = 2'b01, Weakly_taken = 2'b11, Strongly_taken = 2'b10;
// ��������
parameter PHT_DEPTH = 6; 
parameter BHT_DEPTH = 10; 

// BHR��6λ
reg [5:0] BHT [(1<<BHT_DEPTH)-1 : 0];
reg [1:0] PHT [(1<<PHT_DEPTH)-1 : 0];

integer i,j;
wire [(PHT_DEPTH-1):0] PHT_index;
wire [(BHT_DEPTH-1):0] BHT_index;
wire [(PHT_DEPTH-1):0] BHR_v;

// ---------------------------------------Ԥ���߼�---------------------------------------

assign BHT_index = pcF[11:2]; //BHT���������pc��11-2��ʮλ
assign BHR_v = BHT[BHT_index]; //BHR��ֵ��6λ����ΪPHT�������
assign PHT_index = BHR_v ^ pcF[7:2]; //PHT�����������BHR��ֵ��pc�İ�λ����Ƕ�pc���й�ϣ
assign pred_takeF = PHT[PHT_index][1];//���ݶ�λ���ͼ����������ʣ��ɸ��ݵڶ�λ�ж�taken or not taken

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

// ---------------------------------------Ԥ���߼�---------------------------------------

// ---------------------------------------BHT��ʼ���Լ�����---------------------------------------
wire [(PHT_DEPTH-1):0] update_PHT_index;
wire [(BHT_DEPTH-1):0] update_BHT_index;
wire [(PHT_DEPTH-1):0] update_BHR_v;

assign update_BHT_index = pcM[11:2];
assign update_BHR_v = BHT[update_BHT_index];  
assign update_PHT_index = update_BHR_v ^ pcM[7:2];

always@(posedge clk) begin
    if(rst) begin
    //��ʼ��Ϊ0
        for(j = 0; j < (1<<BHT_DEPTH); j=j+1) begin
            BHT[j] <= 0;
        end
    end
    else if(branchM) begin
        // ��λ��ֵ,BHRѭ������
        BHT[update_BHT_index] <= {BHT[update_BHT_index][4:0], actual_takeM};
    end
    else
		BHT[update_BHT_index] <= BHT[update_BHT_index];
end

// ---------------------------------------BHT��ʼ���Լ�����---------------------------------------


// ---------------------------------------PHT��ʼ���Լ�����---------------------------------------
    always @(posedge clk) begin
        if(rst) begin
        //��ʼ��Ϊweakly taken
            for(i = 0; i < (1<<PHT_DEPTH); i=i+1) begin
                PHT[i] <= Weakly_taken;
            end
        end
        else begin
            case(PHT[update_PHT_index])
                // ״̬������PHT
                Strongly_not_taken: PHT[update_PHT_index] <= (actual_takeM)? Weakly_not_taken: Strongly_not_taken;
                Weakly_not_taken: PHT[update_PHT_index] <= (actual_takeM)? Weakly_taken: Strongly_not_taken;
                Weakly_taken: PHT[update_PHT_index] <= (actual_takeM)? Strongly_taken: Weakly_not_taken;
                Strongly_taken: PHT[update_PHT_index] <= (actual_takeM)? Strongly_taken: Weakly_taken;
            endcase 
        end
    end
// ---------------------------------------PHT��ʼ���Լ�����---------------------------------------

    // ����׶�������յ�Ԥ����
    assign pred_takeD = branchD & pred_takeFr;  

// ---------------------------------------Ԥ�������׶�---------------------------------------
    
    reg pred_resE;
    always @(posedge clk ) begin
        //�������ָ�����ˢ��
        if(rst | flushE)
            pred_resE <= 1'b0;
        //ִ�н׶���branch����Ԥ�����
        else if (branchE && PHT[BHT[pcE[11:2]] ^ pcE[7:2]][1] != actual_takeE)
            pred_resE <= 1'b1;
        //default
        else
            pred_resE <= 1'b0;
    end
    // MEM�׶�����Ƿ��ˢ
    assign pred_resM = pred_resE;

endmodule
