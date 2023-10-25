package server;

import client.clientProtocol;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;


/*
 * server socket main程序
 * 首先我们需要先对该socket创建对应的消息MAP
 * 之后执行main函数，选择监听端口，创建serversocket，等待客户端的连接，连接成功后开启读线程
 * 由于是多人聊天程序，所以需要不断循环监测是否有新的客户端连接
 */
public class serverSocket {
    //输入消息队列管理器和输出消息队列管理器
    public static serverINFO<Integer,clientProtocol> Queues = new serverINFO<Integer,clientProtocol>();

    public static void main(String [] args) {
        try {
            // 监听指定的端口
            int port = 65532; //65532  46188
            ServerSocket server = new ServerSocket(port);
            //作为这个TCP连接的编号，对每个连接，分配两个线程
            System.out.println("服务端启动成功，等待TCP连接");
            while (true) {
                Socket socket = server.accept();
                System.out.println("连接成功");
                //输入流
                InputStream inputStream = socket.getInputStream();
                System.out.println("输入流获取成功");
                //封装对象输入流
                ObjectInputStream objectInputStreams = new ObjectInputStream(inputStream);
                OutputStream outputStream = socket.getOutputStream();
                ObjectOutputStream objectOutputStream = new ObjectOutputStream(outputStream);
                System.out.println("启动读线程");
                //启动读线程，写线程在登录成功后创建
                new readThread(inputStream, objectInputStreams, outputStream,objectOutputStream,server, socket).start();
            }
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}