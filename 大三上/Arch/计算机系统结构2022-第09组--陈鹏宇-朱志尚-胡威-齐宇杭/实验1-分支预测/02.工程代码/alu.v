module alu #(WIDTH = 32)
            (input [WIDTH-1:0] a,
             input [WIDTH-1:0] b,
             input [2:0] op,
             output[WIDTH-1:0] result,
             output zero);
    
assign result = (op == 3'b000) ? a & b:
             (op == 3'b001) ? a | b:
             (op == 3'b010) ? a + b:
             (op == 3'b110) ? a - b:
             (op == 3'b111) ? (a<b) ? 1 : 0 :
             8'b0; 

assign zero = ((a-b) == 0);
    
endmodule
