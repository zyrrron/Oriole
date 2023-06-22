`timescale 1ns / 1ps

module parity4
(input [3:0] a,
 output out);
   parity #(.WIDTH(4)) p(.a(a),
			 .out(out));
   
endmodule
