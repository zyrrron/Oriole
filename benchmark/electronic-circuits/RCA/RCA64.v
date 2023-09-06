`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/25/2021 07:00:15 PM
// Design Name: 
// Module Name: RCA64
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

module RCA64(
    input [63:0]A, B,
    input Cin,
    output [63:0]S,
    output Cout
    );
    
    wire [2:0]C;
    
    RCA16 rca161(A[15:0], B[15:0], Cin, S[15:0], C[0]);
    RCA16 rca162(A[31:16], B[31:16], C[0], S[31:16], C[1]);
    RCA16 rca163(A[47:32], B[47:32], C[1], S[47:32], C[2]);
    RCA16 rca164(A[63:48], B[63:48], C[2], S[63:48], Cout);
endmodule







