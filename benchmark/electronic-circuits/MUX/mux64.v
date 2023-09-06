`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 10/09/2020 09:50:32 AM
// Design Name: 
// Module Name: mux4
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


module mux64(
    input [63:0] D0,
    input [63:0] D1,
    output S,
    output [63:0]Y
    );
    
    mux #(.WIDTH(64)) m(.D0(D0),
		       .D1(D1),
		       .S(S),
		       .Y(Y));
    
endmodule
