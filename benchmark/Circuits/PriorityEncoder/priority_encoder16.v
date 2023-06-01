`timescale 1ns / 1ps

module priority_encoder16 (input  [15:0]  in,
                          output reg [3:0] out);
   
  always @* begin
    casex (in)
      16'b1xxxxxxxxxxxxxxx : out = 4'd15;
      16'b01xxxxxxxxxxxxxx : out = 4'd14;
      16'b001xxxxxxxxxxxxx : out = 4'd13;
      16'b0001xxxxxxxxxxxx : out = 4'd12;
      16'b00001xxxxxxxxxxx : out = 4'd11;
      16'b000001xxxxxxxxxx : out = 4'd10;
      16'b0000001xxxxxxxxx : out = 4'd9;
      16'b00000001xxxxxxxx : out = 4'd8;
      16'b000000001xxxxxxx : out = 4'd7;
      16'b0000000001xxxxxx : out = 4'd6;
      16'b00000000001xxxxx : out = 4'd5;
      16'b000000000001xxxx : out = 4'd4;
      16'b0000000000001xxx : out = 4'd3;
      16'b00000000000001xx : out = 4'd2;
      16'b000000000000001x : out = 4'd1;
      16'b0000000000000001 : out = 4'd0;
      default              : out = 4'd0;
    endcase
  end

endmodule
