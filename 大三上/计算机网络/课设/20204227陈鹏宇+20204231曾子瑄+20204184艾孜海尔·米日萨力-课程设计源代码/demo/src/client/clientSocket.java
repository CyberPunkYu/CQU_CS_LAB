package client;

import java.io.*;
import java.net.Socket;

/*
 * client socket main程序
 * 首先我们需要先对该socket创建对应的消息MAP，并初始化MAP中每个消息队列
 * 之后执行main函数，创建socket，开启读写线程，开启GUI
 */
public class clientSocket {

    public static clientINFO<Integer, clientProtocol> queue;
    static {
        queue = new clientINFO<Integer, clientProtocol>();
        //发送的消息队列 id == 0
        queue.putIfAbsent(0);
        //接收的消息队列 id == 协议type
        queue.putIfAbsent(3);
        queue.putIfAbsent(4);
        queue.putIfAbsent(5);
        queue.putIfAbsent(11);
        queue.putIfAbsent(13);
        queue.putIfAbsent(100);
    };

    public static void main(String [] args) throws IOException, ClassNotFoundException, EOFException {
        // 获取客户端链接
    	String ip1 = new String("192.168.56.1");
    	int port1  = 65532;
    	String ip2 = new String("218.89.171.135");
    	int port2  = 41067;
    	String ip = ip1;
    	int  port = port1;
        Socket client = new Socket(ip, port); //本机内网192.168.56.1-->内网穿透103.46.128.49  外机外网218.89.171.137 218.89.171.135  41067
//        Socket client = new Socket("218.89.171.135", 41067);
        System.out.println("客户端是否连接成功:" + client.isConnected());
        // 输入输出流初始化
        ObjectOutputStream objectOutputStream  = new ObjectOutputStream(client.getOutputStream());
        ObjectInputStream  objectInputStream   = new ObjectInputStream(client.getInputStream());
        // 读写线程初始化
        ReadThread r = new ReadThread(client.getInputStream(),objectInputStream);
        WriteThread w = new WriteThread(client.getOutputStream(),objectOutputStream);
        // 读写线程启动
        r.start();
        w.start();
        // GUI启动
        clientGUI.runGUI(ip, port);
        //主线程等待读写线程结束
        try {
            r.join();
            w.join();
        }catch (Exception e){
            e.printStackTrace();
        }
        System.out.println("客户端关闭");
        client.close();
    }
}