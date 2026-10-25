module top #(
    parameter DATA_IN=256
)(
    input clk,
    input rst,
    input [DATA_IN-1:0] a1,
    input [DATA_IN-1:0] b1,
    input [DATA_IN-1:0] c1,
    output [DATA_IN-1:0] d1
);

    wire [DATA_IN-1:0] b2;
    wire [DATA_IN-1:0] c2;

    assign d1 = c2;

    add #( 
        .DATA_IN(DATA_IN)
    ) add_inst00 (
        .clk(clk),
        .rst(rst),
        .a(a1),
        .b(b1),
        .c(b2)
    );

    add #( 
        .DATA_IN(DATA_IN)
    ) add_inst01 (
        .clk(clk),
        .rst(rst),
        .a(b2),
        .b(c1),
        .c(c2)
    );

endmodule