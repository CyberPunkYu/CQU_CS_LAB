package server;

import client.clientProtocol;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;

/*
 * 读线程读取到消息后会先通过协议解析类对协议进行解析
 * 对解析后的协议进行判断后，进行相应的处理
 * 将转发的协议再放入消息队列中
 */
//接收消息的线程
public class readThread extends Thread {
    //输入流
    private InputStream        inputStream;
    private ObjectInputStream  objectInputStream;
    //输出流
    private OutputStream       outputStream;
    private ObjectOutputStream objectOutputStream;
    private ServerSocket       server; // 服务端socket
    private Socket             client; // 客户端socket
    //读线程初始化
    public readThread(InputStream   inputStream , ObjectInputStream  objectInputStream,
                      OutputStream outputStream , ObjectOutputStream objectOutputStream,
                      ServerSocket server       , Socket             client) {
        this.inputStream        = inputStream       ;
        this.objectInputStream  = objectInputStream ;
        this.outputStream       = outputStream      ;
        this.objectOutputStream = objectOutputStream;
        this.server             = server            ;
        this.client             = client            ;
    }


	@Override
    public void run() {
        try {
            Thread.sleep(500);
            boolean isClose = false;     // 读线程关闭标志
            boolean isOpenWrite = false; // 写线程需要通过读线程开启
            //输入监听
            while (!isClose) {
                //读取协议对象
                clientProtocol clientProtocol = (clientProtocol) objectInputStream.readObject();
                //解析消息，并处理消息，返回待转发的消息列表
                List<clientProtocol> relist = serverProtocol.Parsing(clientProtocol);
                //加入消息队列转发请求
                for (clientProtocol message : relist) {
                	//解析协议，将其转发给目的端
                    for (int i = 0; i < message.getLenToID(); i++) {
                    	/*
                    	 * 注意：由服务器转发的协议类型主要是事件回复类型和转发消息类型，其ID为3 4 5
                    	 * 转发消息其实采取的是全转发，只需要判断每个消息的目标端是否非0，若非零则转发出去
                    	 * 
                    	 * 且注意，这个message并不是线程读到的，，而是读到之后经过解析处理后需要转发的信息
                    	 */
                        /*****************************登录回复消息*****************************/
                        if(message.getType() == 3){
                            if(new String(message.getData(), "utf-8").equals("success")){
                                //登录成功则开启id的消息队列，并启动消息队列监听写线程
                                System.out.println("登录成功");
                                //开启对应ID的消息队列
                                serverSocket.Queues.putIfAbsent(message.getToID()[0]);
                                //写线程启动
                                if(!isOpenWrite) {
                                    System.out.println("启动写线程");
                                    //开启对应ID的写进程
                                    new writeThread(message.getToID()[0], outputStream, objectOutputStream, server, client).start();
                                    isOpenWrite=true;
                                }
                            }
                        }
                        /*****************************注册回复消息*****************************/
                        if(message.getType() == 5) {
                            System.out.println("注册成功");
                            //开启对应ID的消息队列
                            serverSocket.Queues.putIfAbsent(message.getToID()[0]);
                            //写线程启动
                            if(!isOpenWrite) {
                                System.out.println("启动写线程");
                                //开启对应ID的写进程	
                                new writeThread(message.getToID()[0], outputStream, objectOutputStream, server, client).start();
                                isOpenWrite=true;
                            }
                        }
                        /*****************************转发消息*****************************/
                        if(message.getToID()[i]!=0) {
                            if (serverSocket.Queues.isExist(message.getToID()[i])) {
                                System.out.println("转发请求");
                                //将该消息写入对应ID队列中
                                serverSocket.Queues.write(message.getToID()[i], message);
                            } else {
                                //接收方在发送后接受前关闭了连接
                                try {
                                    serverSocket.Queues.write(message.getFromID(), new clientProtocol(100, 0, 1, new int[]{message.getFromID()}, 0, "unlogin".getBytes("utf-8")));
                                }catch (Exception e){
                                    e.printStackTrace();
                                }
                            }
                        }
                    }
                    /*****************************注销消息*****************************/
                    //由服务端关闭该client的连接
                    if (message.getType() == 4) {
                        if (new String(message.getData(), "utf-8").equals("success")) {
                            isClose = true;
                            Thread.sleep(10000);
                            objectInputStream.close();
                            inputStream.close();
                        }
                    }
                }
            }
            //20s后关闭TCP链接
            Thread.sleep(20000);
            client.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}