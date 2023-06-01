`timescale 1ns / 1ps

module binary2gray_16(input [15:0] binary,
                     output [15:0] gray);
   binary2gray #(.N(5'd16)) bin2gray(.binary(binary),
                             .gray(gray));
   
endmodule
