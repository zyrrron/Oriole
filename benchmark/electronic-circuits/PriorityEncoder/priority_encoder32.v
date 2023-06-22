`timescale 1ns / 1ps

module priority_encoder16 (input  [31:0]  in,
                          output reg [4:0] out);
   
  always @* begin
    casex (in)
      32'b1xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx : out = 5'd31;
      32'b01xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx : out = 5'd30;
      32'b001xxxxxxxxxxxxxxxxxxxxxxxxxxxxx : out = 5'd29;
      32'b0001xxxxxxxxxxxxxxxxxxxxxxxxxxxx : out = 5'd28;
      32'b00001xxxxxxxxxxxxxxxxxxxxxxxxxxx : out = 5'd27;
      32'b000001xxxxxxxxxxxxxxxxxxxxxxxxxx : out = 5'd26;
      32'b0000001xxxxxxxxxxxxxxxxxxxxxxxxx : out = 5'd25;
      32'b00000001xxxxxxxxxxxxxxxxxxxxxxxx : out = 5'd24;
      32'b000000001xxxxxxxxxxxxxxxxxxxxxxx : out = 5'd23;
      32'b0000000001xxxxxxxxxxxxxxxxxxxxxx : out = 5'd22;
      32'b00000000001xxxxxxxxxxxxxxxxxxxxx : out = 5'd21;
      32'b000000000001xxxxxxxxxxxxxxxxxxxx : out = 5'd20;
      32'b0000000000001xxxxxxxxxxxxxxxxxxx : out = 5'd19;
      32'b00000000000001xxxxxxxxxxxxxxxxxx : out = 5'd18;
      32'b000000000000001xxxxxxxxxxxxxxxxx : out = 5'd17;
      32'b0000000000000001xxxxxxxxxxxxxxxx : out = 5'd16;
      32'b00000000000000001xxxxxxxxxxxxxxx : out = 5'd15;
      32'b000000000000000001xxxxxxxxxxxxxx : out = 5'd14;
      32'b0000000000000000001xxxxxxxxxxxxx : out = 5'd13;
      32'b00000000000000000001xxxxxxxxxxxx : out = 5'd12;
      32'b000000000000000000001xxxxxxxxxxx : out = 5'd11;
      32'b0000000000000000000001xxxxxxxxxx : out = 5'd10;
      32'b00000000000000000000001xxxxxxxxx : out = 5'd9;
      32'b000000000000000000000001xxxxxxxx : out = 5'd8;
      32'b0000000000000000000000001xxxxxxx : out = 5'd7;
      32'b00000000000000000000000001xxxxxx : out = 5'd6;
      32'b000000000000000000000000001xxxxx : out = 5'd5;
      32'b0000000000000000000000000001xxxx : out = 5'd4;
      32'b00000000000000000000000000001xxx : out = 5'd3;
      32'b000000000000000000000000000001xx : out = 5'd2;
      32'b0000000000000000000000000000001x : out = 5'd1;
      32'b00000000000000000000000000000001 : out = 5'd0;
      default                              : out = 5'd0;
    endcase
  end

endmodule
