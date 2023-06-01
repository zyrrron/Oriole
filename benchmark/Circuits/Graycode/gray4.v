`timescale 1ns / 1ps

module binary2gray_4(input [3:0] binary,
                     output [3:0] gray);
   binary2gray #(.N(3'd4)) bin2gray(.binary(binary),
                             .gray(gray));
   
endmodule
