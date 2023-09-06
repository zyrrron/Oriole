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


module RCA8(
    input [7:0]A, B,
    input Cin,
    output [7:0]S,
    output Cout
    );
    
    wire C;
    
    RCA4 rca41(A[3:0], B[3:0], Cin, S[3:0], C);
    RCA4 rca42(A[7:4], B[7:4], C, S[7:4], Cout);
    
endmodule
