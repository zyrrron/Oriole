`timescale 1ns / 1ps

module parity32
(input [31:0] a,
 output out);
   parity #(.WIDTH(32)) p(.a(a),
			 .out(out));
   
endmodule
