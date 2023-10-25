`timescale 1ns / 1ps

module mips_global_pred(
	input wire clk,
	input wire rst,
	input wire[31:0] instr,
	input wire[31:0] readdata,
	output wire memwriteM,
	output wire[31:0] pc, 
	output wire[31:0] resultW,
	output wire[31:0] aluoutM, 
	output wire[31:0] writedata,
	output [4:0] rs, 
	output [4:0] rt, 
	output [4:0] rd,
	output stallF, 
	output stallD, 
	output flushD, 
	output flushE, 
	output flushM
);

wire [31:0] instrD;
wire regwriteD, memtoregD, memwriteD, branchD, alusrcD, regdstD, jumpD, pcsrcD;
wire [2:0] alucontrolD;
wire regwriteE, memtoregE, memwriteE, alusrcE, regdstE;
wire [2:0] alucontrolE;
wire regwriteM; 
wire memtoregM; 
wire regwriteW;
wire memtoregW;

assign rs = instrD[25:21];
assign rt = instrD[20:16];
assign rd = instrD[15:11];

flopenrc #(32) FD_instr (
    .clk(clk),
    .rst(rst),
    .en(~stallD),
	.clear(flushD),
    .d(instr),
    .q(instrD)
);

flopenr #(2) MWsignal(
    .clk(clk),
    .rst(rst),
    .en(1'b1),
    .d({regwriteM, memtoregM}),
    .q({regwriteW, memtoregW})
);

flopenr #(3) EMsignal(
    .clk(clk),
    .rst(rst),
    .en(1'b1),
    .d({regwriteE, memtoregE, memwriteE}),
    .q({regwriteM, memtoregM, memwriteM})
);

floprc #(8) DEsignal(
    .clk(clk),
    .rst(rst),
    .clear(flushE),
    .d({regwriteD, memtoregD, memwriteD, alucontrolD, alusrcD, regdstD}),
    .q({regwriteE, memtoregE, memwriteE, alucontrolE, alusrcE, regdstE})
);

controller con(
	.op(instrD[31:26]),
	.funct(instrD[5:0]),
	.memtoregD(memtoregD),
	.memwriteD(memwriteD),
	.alusrcD(alusrcD),
	.regdstD(regdstD),
	.regwriteD(regwriteD),
	.branchD(branchD),
	.jumpD(jumpD),
	.alucontrolD(alucontrolD)
);

datapath_global_pred datapath(
	.clk(clk),
	.rst(rst),
	.instrD(instrD),
	.readdata(readdata),
	.regwriteE(regwriteE),
	.regwriteM(regwriteM),
	.regwriteW(regwriteW),
	.memtoregW(memtoregW),
	.memtoregE(memtoregE),
	.memtoregM(memtoregM),
	.alucontrolE(alucontrolE),
	.alusrcE(alusrcE),
	.regdstE(regdstE),
	.jumpD(jumpD),
	.branchD(branchD),
	.pc(pc),
	.aluoutM(aluoutM),
	.mem_WriteData(writedata),
	.resultW(resultW),
	.stallF(stallF),
	.stallD(stallD),
	.flushD(flushD),
	.flushE(flushE),
	.flushM(flushM)
);

	
endmodule
