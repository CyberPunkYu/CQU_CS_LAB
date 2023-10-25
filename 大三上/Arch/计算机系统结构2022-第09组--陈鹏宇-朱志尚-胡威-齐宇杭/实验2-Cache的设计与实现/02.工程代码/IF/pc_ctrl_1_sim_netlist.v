// Copyright 1986-2019 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2019.2 (win64) Build 2708876 Wed Nov  6 21:40:23 MST 2019
// Date        : Mon Oct 19 19:51:40 2020
// Host        : DESKTOP-UPCS6CJ running 64-bit major release  (build 9200)
// Command     : write_verilog -force -mode funcsim
//               d:/Depository/NSCSCC/Lab2/cache_lab_v0.02/soc_axi_lite_loongson/run_vivado/mycpu_prj1/mycpu.srcs/sources_1/ip/pc_ctrl_1/pc_ctrl_1_sim_netlist.v
// Design      : pc_ctrl_1
// Purpose     : This verilog netlist is a functional simulation representation of the design and should not be modified
//               or synthesized. This netlist cannot be used for SDF annotated simulation.
// Device      : xc7a200tfbg676-2
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

// (* CHECK_LICENSE_TYPE = "pc_ctrl_1,pc_ctrl,{}" *) (* DowngradeIPIdentifiedWarnings = "yes" *) (* IP_DEFINITION_SOURCE = "package_project" *) 
// (* X_CORE_INFO = "pc_ctrl,Vivado 2019.2" *) 
// (* NotValidForBitStream *)
module pc_ctrl_1
   (branchD,
    branchM,
    succM,
    actual_takeM,
    pred_takeD,
    pc_trapM,
    jumpD,
    jump_conflictD,
    jump_conflictE,
    pc_sel);
  input branchD;
  input branchM;
  input succM;
  input actual_takeM;
  input pred_takeD;
  input pc_trapM;
  input jumpD;
  input jump_conflictD;
  input jump_conflictE;
  output [2:0]pc_sel;

  wire actual_takeM;
  wire branchD;
  wire branchM;
  wire jumpD;
  wire jump_conflictD;
  wire jump_conflictE;
  wire [2:0]pc_sel;
  wire \pc_sel[0]_INST_0_i_1_n_0 ;
  wire pc_trapM;
  wire pred_takeD;
  wire succM;

  LUT6 #(
    .INIT(64'h00000000EEEE0EFE)) 
    \pc_sel[0]_INST_0 
       (.I0(jump_conflictE),
        .I1(\pc_sel[0]_INST_0_i_1_n_0 ),
        .I2(branchM),
        .I3(actual_takeM),
        .I4(succM),
        .I5(pc_trapM),
        .O(pc_sel[0]));
  LUT4 #(
    .INIT(16'h80C0)) 
    \pc_sel[0]_INST_0_i_1 
       (.I0(jump_conflictD),
        .I1(pred_takeD),
        .I2(branchD),
        .I3(jumpD),
        .O(\pc_sel[0]_INST_0_i_1_n_0 ));
  LUT6 #(
    .INIT(64'hFFFFFFFFAAFA2232)) 
    \pc_sel[1]_INST_0 
       (.I0(jump_conflictE),
        .I1(branchM),
        .I2(jumpD),
        .I3(jump_conflictD),
        .I4(succM),
        .I5(pc_trapM),
        .O(pc_sel[1]));
  LUT3 #(
    .INIT(8'hF4)) 
    \pc_sel[2]_INST_0 
       (.I0(succM),
        .I1(branchM),
        .I2(pc_trapM),
        .O(pc_sel[2]));
endmodule
// `ifndef GLBL
// `define GLBL
// `timescale  1 ps / 1 ps

// module glbl ();

//     parameter ROC_WIDTH = 100000;
//     parameter TOC_WIDTH = 0;

// //--------   STARTUP Globals --------------
//     wire GSR;
//     wire GTS;
//     wire GWE;
//     wire PRLD;
//     tri1 p_up_tmp;
//     tri (weak1, strong0) PLL_LOCKG = p_up_tmp;

//     wire PROGB_GLBL;
//     wire CCLKO_GLBL;
//     wire FCSBO_GLBL;
//     wire [3:0] DO_GLBL;
//     wire [3:0] DI_GLBL;
   
//     reg GSR_int;
//     reg GTS_int;
//     reg PRLD_int;

// //--------   JTAG Globals --------------
//     wire JTAG_TDO_GLBL;
//     wire JTAG_TCK_GLBL;
//     wire JTAG_TDI_GLBL;
//     wire JTAG_TMS_GLBL;
//     wire JTAG_TRST_GLBL;

//     reg JTAG_CAPTURE_GLBL;
//     reg JTAG_RESET_GLBL;
//     reg JTAG_SHIFT_GLBL;
//     reg JTAG_UPDATE_GLBL;
//     reg JTAG_RUNTEST_GLBL;

//     reg JTAG_SEL1_GLBL = 0;
//     reg JTAG_SEL2_GLBL = 0 ;
//     reg JTAG_SEL3_GLBL = 0;
//     reg JTAG_SEL4_GLBL = 0;

//     reg JTAG_USER_TDO1_GLBL = 1'bz;
//     reg JTAG_USER_TDO2_GLBL = 1'bz;
//     reg JTAG_USER_TDO3_GLBL = 1'bz;
//     reg JTAG_USER_TDO4_GLBL = 1'bz;

//     assign (strong1, weak0) GSR = GSR_int;
//     assign (strong1, weak0) GTS = GTS_int;
//     assign (weak1, weak0) PRLD = PRLD_int;

//     initial begin
// 	GSR_int = 1'b1;
// 	PRLD_int = 1'b1;
// 	#(ROC_WIDTH)
// 	GSR_int = 1'b0;
// 	PRLD_int = 1'b0;
//     end

//     initial begin
// 	GTS_int = 1'b1;
// 	#(TOC_WIDTH)
// 	GTS_int = 1'b0;
//     end

// endmodule
// `endif