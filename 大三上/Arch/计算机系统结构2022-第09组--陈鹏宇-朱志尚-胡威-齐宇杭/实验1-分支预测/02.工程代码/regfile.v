`timescale 1ns / 1ps

module regfile(
	input wire clk,
	input wire rst,
	input wire we3,
	input wire[4:0] ra1,ra2,wa3,
	input wire[31:0] wd3,
	output wire[31:0] rd1,rd2
    );

	reg [31:0] rf[31:0];
	always @(posedge clk) begin
		if (rst) begin
		     rf[0] <= 32'b0;
		end else if(we3) begin
			 rf[wa3] <= wd3;
		end
	end

	assign rd1 = (ra1 != 0) ? rf[ra1] : 0;
	assign rd2 = (ra2 != 0) ? rf[ra2] : 0;
	
	assign r2 = rf[2];
	assign r4 = rf[4];
	assign r5 = rf[5];
	assign r7 = rf[7];
endmodule
