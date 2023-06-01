`timescale 1ns / 1ps

// The gray code is an ordering of the binary numbers such that two successive values differ in only
// one bit. 
// Gray codes are commonly used to facilitate error correction in digital communications. For more
// information on gray codes, please refer to https://en.wikipedia.org/wiki/Gray_code

// A very simple way to convert the binary code to gray code is as follows:
// - The most significant bit (MSB) of the Gray code is always equal to the MSB of the given Binary
// code.
// - Other bits of the output Gray code can be obtained by XORing binary code bit at the index and
// previous index.
// In this module, we use the abovementioned implementation. For more information on this
// implementation, refer to https://www.tutorialspoint.com/conversion-of-binary-to-gray-code

// The binary2gray module is a parametrized implementation, where it receives the number of bits as
// an input parameter (N).
// The default value of the input parameter is 4, to create a larger binary gray module, you need to
// create a new verilog file. 
// In the new file, you need to specify the width of the input and output ports based on the number
// of bits in your binary2gray module.
// Then, you need to instantiate the binary2gray module passing an input parameter with the same
// value as the input/output width of your module.

module binary2gray
#(parameter   N = 3'd4)
(input  [N-1:0] binary,
 output reg [N-1:0] gray);
 
  integer i;
  
  always @(*)
  begin
    gray[N-1] = binary[N-1];
    for (i=N-2;i>=0;i=i-1)
      gray[i] = binary[i] ^ binary[i+1];
  end
endmodule
