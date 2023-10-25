`timescale 1ns / 1ps

module aludec(input [5:0] funct,
              input [1:0] aluop,
              output reg [2:0] alucontrol);
    
always @(*) begin
    case (aluop)
        2'b00:begin
            alucontrol <= 3'b010;
        end
        2'b01:begin
            alucontrol <= 3'b110;
        end
        2'b10:begin
            case (funct)
                6'b100000: begin
                    alucontrol <= 3'b010;
                end
                6'b100010: begin
                    alucontrol <= 3'b110;
                end
                6'b100100: begin
                    alucontrol <= 3'b000;
                end
                6'b100101: begin
                    alucontrol <= 3'b001;
                end
                6'b101010: begin
                    alucontrol <= 3'b111;
                end
                default: alucontrol <= 3'b000;
            endcase
        end
        default: begin
            alucontrol <= 3'b000;
        end
    endcase
end
    
    
endmodule
