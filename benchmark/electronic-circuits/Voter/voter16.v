`timescale 1ns / 1ps

module voter16(input [15:0] a,
	      input [15:0] b,
	      output 	  out);
   voter #(.WIDTH(16)) v(.a(a),
			.b(b),
			.out(out));
  
endmodule
