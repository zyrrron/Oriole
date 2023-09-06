`timescale 1ns / 1ps

module binary2gray_64(input [63:0] binary,
                     output [63:0] gray);
   binary2gray #(.N(7'd64)) bin2gray(.binary(binary),
                             .gray(gray));
   
endmodule
