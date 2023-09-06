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
(
 input [WIDTH-1:0] D0,
 input [WIDTH-1:0] D1,
 input S,
 output [WIDTH-1:0] Y
);

   assign Y = S ? D0 : D1; 
    
endmodule

