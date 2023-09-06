`timescale 1ns / 1ps

module parity8
(input [7:0] a,
 output out);
   parity #(.WIDTH(8)) p(.a(a),
			 .out(out));
   
endmodule
