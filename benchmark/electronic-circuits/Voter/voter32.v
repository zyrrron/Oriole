`timescale 1ns / 1ps

module voter32(input [31:0] a,
	      input [31:0] b,
	      output 	  out);
   voter #(.WIDTH(32)) v(.a(a),
			.b(b),
			.out(out));
  
endmodule
