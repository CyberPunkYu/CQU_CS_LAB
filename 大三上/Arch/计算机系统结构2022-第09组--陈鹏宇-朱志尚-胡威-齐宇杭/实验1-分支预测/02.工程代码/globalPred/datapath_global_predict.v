`timescale 1ns / 1ps

module datapath_global_pred(
    input clk, rst,
    input [31:0]instrD, readdata, 
    input regwriteE, regwriteM, regwriteW,
    input memtoregW, memtoregE, memtoregM,
    input alusrcE, regdstE,
    input jumpD, branchD,
    input [2:0] alucontrolE,
    output wire [31:0]pc, aluoutM, mem_WriteData, resultW,
    output stallF, stallD,
	output flushD, flushE, flushM
);

// pc_branched: ��·ѡ���֧֮���pc; 
wire [31:0] pc_branched; 
wire [31:0] pc_realnext;

//ALU������ԴA��B
wire  [31:0]ALUsrcA; 
wire  [31:0]ALUsrcB1; 
wire  [31:0]ALUsrcB2, sl2_imm, sl2_Jaddr, jump_addr; 

// Fetch 
wire [31:0] pcF, pcPlus4F;

// Decode 
wire [31:0] pcD, pcPlus4D, pcBranchD, rd1D, rd2D, signImmD;
wire [ 4:0] rsD, rtD, rdD;

// Execute 
wire [31:0] pcE, pcPlus4E, pcBranchE, rd1E, rd2E, signImmE, aluoutE, writedataE;
wire [ 4:0] rsE, rtE, rdE, writeregE; // д��Ĵ�����
wire branchE, zeroE, actual_takeE;

// Mem  
wire [31:0] pcM, pcPlus4M, pcBranchM, writedataM;
wire [ 4:0] writeregM;
wire branchM, zeroM, actual_takeM;
 
// WB  
wire [31:0] aluoutW, readdataW;
wire [ 4:0] writeregW;

// hazard
wire [1:0] forwardAE; 
wire [1:0] forwardBE;

// branch prediction
wire pred_takeD, pred_takeE, pred_takeM, pred_resM;//Ԥ��

// -------------------Fetch------------------------

//pc
flopenr #(32) pc_module(clk, rst, ~stallF, pc_realnext, pc);
assign pcF = pc; 
// branch pc
assign pc_branched = {pred_resM, pred_takeM} == 2'b10 ? pcBranchM : //���Ԥ�ⲻ��ת��Ԥ�����Ŀ���ַΪpc+4+sl2_imm
					 {pred_resM, pred_takeD} == 2'b01 ? pcBranchD : //���Ԥ����ת��ȷ�������Ŀ���ַ
					 {pred_resM, pred_takeD} == 2'b00 ? pcPlus4F :	//���Ԥ�ⲻ��ת��ȷ�������pc+4
                     pcPlus4M;                                      //���Ԥ����ת��Ԥ����������pc+4

//mux, ѡ���֧֮���pc��jump_addr
mux2 #(32) pcnext(jump_addr, pc_branched, jumpD, pc_realnext);

//PC+4
adder pc4_adder (pcF, 32'h4, pcPlus4F);

// --------------------fetech--------------------

// pcF-D
flopenrc #(32) Fpc (clk, rst, ~stallD, flushD, pcF, pcD);

// pc4F-D
flopenrc #(32) Fpc4 (clk, rst, ~stallD, flushD, pcPlus4F, pcPlus4D);

//--------------------Decode----------------------- 

//jumpָ��
sl2 sl2_2({6'b0, instrD[25:0]}, sl2_Jaddr);

assign jump_addr = {pcPlus4D[31:28], sl2_Jaddr[27:0]};
assign rsD = instrD[25:21];
assign rtD = instrD[20:16];
assign rdD = instrD[15:11];

//�Ĵ�����
regfile regfile(~clk, rst, regwriteW, instrD[25:21], instrD[20:16], writeregW, resultW, rd1D, rd2D);
//������չ
signext sign_extend(instrD[15:0], signImmD);
//������������
sl2 sl21mm(signImmD, sl2_imm);
//pcBranchD
adder pcbranch_adder (sl2_imm, pcPlus4D, pcBranchD);


// -------------------decode-execution---------------------

// rd1
floprc #(32) DE_rd1 (clk, rst, flushE, rd1D, rd1E);
// rd2
floprc #(32) DE_rd2 (clk, rst, flushE, rd2D, rd2E);
// rs, rt, rd
floprc #(15) DE_rt_rd (clk, rst, flushE, {rsD, rtD, rdD}, {rsE, rtE, rdE});
// extend_imm
floprc #(32) DE_imm (clk, rst, flushE, signImmD, signImmE);
// branch
floprc #(1) DE_branch (clk, rst, flushE, branchD, branchE);
// pc
floprc #(32) DE_pc (clk, rst, flushE, pcD, pcE);
// pcbranch
floprc #(32) DE_pcbranch (clk, rst, flushE, pcBranchD, pcBranchE);
// pc4
floprc #(32) DE_pc4 (clk, rst, flushE, pcPlus4D, pcPlus4E);
// pred
floprc #(1) DE_predTake (clk, rst, flushE, pred_takeD, pred_takeE);


// ----------------Execution------------------------

// ALU
mux3 #(32) mux_ALUAsrc(rd1E, resultW, aluoutM, forwardAE, ALUsrcA);
mux3 #(32) mux_ALUBsrc1(rd2E, resultW, aluoutM, forwardBE, ALUsrcB1);
mux2 #(32) mux_ALUBsrc2(signImmE, ALUsrcB1, alusrcE, ALUsrcB2);
alu alu(ALUsrcA, ALUsrcB2, alucontrolE, aluoutE, zeroE);

//�õ�ʵ���Ƿ���ת
assign actual_takeE = branchE && zeroE;
assign writedataE = ALUsrcB1; 
// �Ĵ�����д���ַ writereg
mux2 #(5) mux_WA3(rdE, rtE, regdstE, writeregE);
// ----------------execution-Mem----------------

// aluout
flopenrc #(32) EM_aluout (clk, rst, 1'b1, flushM, aluoutE, aluoutM);
// writedata
flopenrc #(32) EM_writedata (clk, rst, 1'b1, flushM, writedataE, writedataM);
// writereg
flopenrc #(5) EM_writereg (clk, rst, 1'b1, flushM, writeregE, writeregM);
// pc
flopenrc #(32) EM_pc (clk, rst, 1'b1, flushM, pcE, pcM);
// branch
flopenrc #(1) EM_branch (clk, rst, 1'b1, flushM, branchE, branchM);
// zero
flopenrc #(1) EM_zero (clk, rst, 1'b1, flushM, zeroE, zeroM);
// pcbranch
flopenrc #(32) EM_pcbranch (clk, rst, 1'b1, flushM, pcBranchE, pcBranchM);
// pc4
flopenrc #(32) EM_pc4 (clk, rst, 1'b1, flushM, pcPlus4E, pcPlus4M);
// pred_take
flopenrc #(1) EM_pred_take (clk, rst, 1'b1, flushM, pred_takeE, pred_takeM);


// Mem 
assign actual_takeM = branchM && zeroM;
assign mem_WriteData = writedataM;

//--------------------Mem-wb-----------------------

// aluout
flopenr #(32) MF_aluout (clk, rst, 1'b1, aluoutM, aluoutW);
// readdata from data memory
flopenr #(32) MF_readdata (clk, rst, 1'b1, readdata, readdataW);
// writereg
flopenr #(5) MW_writereg (clk, rst, 1'b1, writeregM, writeregW);


// -------------------Write Back----------------------- 
//mux
mux2 #(32) mux_WDin(readdataW, aluoutW, memtoregW, resultW);

// --------------------hazard--------------------


hazard hazard(rsD, rtD, rsE, rtE, writeregE, writeregM, writeregW,
              regwriteE, regwriteM, regwriteM, memtoregE, memtoregM,
              pred_takeD, pred_resM, forwardAE, forwardBE, 
              stallF, stallD, flushD, flushE, flushM);

// ---------------pre-----------------

branch_predict_global bpl(clk, rst, flushD, stallD, flushE, pcF, pcE, pcM, branchD,
                         branchE, branchM, actual_takeE, actual_takeM, pred_takeD, pred_resM);

endmodule



