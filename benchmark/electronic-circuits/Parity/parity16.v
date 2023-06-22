`timescale 1ns / 1ps

module parity16
(input [15:0] a,
 output out);
   parity #(.WIDTH(16)) p(.a(a),
			 .out(out));
   
endmodule
