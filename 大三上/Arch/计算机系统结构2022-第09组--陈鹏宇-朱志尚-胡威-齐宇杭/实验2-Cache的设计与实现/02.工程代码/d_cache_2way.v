module d_cache_2way (
    input wire clk, rst,
    //mips core
    input         cpu_data_req     ,  // CPU发出load或store请求信号
    input         cpu_data_wr      ,  // 写请求信号
    input  [1 :0] cpu_data_size    ,  // 结合地址最低两位，确定数据的有效字节
    input  [31:0] cpu_data_addr    ,  // 数据地址
    input  [31:0] cpu_data_wdata   ,  // 写入数据
    output [31:0] cpu_data_rdata   ,  // 读出数据
    output        cpu_data_addr_ok ,  // 由cache返回ok信号间接传递，地址握手成功
    output        cpu_data_data_ok ,  // 由cache返回的ok间接传递 ，说明读写成功

    //axi interface
    output         cache_data_req     , // cache发出load或store请求信号
    output         cache_data_wr      , // 写请求信号
    output  [1 :0] cache_data_size    ,
    output  [31:0] cache_data_addr    ,
    output  [31:0] cache_data_wdata   , // 写入内存的数据
    input   [31:0] cache_data_rdata   , // 从内存读出的数据
    input          cache_data_addr_ok , // 由mem确认addr已经收到，地址握手成功
    input          cache_data_data_ok   // 由mem返回的ok间接传递 ，说明读写成功
);
    //Cache配置
    parameter  INDEX_WIDTH  = 9, OFFSET_WIDTH = 2;//由于两路组相联，所以行数少一半，即index少一位
    localparam TAG_WIDTH    = 32 - INDEX_WIDTH - OFFSET_WIDTH;
    localparam CACHE_DEEPTH = 1 << INDEX_WIDTH;
    
    //Cache存储单元
    reg                 cache_valid [CACHE_DEEPTH - 1 : 0][1:0];
    reg                 cache_dirty [CACHE_DEEPTH - 1 : 0][1:0]; // 脏位
    reg                 cache_rec_u [CACHE_DEEPTH - 1 : 0][1:0]; // 记录每个cacheline的使用情况
    reg [TAG_WIDTH-1:0] cache_tag   [CACHE_DEEPTH - 1 : 0][1:0];
    reg [31:0]          cache_block [CACHE_DEEPTH - 1 : 0][1:0];

    //访问地址分解
    wire [OFFSET_WIDTH-1:0] offset;
    wire [INDEX_WIDTH-1:0] index;
    wire [TAG_WIDTH-1:0] tag;
    
    assign offset = cpu_data_addr[OFFSET_WIDTH - 1 : 0];
    assign index = cpu_data_addr[INDEX_WIDTH + OFFSET_WIDTH - 1 : OFFSET_WIDTH];
    assign tag = cpu_data_addr[31 : INDEX_WIDTH + OFFSET_WIDTH];

    //访问Cache line
    wire c_valid[1:0];
    wire c_dirty[1:0]; // 脏位
    wire c_rec_u[1:0]; // 最近使用过
    wire [TAG_WIDTH-1:0] c_tag[1:0];
    wire [31:0] c_block[1:0];

    assign c_valid[0] = cache_valid[index][0];
    assign c_valid[1] = cache_valid[index][1];
    assign c_dirty[0] = cache_dirty[index][0];
    assign c_dirty[1] = cache_dirty[index][1];
    assign c_rec_u[0] = cache_rec_u[index][0]; // 使用标记赋值
    assign c_rec_u[1] = cache_rec_u[index][1]; 
    assign c_tag  [0] = cache_tag  [index][0];
    assign c_tag  [1] = cache_tag  [index][1];
    assign c_block[0] = cache_block[index][0];
    assign c_block[1] = cache_block[index][1];

    //判断是否命中
    wire hit, miss;
    assign hit = c_valid[0] & (c_tag[0] == tag) | c_valid[1] & (c_tag[1] == tag);  //cache两路中其中一路满足条件即为hit
    assign miss = ~hit;
    
    wire c_way;// cache应该替换哪一路
    assign c_way = hit ? (c_valid[0] & (c_tag[0] == tag) ? 1'b0 : 1'b1) : //如果hit，选择hit的那一路
                        c_rec_u[0] ? 1'b1 : 1'b0;                         //如果miss，需要选择最近未使用的那一路

    //读或写
    wire read, write;
    assign write = cpu_data_wr;
    assign read = ~write;

    // 当前cache line是否dirty
    wire dirty, clean; 
    assign dirty = c_dirty[c_way];
    assign clean = ~dirty;

    //FSM 新的状态机
    parameter IDLE = 2'b00, RM = 2'b01, WM = 2'b11;
    reg [1:0] state;
    // 标识是否前一个状态是RM，用于确定写缺失时写内存的时机
    reg from_RM; // 确定更新cache的时间
    always @(posedge clk) begin 
        if(rst) begin//重置
            state <= IDLE;
            from_RM <= 1'b0;
        end
        else begin
            case(state)
                IDLE:begin
                    if (cpu_data_req) begin
                        if (hit) state <= IDLE; // 读写命中  
                        else if (miss & clean) state <= RM;  // 读写miss且not dirty，直接读内存
                        else if (miss & dirty) state <= WM; // 读写miss且dirty，先要写内存
                    end
                    else begin state <= IDLE; end
                    from_RM <= 1'b0; // 该寄存器标识前一个状态是否是 RM，用来确定后续写缺失时 cache line 的更新时机
                end
                RM:begin
                    if (cache_data_data_ok) state <= IDLE; // 如果cache收到mem收到数据ok信息，回到初态
                    else state <= RM;
                    from_RM <= 1'b1;
                end
                WM:begin
                    if (cache_data_data_ok)  state <= RM; // dirty块写回后，需将正确的数据读入进cache，需进入RM态
                    else  state <= WM;
                end
            endcase
        end
    end

    //读内存
    //变量read_req, addr_rcv, read_finish用于构造类sram信号。
    wire read_req;      //一次完整的读事务，从发出读请求到结束 当前是否为RM状态
    reg addr_rcv;       //地址接收成功(addr_ok)后到结束
    wire read_finish;   //数据接收成功(data_ok)，即读请求结束 处于RM状态，且已经得到读取的数据
    always @(posedge clk) begin
        addr_rcv <= rst ? 1'b0 :
                    read_req & cache_data_req & cache_data_addr_ok ? 1'b1 : // read->read_req，写回指令如果dirty且miss，不仅会WM，且会到RM，但单靠read无法确认
                    read_finish ? 1'b0 : 
                    addr_rcv;
    end
    assign read_req = state==RM;
    assign read_finish = read_req & cache_data_data_ok; // read->read_req

    //写内存
    wire write_req;     // 是否处于WM状态
    reg waddr_rcv;      // 处于WM状态，且地址已经得到mem确认
    wire write_finish;  // 处于WM状态，且data已经写入mem 
    always @(posedge clk) begin
        waddr_rcv <= rst ? 1'b0 :
                     write_req & cache_data_req & cache_data_addr_ok ? 1'b1 :
                     write_finish ? 1'b0 : waddr_rcv;
    end
    assign write_req = state==WM;
    assign write_finish = write_req & cache_data_data_ok;

    //output to mips core  cache->cpu
    // 所有和cache相关的都需要添加路数的索引，即c_way
    assign cpu_data_rdata   = hit ? c_block[c_way] : cache_data_rdata;// 命中就读cache line；否则就读从mem取回的数据
    assign cpu_data_addr_ok = (cpu_data_req & hit & read_req) | (cache_data_req & cache_data_addr_ok & read_req);//hit->直接确认 
                                                                                                       //miss->cache_data_req(向内存请求数据）
                                                                                                       //cpu_data_addr_ok与cache_data_addr_ok信号保持一致
                                                                                                       //read_req:由于写回中写回内存后还需要读取内存，所以用read_req表示处于RM阶段                                       
    assign cpu_data_data_ok = (cpu_data_req & hit & read_req) | (cache_data_data_ok & read_req);//hit->直接确认
                                                                                      //miss->收到addr_ok后，data_req就会拉低
                                                                                      //cpu_data_data_ok与cache_data_data_ok保持一致，确认数据已经写入或者返回
                                                                                      //data_ok后会返回IDLE阶段，只能通过RM返回，即读完MEM后

    //output to axi interface cache->axi
    //如果发生读/写缺失时，cache_data_req会拉高，此时有两种情况，读缺失和写缺失
    //read_req说明处在RM状态，但addr_rcv为低电平，说明地址还没有握手成功，一旦握手成功，就会将data_req拉低
    //其中addr_rcv = read_req & cache_data_req & cache_data_addr_ok 取决于cache_data_addr_ok
    assign cache_data_req   = read_req & ~addr_rcv | write_req & ~waddr_rcv;
    assign cache_data_wr    = write_req; // 写请求信号的传递，只有处于WM状态才写。而不是cpu_data_wr信号真就写，写缺失脏也会经过WM
    assign cache_data_size  = cpu_data_size;// 确定数据的有效字节
    assign cache_data_addr  = cache_data_wr ? {c_tag[c_way], index, offset} : cpu_data_addr;//read->读的是cpu_data_addr;write->读的是cache中的地址
    assign cache_data_wdata = c_block[c_way]; //由于写回cache，写回的数据肯定是原来cache的数据

    //写入Cache
    //保存地址中的tag, index，防止addr发生改变
    reg [TAG_WIDTH-1:0] tag_save;
    reg [INDEX_WIDTH-1:0] index_save;
    always @(posedge clk) begin
        tag_save   <= rst ? 0 :
                      cpu_data_req ? tag : tag_save;
        index_save <= rst ? 0 :
                      cpu_data_req ? index : index_save;
    end

    wire [31:0] write_cache_data;
    assign write_cache_data = cpu_data_wdata;

    integer t, w;
    always @(posedge clk) begin
        if(rst) begin
            // 循环遍历每个set里的每一路
            for(t=0; t<CACHE_DEEPTH; t=t+1) begin
                for (w=0; w<2; w=w+1) begin
                    cache_valid[t][w] <= 0; // 刚开始将Cache置为无效
                    cache_dirty[t][w] <= 0; // 置为not dirty
                    cache_rec_u[t][w] <= 0; // 未使用态
                end
            end
        end
        else begin
            if(read_finish) begin //读缺失，访存结束时
                cache_valid[index_save][c_way] <= 1'b1; // 将Cache line置为有效
                cache_dirty[index_save][c_way] <= 1'b0; // 根据流程图，读缺失后将脏位置0
                cache_tag  [index_save][c_way] <= tag_save; // 用当前指令的tag更新cache_tag
                cache_block[index_save][c_way] <= cache_data_rdata; // 读到的数据写入Cache line
            end
            else if(write & hit) begin // hit->写命中直接更新；
                cache_dirty[index][c_way] <= 1'b1; // 脏位置1
                cache_block[index][c_way] <= write_cache_data; // 写入Cache line，使用index而不是index_save
            end
            else if(write & from_RM) begin // from_RM->写缺失经过RM拿到新数据后才能更新；
                cache_dirty[index_save][c_way] <= 1'b1; // 脏位置1
                cache_block[index_save][c_way] <= write_cache_data; // 写入Cache line，使用index_save
            end
            //更新cache line的最近使用情况
            if((read | write) & (hit | from_RM)) begin
                cache_rec_u[index][c_way] <= 1'b1; // c_way赋1
                cache_rec_u[index][c_way ^ 1] <= 1'b0; // 另一路赋0，由于只有两路所以用异或来计算
            end
        end
    end
endmodule