module cache (
    input wire clk, rst,
    //mips core
    input         cpu_inst_req     ,
    input         cpu_inst_wr      ,
    input  [1 :0] cpu_inst_size    ,
    input  [31:0] cpu_inst_addr    ,
    input  [31:0] cpu_inst_wdata   ,
    output [31:0] cpu_inst_rdata   ,
    output        cpu_inst_addr_ok ,
    output        cpu_inst_data_ok ,

    input         cpu_data_req     ,
    input         cpu_data_wr      ,
    input  [1 :0] cpu_data_size    ,
    input  [31:0] cpu_data_addr    ,
    input  [31:0] cpu_data_wdata   ,
    output [31:0] cpu_data_rdata   ,
    output        cpu_data_addr_ok ,
    output        cpu_data_data_ok ,

    //axi interface
    output         cache_inst_req     ,
    output         cache_inst_wr      ,
    output  [1 :0] cache_inst_size    ,
    output  [31:0] cache_inst_addr    ,
    output  [31:0] cache_inst_wdata   ,
    input   [31:0] cache_inst_rdata   ,
    input          cache_inst_addr_ok ,
    input          cache_inst_data_ok ,

    output         cache_data_req     ,
    output         cache_data_wr      ,
    output  [1 :0] cache_data_size    ,
    output  [31:0] cache_data_addr    ,
    output  [31:0] cache_data_wdata   ,
    input   [31:0] cache_data_rdata   ,
    input          cache_data_addr_ok ,
    input          cache_data_data_ok
);

    i_cache i_cache(
        .clk(clk), .rst(rst),
        .cpu_inst_req     (cpu_inst_req     ),
        .cpu_inst_wr      (cpu_inst_wr      ),
        .cpu_inst_size    (cpu_inst_size    ),
        .cpu_inst_addr    (cpu_inst_addr    ),
        .cpu_inst_wdata   (cpu_inst_wdata   ),
        .cpu_inst_rdata   (cpu_inst_rdata   ),
        .cpu_inst_addr_ok (cpu_inst_addr_ok ),
        .cpu_inst_data_ok (cpu_inst_data_ok ),

        .cache_inst_req     (cache_inst_req     ),
        .cache_inst_wr      (cache_inst_wr      ),
        .cache_inst_size    (cache_inst_size    ),
        .cache_inst_addr    (cache_inst_addr    ),
        .cache_inst_wdata   (cache_inst_wdata   ),
        .cache_inst_rdata   (cache_inst_rdata   ),
        .cache_inst_addr_ok (cache_inst_addr_ok ),
        .cache_inst_data_ok (cache_inst_data_ok )
    );

    d_cache_4way_LRU d_cache(
        .clk(clk), .rst(rst),
        .cpu_data_req     (cpu_data_req     ),
        .cpu_data_wr      (cpu_data_wr      ),
        .cpu_data_size    (cpu_data_size    ),
        .cpu_data_addr    (cpu_data_addr    ),
        .cpu_data_wdata   (cpu_data_wdata   ),
        .cpu_data_rdata   (cpu_data_rdata   ),
        .cpu_data_addr_ok (cpu_data_addr_ok ),
        .cpu_data_data_ok (cpu_data_data_ok ),
    
        .cache_data_req     (cache_data_req     ),
        .cache_data_wr      (cache_data_wr      ),
        .cache_data_size    (cache_data_size    ),
        .cache_data_addr    (cache_data_addr    ),
        .cache_data_wdata   (cache_data_wdata   ),
        .cache_data_rdata   (cache_data_rdata   ),
        .cache_data_addr_ok (cache_data_addr_ok ),
        .cache_data_data_ok (cache_data_data_ok )
    );
endmodule