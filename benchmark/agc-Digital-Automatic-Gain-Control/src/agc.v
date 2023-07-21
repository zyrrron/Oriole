`timescale 1 ns /  1 ps
module agc_tb();

	reg clk;
	reg RESETn;
	wire overload;
	wire [5:0] gain_array_out;
	wire done;

	reg [5:0] target_gain;

	// Don't care about these for now
	reg [3:0] amplified_signal;
	wire [63:0] vga_control;

	//DUT Instantiation
	agc dut(
		.clk             (clk),
		.RESETn          (RESETn),
		.amplified_signal(amplified_signal),
		.overload        (overload),
		.ext_or_int		 (1'b1),
		.vga_control	 (vga_control),
		.gain_array_out  (gain_array_out),
		.done_out        (done)
		);

	//assign target_gain = 6'd39;
	assign overload = (gain_array_out > target_gain);

	initial begin 
		clk = 0;
		RESETn = 1;
		amplified_signal = 16'd0;
		target_gain = 6'd63;			//Tiny signal; gain is maxed
		#10 RESETn = 0;
		#20 RESETn = 1;
		#1000 target_gain = 6'd56;		//Some signal, lower gain
	end
	always
		#5 clk = ~clk;

  //--------------------------------------------------------------------
  // Timeout
  //--------------------------------------------------------------------
  // If something goes wrong, kill the simulation...
/*  reg [  63:0] cycle_count = 0;
  always @(posedge clk) begin
    cycle_count = cycle_count + 1;
    if (cycle_count >= 3000) begin
      $display("TIMEOUT");
      $finish;
    end
  end*/


endmodule // agc_tb

module mapping_function(
	input [5:0] gain_array,
	output reg [4:0] vga1_control,
	output reg [3:0] vga2_control,
	output reg [3:0] vga3_control
	);

always @(*) begin : proc_mapping
	vga1_control = 5'b10010;
	vga2_control = 4'b1010;
	vga3_control = 4'b1010;
	case(gain_array)
		6'd38: begin
			vga1_control = 5'd18;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd37: begin
			vga1_control = 5'd17;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd36: begin
			vga1_control = 5'd16;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd35: begin
			vga1_control = 5'd15;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd34: begin
			vga1_control = 5'd14;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd33: begin
			vga1_control = 5'd13;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd32: begin
			vga1_control = 5'd12;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd31: begin
			vga1_control = 5'd11;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd30: begin
			vga1_control = 5'd10;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd29: begin
			vga1_control = 5'd9;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd28: begin
			vga1_control = 5'd8;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd27: begin
			vga1_control = 5'd7;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd26: begin
			vga1_control = 5'd6;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd25: begin
			vga1_control = 5'd5;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd24: begin
			vga1_control = 5'd4;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd23: begin
			vga1_control = 5'd3;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd22: begin
			vga1_control = 5'd2;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd21: begin
			vga1_control = 5'd1;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd20: begin
			vga1_control = 5'd0;
			vga2_control = 4'd10;
			vga3_control = 4'd10;
		end
		6'd19: begin
			vga1_control = 5'd0;
			vga2_control = 4'd9;
			vga3_control = 4'd10;
		end
		6'd18: begin
			vga1_control = 5'd0;
			vga2_control = 4'd8;
			vga3_control = 4'd10;
		end
		6'd17: begin
			vga1_control = 5'd0;
			vga2_control = 4'd7;
			vga3_control = 4'd10;
		end
		6'd16: begin
			vga1_control = 5'd0;
			vga2_control = 4'd6;
			vga3_control = 4'd10;
		end
		6'd15: begin
			vga1_control = 5'd0;
			vga2_control = 4'd5;
			vga3_control = 4'd10;
		end
		6'd14: begin
			vga1_control = 5'd0;
			vga2_control = 4'd4;
			vga3_control = 4'd10;
		end
		6'd13: begin
			vga1_control = 5'd0;
			vga2_control = 4'd3;
			vga3_control = 4'd10;
		end
		6'd12: begin
			vga1_control = 5'd0;
			vga2_control = 4'd2;
			vga3_control = 4'd10;
		end
		6'd11: begin
			vga1_control = 5'd0;
			vga2_control = 4'd1;
			vga3_control = 4'd10;
		end
		6'd10: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd10;
		end
		6'd9: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd9;
		end
		6'd8: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd8;
		end
		6'd7: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd7;
		end
		6'd6: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd6;
		end
		6'd5: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd5;
		end
		6'd4: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd4;
		end
		6'd3: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd3;
		end
		6'd2: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd2;
		end
		6'd1: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd1;
		end
		6'd0: begin
			vga1_control = 5'd0;
			vga2_control = 4'd0;
			vga3_control = 4'd0;
		end
		default: begin
			vga1_control = 5'b10010;
			vga2_control = 4'b1010;
			vga3_control = 4'b1010;
		end
	endcase // gain_array
end
endmodule // mapping_function

module gain_binary_search(
	input clk,
	input RESETn,
	input adjust,
	input up_dn,				//When adjust = 1, increase gain array if up_dn = 1; decrease if up_dn = 0
	output reg [5:0] gain_array,
	output wire done			//Signals binary search through gain array has completed
);

reg [2:0] ptr;

assign done = (&ptr);			//When ptr = 000, and one more adjustment is made, ptr - 1 = 111, and it's the only time &ptr == 1


always @(posedge clk) begin
	if(!RESETn) begin
		gain_array <= 6'b111111;
		ptr <= 3'b101;
	end
	else begin
		if(adjust) begin
			//Turn up gain, as long as gain is not maxed
			if(up_dn && (gain_array != 6'b111111)) begin
				gain_array[ptr] <= 0;
				gain_array[ptr+1] <= 1;
				ptr <= ptr - 1;
			end
			//Turn down gain
			else if(!up_dn) begin 
				gain_array[ptr] <= 0;
				ptr <= ptr - 1;
			end
		end
	end
end

/*always @(posedge clk) begin
	if(!RESETn) begin
		gain_array <= 6'b100110;
		ptr <= 3'b101;
	end
	else begin
		if(adjust) begin
			//Turn up gain, as long as gain is not maxed
			if(up_dn && (gain_array != 6'b100110)) begin
				if(gain_array == 6'b011111) begin
					gain_array <= 6'b100011;
					ptr <= 3'b001;
				end
				else begin
					gain_array[ptr] <= 0;
					gain_array[ptr+1] <= 1;
					ptr <= ptr - 1;
				end
			end
			//Turn down gain
			else if(!up_dn) begin 
				if(gain_array == 6'b100110) begin 
					gain_array <= 6'b011111;
				end
				else begin 
					gain_array[ptr] <= 0;
				end
				ptr <= ptr - 1;
			end
		end
	end
end*/

endmodule // gain_binary_search

module agc_controller(
	input clk,
	input RESETn,
	input [3:0] counter1,
	input [7:0] counter2,
	input [7:0] target_counter2,
	input indicator,
	input done,
	output reg counter1_mode,
	output reg counter2_mode,
	//output reg preamble_counter_mode,
	output reg detect_mode,
	output reg adjust,
	output reg up_dn
	);

//State Encoding
localparam s_reset = 2'b00,
		   s_detect = 2'b01,
		   s_adjust = 2'b10,
		   s_done = 2'b11;

reg [1:0] state;
reg [1:0] next_state;

always @(*) begin: next_state_logic
	next_state = state;
	case(state)
		s_reset: begin
			next_state = s_detect;
		end

		s_detect: begin
			if(done)
				next_state = s_done;
			else if(counter1 == 4'b1111)
				next_state = s_adjust;
		end

		s_adjust: begin
			if(done)
				next_state = s_done;
			else if(counter2 == target_counter2)
				next_state = s_detect;
		end

		s_done: begin 
			//Do nothing.
		end

		default: begin
			next_state = s_reset;
		end
	endcase // state
end // next_state_logic

always @(*) begin : state_actions
	counter1_mode = 0;
	counter2_mode = 0;
	//preamble_counter_mode = 1;
	detect_mode = 0;
	adjust = 0;
	up_dn = 1;
	case(state)
		s_reset: begin
			//preamble_counter_mode = 0;
		end

		s_detect: begin 
			counter1_mode = 1;
			detect_mode = 1;
		end

		s_adjust: begin 
			counter2_mode = 1;
			adjust = 1;
			up_dn = !indicator;
		end

		s_done: begin 

		end
	endcase // state
end // state_actions

always @(posedge clk) begin : next_state_assignment
	if(!RESETn) begin
		state <= s_reset;
	end else begin
		state <= next_state;
	end
end // next_state_assignment
endmodule // agc_controller

module agc(
	input clk, RESETn,

	//Output of ADC, after being amplified by the VGAs
	input [3:0] amplified_signal,

	//One bit signaling if input is saturated
	input overload,

	//Controls if the overload signal is generated internally (0) or externally (1)
	input ext_or_int,

	output wire [63:0] vga_control,

	//Outputs for debugging
	output wire [5:0] gain_array_out,
	output wire done_out

	);


reg indicator;
reg [3:0] counter1;
reg [7:0] counter2;
//reg [10:0] preamble_counter;
reg last_adjust;

wire [5:0] gain_array;
wire counter1_mode;			//0: reset, 1: count up
wire counter2_mode;
wire [7:0] target_counter2;
//wire preamble_counter_mode;
wire detect_mode;			//0: clear indicator, 1: "envelope" detection
wire adjust_pos_edge;
wire adjust;
wire up_dn;
wire bs_done;
wire done;
wire internal_overload;

assign adjust_pos_edge = adjust && !last_adjust;
//assign done = bs_done || (&preamble_counter);
assign done = bs_done;
assign internal_overload = (ext_or_int ? overload : (&amplified_signal));
assign target_counter2 = 8'd160;		//160 cycles @ 16MHz = 10us

//Debugging outputs
assign gain_array_out = gain_array;
assign done_out = done;
assign vga_control = {64{1'b1}};		//This needs to be changed once mapping is confirmed

gain_binary_search gbs(
	.clk       (clk),
	.RESETn    (RESETn),
	.adjust    (adjust_pos_edge),
	.up_dn     (up_dn),
	.gain_array(gain_array),
	.done      (bs_done)
	);

agc_controller agcc(
	.clk                  (clk),
	.RESETn               (RESETn),
	.counter1             (counter1),
	.counter2             (counter2),
	.target_counter2	  (target_counter2),
	.indicator            (indicator),
	.done                 (bs_done),
	.counter1_mode        (counter1_mode),
	.counter2_mode        (counter2_mode),
	//.preamble_counter_mode(preamble_counter_mode),
	.detect_mode          (detect_mode),
	.adjust               (adjust),
	.up_dn                (up_dn)
	);

/*mapping_function mf(
	.gain_array  (gain_array),
	.vga1_control(vga1_control),
	.vga2_control(vga2_control),
	.vga3_control(vga3_control)
	);*/

always @(posedge clk) begin : proc_counters
	if(~RESETn) begin
		counter1 <= 4'b0;
		counter2 <= 8'b0;
		//preamble_counter <= 11'b0;
		indicator <= 1'b0;
		last_adjust <= 1'b0;
	end else begin
		counter1 <= (counter1_mode ? counter1 + 1 : 4'b0);
		counter2 <= (counter2_mode ? counter2 + 1 : 8'b0);
		//preamble_counter <= (preamble_counter_mode ? preamble_counter + 1 : 11'b0);	
		indicator <= (detect_mode ? (indicator || internal_overload) : 0);
		last_adjust <= adjust;
	end
end
endmodule // agc
