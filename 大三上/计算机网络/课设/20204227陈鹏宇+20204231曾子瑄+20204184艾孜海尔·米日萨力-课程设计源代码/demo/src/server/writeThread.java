package server;

import client.clientProtocol;


import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

/*
 * 写进程由读进程打开
 * 读取本ID对应的消息队列，并与客户端通信
 */

public class writeThread extends Thread{
    private int id;//序号
    private OutputStream       outputStream;
    private ObjectOutputStream objectOutputStream;
    @SuppressWarnings("unused")
	private ServerSocket       server;
    @SuppressWarnings("unused")
    private Socket             client;

    public writeThread(int id, OutputStream outputStream, ObjectOutputStream objectOutputStream, ServerSocket server, Socket client) {
        this.id                 = id;
        this.outputStream 		= outputStream;
        this.objectOutputStream = objectOutputStream;
        this.server 			= server;
        this.client 			= client;
    }
    @Override
    public void run() {
        try {
            //读取本id的消息队列
            boolean isClose = false;
            while(!isClose) {
                Thread.sleep(300);
                //等待消息队列不为空
                while(serverSocket.Queues.isEmtry(id)){}
                clientProtocol message = serverSocket.Queues.read(id);
                //若是注销回复消息，且注销成功，则结束线程
                if(message.getType() == 4){
                    if (new String(message.getData(), "utf-8").equals("success")) { isClose = true; }
                }
                objectOutputStream.writeObject(message);
                objectOutputStream.flush();
            }
            Thread.sleep(5000);
            objectOutputStream.close();
            outputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

