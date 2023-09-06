`timescale 1ns / 1ps

module parity
#(parameter WIDTH=2)
(input [WIDTH-1:0] a,
 output out);
   assign out = ^a;

endmodule
