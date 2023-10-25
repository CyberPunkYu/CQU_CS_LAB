module mux2 #(parameter WIDTH = 32)
             (input wire[WIDTH-1:0] a, b,
              input wire s,
              output wire[WIDTH-1:0] y);
    
    assign y = (s == 1'b1) ? a : b;
    
endmodule
