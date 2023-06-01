`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 10/08/2020 10:13:09 PM
// Design Name: 
// Module Name: mux
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


module mux
#(parameter WIDTH=2)
(input D0[WIDTH-1:0],
 input D1[WIDTH-1:0],
 input S,
 output Y[WIDTH-1:0]);

   assign Y = S ? D0 : D1; 
    
endmodule
