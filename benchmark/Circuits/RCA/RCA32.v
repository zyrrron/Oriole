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

module RCA(
        input A, B, Cin,
        output S,
        output Cout
    );
    
    assign Cout = A*B + (A^B)*Cin;
    assign S = A^B^Cin;
        
endmodule

module RCA4(
    input [3:0]A, B,
    input Cin,
    output [3:0]S,
    output Cout
    );
    
    wire [2:0]C;
    
    RCA rca1(A[0], B[0], Cin, S[0], C[0]);
    RCA rca2(A[1], B[1], C[0], S[1], C[1]);
    RCA rca3(A[2], B[2], C[1], S[2], C[2]);
    RCA rca4(A[3], B[3], C[2], S[3], Cout);
    
endmodule

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

module RCA32(
    input [31:0]A, B,
    input Cin,
    output [31:0]S,
    output Cout
    );
    
    wire C;
    
    RCA rca161(A[15:0], B[15:0], Cin, S[15:0], C);
    RCA rca162(A[31:16], B[31:16], C, S[31:16], Cout);
    
endmodule
