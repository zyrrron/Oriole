`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/25/2021 06:51:14 PM
// Design Name: 
// Module Name: RCA4
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

module RCA32(
    input [31:0]A, B,
    input Cin,
    output [31:0]S,
    output Cout
    );
    
    wire C;
    
    RCA16 rca161(A[15:0], B[15:0], Cin, S[15:0], C);
    RCA16 rca162(A[31:16], B[31:16], C, S[31:16], Cout);
    
endmodule
