module uart_tx #(
    parameter CLK_FREQ = 50000000,       // 50 MHz
    parameter BAUD_RATE = 115200
)(
    input  wire clk,
    input  wire reset,
    input  wire tx_start,
    input  wire [7:0] tx_data,
    output reg  tx_busy,
    output reg  tx
);

    localparam integer BAUD_DIV = CLK_FREQ / BAUD_RATE;

    reg [15:0] baud_cnt = 0;
    reg baud_tick = 0;

    // UART state machine
    reg [3:0] bit_index = 0;
    reg [9:0] frame = 10'b1111111111; // start + data + stop bits

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            baud_cnt <= 0;
            baud_tick <= 0;
        end else begin
            if (baud_cnt == BAUD_DIV-1) begin
                baud_cnt <= 0;
                baud_tick <= 1;
            end else begin
                baud_cnt <= baud_cnt + 1;
                baud_tick <= 0;
            end
        end
    end

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            tx <= 1;         // idle = high
            tx_busy <= 0;
            bit_index <= 0;
        end else begin
            if (!tx_busy) begin
                if (tx_start) begin
                    // Frame format: 1 start bit, 8 data bits, 1 stop bit
                    frame <= {1'b1, tx_data, 1'b0};
                    tx_busy <= 1;
                    bit_index <= 0;
                end
            end else begin
                if (baud_tick) begin
                    tx <= frame[bit_index];
                    bit_index <= bit_index + 1;

                    if (bit_index == 9) begin
                        tx_busy <= 0;  // Finished
                    end
                end
            end
        end
    end
endmodule
