`timescale 1ns / 1ps

module comparator_1bit
(input a,
 input b, 
 output equal,
 output greater,
 output lower);

assign equal = a ~^ b;
assign lower = (~a) & b;
assign greater = a & (~b);

endmodule


module parity
#(parameter WIDTH=2)
(input [WIDTH-1:0] a,
 output out);
   assign out = ^a;

endmodule


module voter
#(parameter WIDTH=2)
(input [WIDTH-1:0] a,
 input [WIDTH-1:0] b,
 output out);

   wire [WIDTH-1:0] equal, greater, lower;
   wire             parity_equal, parity_greater, parity_lower;
   wire             parity_level2_0, parity_level2_1;
   
   
   comparator_1bit comp [WIDTH-1:0](.a(a),
                                    .b(b),
                                    .equal(equal),
                                    .greater(greater),
                                    .lower(lower));

   parity #(.WIDTH(WIDTH)) par_equal(.a(equal),
                                     .out(parity_equal));
   parity #(.WIDTH(WIDTH)) par_greater(.a(greater),
                                     .out(parity_greater));
   parity #(.WIDTH(WIDTH)) par_lower(.a(lower),
                                     .out(parity_lower));
   

   parity #(.WIDTH(2)) par_level2_0(.a({parity_lower, parity_equal}),
                                     .out(parity_level2_0));
   parity #(.WIDTH(2)) par_level2_1(.a({parity_equal, parity_greater}),
                                     .out(parity_level2_1));

   parity #(.WIDTH(2)) par_out(.a({parity_level2_0, parity_level2_1}),
                                     .out(out));
   

endmodule
