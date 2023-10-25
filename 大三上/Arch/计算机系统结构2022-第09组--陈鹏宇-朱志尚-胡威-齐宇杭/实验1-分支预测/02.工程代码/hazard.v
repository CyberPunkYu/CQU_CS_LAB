`timescale 1ns / 1ps

module hazard(input [4:0] rsD,
              input [4:0] rtD,
              input [4:0] rsE,
              input [4:0] rtE,
              input [4:0] writeregE,
              input [4:0] writeregM,
              input [4:0] writeregW,
              input regwriteE,
              input regwriteM,
              input regwriteW,
              input memtoregE,
              input memtoregM,
              input pred_takeD,
              input pred_resM,
              
              output [1:0] forwardAE,
              output [1:0] forwardBE,
              output wire stallF, stallD, flushD, flushE, flushM
              );

// --------------------------------
// 数据冒险

// forward
assign forwardAE = ((rsE != 0) && (rsE == writeregM) && regwriteM) ? 2'b10 :
                   ((rsE != 0) && (rsE == writeregW) && regwriteW) ? 2'b01 :
                   2'b00;
assign forwardBE = ((rtE != 0) && (rtE == writeregM) && regwriteM) ? 2'b10 :
                   ((rtE != 0) && (rtE == writeregW) && regwriteW) ? 2'b01 :
                   2'b00;

// --------------------------------
// stall
wire lwstall;
assign lwstall = ((rsD == rtE) || (rtD == rtE)) && memtoregE;
assign stallF = lwstall;
assign stallD = lwstall;
assign flushD = pred_takeD | pred_resM;
assign flushM = pred_resM;
assign flushE = lwstall || pred_resM; 

endmodule
