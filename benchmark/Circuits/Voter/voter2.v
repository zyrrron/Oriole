`timescale 1ns / 1ps



module voter2(input [1:0] a,
	      input [1:0] b,
	      output 	  out);
   voter #(.WIDTH(2)) v(.a(a),
			    .b(b),
			    .out(out));
  
endmodule
