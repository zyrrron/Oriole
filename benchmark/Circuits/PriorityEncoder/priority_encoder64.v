`timescale 1ns / 1ps

module priorityenc64(input [63:0] in,
		     output reg [5:0] out);
   

  always @* begin
      casex(in)
        64'b1xxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd63;
        64'b01xx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd62;
        64'b001x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd61;
        64'b0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd60;
        64'b0000_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd59;
        64'b0000_01xx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd58;
        64'b0000_001x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd57;
        64'b0000_0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd56;
        64'b0000_0000_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd55;
        64'b0000_0000_01xx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd54;
        64'b0000_0000_001x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd53;
        64'b0000_0000_0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd52;
        64'b0000_0000_0000_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd51;
        64'b0000_0000_0000_01xx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd50;
        64'b0000_0000_0000_001x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd49;
        64'b0000_0000_0000_0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd48;
        64'b0000_0000_0000_0000_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd47;
        64'b0000_0000_0000_0000_01xx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd46;
        64'b0000_0000_0000_0000_001x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd45;
        64'b0000_0000_0000_0000_0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd44;
        64'b0000_0000_0000_0000_0000_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd43;
        64'b0000_0000_0000_0000_0000_01xx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd42;
        64'b0000_0000_0000_0000_0000_001x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd41;
        64'b0000_0000_0000_0000_0000_0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd40;
        64'b0000_0000_0000_0000_0000_0000_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd39;
        64'b0000_0000_0000_0000_0000_0000_01xx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd38;
        64'b0000_0000_0000_0000_0000_0000_001x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd37;
        64'b0000_0000_0000_0000_0000_0000_0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd36;
        64'b0000_0000_0000_0000_0000_0000_0000_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd35;
        64'b0000_0000_0000_0000_0000_0000_0000_01xx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd34;
        64'b0000_0000_0000_0000_0000_0000_0000_001x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd33;
        64'b0000_0000_0000_0000_0000_0000_0000_0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd32;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd31;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_01xx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd30;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_001x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd29;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd28;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd27;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_01xx_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd26;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_001x_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd25;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0001_xxxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd24;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_1xxx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd23;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_01xx_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd22;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_001x_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd21;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0001_xxxx_xxxx_xxxx_xxxx_xxxx: out = 6'd20;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_1xxx_xxxx_xxxx_xxxx_xxxx: out = 6'd19;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_01xx_xxxx_xxxx_xxxx_xxxx: out = 6'd18;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_001x_xxxx_xxxx_xxxx_xxxx: out = 6'd17;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0001_xxxx_xxxx_xxxx_xxxx: out = 6'd16;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_1xxx_xxxx_xxxx_xxxx: out = 6'd15;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_01xx_xxxx_xxxx_xxxx: out = 6'd14;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_001x_xxxx_xxxx_xxxx: out = 6'd13;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0001_xxxx_xxxx_xxxx: out = 6'd12;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_1xxx_xxxx_xxxx: out = 6'd11;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_01xx_xxxx_xxxx: out = 6'd10;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_001x_xxxx_xxxx: out = 6'd9;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0001_xxxx_xxxx: out = 6'd8;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_1xxx_xxxx: out = 6'd7;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_01xx_xxxx: out = 6'd6;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_001x_xxxx: out = 6'd5;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0001_xxxx: out = 6'd4;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_1xxx: out = 6'd3;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_01xx: out = 6'd2;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_001x: out = 6'd1;
        64'b0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0000_0001: out = 6'd0;
        default:                                                                           : out = 6'd0;
      endcase
  end

endmodule
