`timescale 1ns / 1ps

module voter8(input [7:0] a,
	      input [7:0] b,
	      output 	  out);
   voter #(.WIDTH(8)) v(.a(a),
			.b(b),
			.out(out));
  
endmodule
