`timescale 1ns / 1ps

module binary2gray_8(input [7:0] binary,
                     output [7:0] gray);
   binary2gray #(.N(4'd8)) bin2gray(.binary(binary),
                             .gray(gray));
   
endmodule
