`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/25/2021 06:29:57 PM
// Design Name: 
// Module Name: RCA16
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


module RCA16(
    input [15:0]A, B,
    input Cin,
    output [15:0]S,
    output Cout
    );
    
    wire [2:0]C;
    
    RCA4 rca41(A[3:0], B[3:0], Cin, S[3:0], C[0]);
    RCA4 rca42(A[7:4], B[7:4], C[0], S[7:4], C[1]);
    RCA4 rca43(A[11:8], B[11:8], C[1], S[11:8], C[2]);
    RCA4 rca44(A[15:12], B[15:12], C[2], S[15:12], Cout);
endmodule
