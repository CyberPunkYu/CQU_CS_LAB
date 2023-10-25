package client;
import java.io.Serializable;

/*
 * 协议，网络协议的简称，网络协议是通信计算机双方必须共同遵从的一组约定。
 * 如怎么样建立连接、怎么样互相识别等。只有遵守这个约定，计算机之间才能相互通信交流。
 * 它的三要素是：语法、语义、时序。
 * 自定义应用层协议，所有客户端和服务端的通信都依靠协议
 * 
 * 语法：主要结构如下
 * 协议类型、源ID、目标ID数量、目标ID数组、数据类型、数据字段
 * 协议类型具体如下：
 * 0 为登录请求      1 为注销请求   2 为注册请求
 * 3,4,5为服务端回复，登录/注销/注册    成功/失败
 * 10 为发送消息请求 11 为消息回复(客户端收到的消息type)  
 * 12为获取在线用户请求  13 为在线用户状态回复 100 为异常回复
 * 语义：
 * 该协议的使用场景主要涉及所有C/S通信的事件，如：登录，登录回复，注册，注册回复等
 * 时序没有设计太复杂，主要是每个请求后，接收方都会想发送方进行回复。
 */

public class clientProtocol implements Serializable {
	private static final long serialVersionUID = 1L;
	public clientProtocol(){}
    public clientProtocol(int type,int sourceID,int lenToID,int[] destinID,int datatype,byte[] data){
        this.type=type;//类型
        this.sourceID=sourceID;//请求ID
        this.lenToID=lenToID;//目标ID总数
        this.destinID=destinID;//目标ID数组
        this.datatype=String.valueOf(datatype);//数据类型 0为文本
        this.data=data;//具体的数据
    }
    public clientProtocol(int type,int sourceID,int lenToID,int[] destinID,String datatype,byte[] data){
        this.type=type;
        this.sourceID=sourceID;
        this.lenToID=lenToID;
        this.destinID=destinID;
        this.datatype=datatype;
        this.data=data;
    }

    private int type; 
    private int sourceID;//若是服务端回复则此为 0
    private int lenToID;
    private int[] destinID;
    private String datatype;
    private byte[] data;
    /*协议读写操作*/
    public byte[] getData() { return data; }
    public String getDatatype() { return datatype; }
    public int getFromID() { return sourceID; }
    public int getLenToID() { return lenToID; }
    public int getType() { return type; }
    public int[] getToID() { return destinID; }
    public void setData(byte[] data) { this.data = data; }
    public void setDatatype(int datatype) { this.datatype = String.valueOf(datatype); }
    public void setDatatype(String datatype) { this.datatype = datatype; }
    public void setFromID(int sourceID) { this.sourceID = sourceID; }
    public void setLenToID(int lenToID) { this.lenToID = lenToID; }
    public void setToID(int[] destinID) { this.destinID = destinID; }
    public void setType(int type) { this.type = type; }
    public String getDataTypeString(){ return datatype; }
}
