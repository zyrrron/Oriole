`timescale 1ns / 1ps

module voter4(input [3:0] a,
	      input [3:0] b,
	      output 	  out);
   voter #(.WIDTH(4)) v(.a(a),
			.b(b),
			.out(out));
  
endmodule
