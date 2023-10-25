`timescale 1ns / 1ps

module mips_local_pred(
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

flopenrc #(32) FD_instr (clk, rst, ~stallD, flushD, instr, instrD);

flopenr #(2) MWsignal(clk, rst, 1'b1, {regwriteM, memtoregM}, {regwriteW, memtoregW});

flopenr #(3) EMsignal(clk, rst, 1'b1, {regwriteE, memtoregE, memwriteE},{regwriteM, memtoregM, memwriteM});

floprc #(8) DEsignal(clk, rst, flushE, {regwriteD, memtoregD, memwriteD, alucontrolD, alusrcD, regdstD},
                                       {regwriteE, memtoregE, memwriteE, alucontrolE, alusrcE, regdstE});

controller con(instrD[31:26], instrD[5:0], memtoregD, memwriteD, alusrcD,
               regdstD, regwriteD, branchD, alucontrolD, jumpD);


datapath_local_pred dpl(clk, rst, instrD, readdata, regwriteE, regwriteM, regwriteW,
                        memtoregW, memtoregE, memtoregW, alusrcE, regdstE, jumpD, branchD,
                        alucontrolE, pc, aluoutM, writedata, resultW, stallF,
                        stallD, flushD, flushE, flushM);
endmodule
