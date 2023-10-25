## 简介

此目录包含了一个接口为类sram的cpu核，可以将其作为一个模块在其它地方使用。

> **关于封装接口的重要性**：在原来的设计中，cache同时充当了sram转axi的作用，这导致cache和cpu耦合度很高，有许多相互的潜在假设，十分不清晰，这导致这次将datapath封装成类sram并没有那么顺利。而经过这次封装后，虽然多经过了一次转换降低了效率，但也使得之后的设计可以聚焦于每个模块内，改错也更加方便。

本目录代码基于tag v1.0，使用了其中的datapath，并基于其sram接口封装成了类sram接口。然后使用了龙芯官方提供的cpu_axi_interface模块，封装成axi接口，用于接入龙芯发布包的测试环境。

结构图如下：

```
//           ---------------------------------------    mycpu_top.v
//        |   -------------------------    mips core|
//        |   |        data_path       |            |
//        |   -------------------------             |
//        |        | sram       | sram              |
//        |      ----           ----                |
//        |     |    |         |    |               |
//        |      ----           ----                |
//        |        | sram-like    | sram-like       |
//           ---------------------------------------
//                 | sram-like    | sram-like
//           ---------------------------------------
//        |    								cache    |
//        |    								         |
//           ---------------------------------------
//                 | sram-like    | sram-like
//           ---------------------------------------
//        |    			cpu_axi_interface(longsoon)  |
//        |    								         |
//           ---------------------------------------
//          			        | axi

```

### sram接口转类sram接口

sram接口代表的是单周期返回数据，而不需要进行握手协商。

以下介绍如何将sram接口转成类sram接口。

#### sram接口扩充

首先定义转换模块（以访存为例）

```verilog
module d_sram_to_sram_like(
    input wire clk, rst,
    //sram
    input wire data_sram_en,
    input wire [31:0] data_sram_addr,
    output wire [31:0] data_sram_rdata,
    input wire [3:0] data_sram_wen, //4位代表每个字节的写使能
    input wire [31:0] data_sram_wdata,
    
    output wire d_stall,
    input wire longest_stall
    
    //sram like
    output wire data_req,
    output wire data_wr,
    output wire [1:0] data_size,
    output wire [31:0] data_addr,   
    output wire [31:0] data_wdata,

    input wire [31:0] data_rdata,
    input wire data_addr_ok,
    input wire data_data_ok
);
    //To Do
endmodule
```

sram接口中以下接口变量容易理解

```verilog
wire data_sram_en
wire [31:0] data_sram_addr
wire [31:0] data_sram_rdata
wire [3:0] data_sram_wen	
wire [31:0] data_sram_wdata
```

对应的是Block Memory Generator ip核的Native类型接口

##### d_stall信号

由于sram接口并不包含握手信号（如类sram的ok，axi的valid-ready），因此转换成类sram需要引入暂停信号，让cpu等待数据返回。

##### longest_stall信号

（这一点可能不好理解）由于有多种原因导致cpu暂停（取指，访存，乘除法），如果在除法暂停期间，取指已经完成，但cpu还在暂停，此时就可能导致重复第二次取指。因此我们还需要一个信号，能够表示cpu流水线暂停的整个时期。根据该信号，我们能够保证一次流水线暂停只取一次指令，只进行一次内存访问。

#### 波形图

![image-20201014174459695](\images\readme\image-20201014174459695.png)

#### 类sram转换

关键代码如下

```verilog
 	reg addr_rcv;      //地址握手成功
    reg do_finish;     //读写事务结束

    always @(posedge clk) begin
        addr_rcv <= rst          ? 1'b0 :
                    ~data_data_ok & data_req & data_addr_ok ? 1'b1 :    //data_data_ok优先
                    data_data_ok ? 1'b0 : addr_rcv;
    end

    always @(posedge clk) begin
        do_finish <= rst          ? 1'b0 :
                     data_data_ok ? 1'b1 :
                     ~longest_stall ? 1'b0 : do_finish;
    end

    //save rdata
    reg [31:0] data_rdata_save;
    always @(posedge clk) begin
        data_rdata_save <= rst ? 32'b0:
                           data_data_ok ? data_rdata : data_rdata_save;
    end

    //sram like
    assign data_req = data_sram_en & ~addr_rcv & ~do_finish;
    assign data_wr = data_sram_en & |data_sram_wen;
    assign data_size = (data_sram_wen==4'b0001 || data_sram_wen==4'b0010 || data_sram_wen==4'b0100 || data_sram_wen==4'b1000) ? 2'b00:
                       (data_sram_wen==4'b0011 || data_sram_wen==4'b1100 ) ? 2'b01 : 2'b10;
    assign data_addr = data_sram_addr;
    assign data_wdata = data_sram_wdata;

    //sram
    assign data_sram_rdata = data_rdata_save;
    assign d_stall = data_sram_en & ~do_finish;
```

#### tips

1. en的语义表示流水线暂停的整个期间是否需要取指/访存，故需要保持不变
2. 其中rcv要保证在req后再拉高，因为很多类sram中addr_ok都是恒为1的。

