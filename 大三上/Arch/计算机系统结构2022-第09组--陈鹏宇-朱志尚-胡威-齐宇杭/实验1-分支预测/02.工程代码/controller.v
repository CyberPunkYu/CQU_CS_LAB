`timescale 1ns / 1ps

module controller(input [5:0] op,
                  input [5:0] funct,
                  output memtoregD,
                  output memwriteD,
                  output alusrcD,
                  output regdstD,
                  output regwriteD,
                  output branchD,
                  output [2:0]alucontrolD,
                  output jumpD);

wire [1:0]aluop;

main_decoder main_decoder(
    .op(op),

    .regdst(regdstD),
    .regwrite(regwriteD),
    .alusrc(alusrcD),
    .memwrite(memwriteD),
    .memtoreg(memtoregD),
    .branch(branchD),
    .jump(jumpD),
    .aluop(aluop)
);

aludec aludec(
    .funct(funct),
    .aluop(aluop),
    .alucontrol(alucontrolD)
);

endmodule
