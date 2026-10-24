module add#(
    parameter DATA_IN=256
)(
    input clk,
    input rst,
    input [DATA_IN:0] a,
    input [DATA_IN:0] b,
    output reg [DATA_IN:0] c
);


    always@(posedge clk or negedge rst)
    if(!rst)
        c <= {DATA_IN{1'b0}};
    else
        c <= a + b;

endmodule