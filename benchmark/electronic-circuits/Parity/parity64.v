`timescale 1ns / 1ps

module parity64
(input [63:0] a,
 output out);
   parity #(.WIDTH(64)) p(.a(a),
			 .out(out));
   
endmodule
