`timescale 1ns / 1ps

module globalPred(
	input wire clk,
	input wire rst,
	output wire [31:0] writedata,
	output wire [31:0] dataadr,
	output wire memwrite,
    output [31:0] instr,
    output [31:0] pc,
    output [31:0] resultW,
	output [4:0] rs,
	output [4:0] rt,
	output [4:0] rd,
	output stallF,
	output stallD,
	output flushD, 
	output flushE, 
	output flushM,
	output wire [31:0] readd
);

mips_global_pred mips_global_pred(
	.clk(clk),
	.rst(rst),
	.instr(instr),
	.readdata(readd),
	.memwriteM(memwrite),
	.pc(pc),
	.aluoutM(dataadr),
	.writedata(writedata),
	.resultW(resultW),
	.rs(rs),
	.rt(rt),
	.rd(rd),
    .stallF(stallF),
	.stallD(stallD),
	.flushD(flushD),
	.flushE(flushE),
	.flushM(flushM)
);

data_ram data_ram(
	.clka(~clk),
	.ena(1'b1),
	.wea({4{memwrite}}),
	.addra(dataadr),
	.dina(writedata),	
	.douta(readd)	
);

inst_ram inst_ram(
	.clka(~clk),
	.ena(1'b1),    
	.wea(4'b0000),     
	.addra({2'b0, pc[7:2]}),
	.dina(32'b0),    
	.douta(instr)
);

endmodule
