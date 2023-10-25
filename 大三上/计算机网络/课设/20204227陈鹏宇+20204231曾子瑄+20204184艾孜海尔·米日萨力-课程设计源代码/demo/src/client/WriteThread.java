package client;

import java.io.*;

public class WriteThread extends Thread {
    /* 
     * 异常终止指示，由于官方进程终止函数如Stop等过于不安全，所以需要通过exit来确认进程是否终止，
	 * 通常情况下，是在run函数结束后自动终止，但由于用户可能会通过关闭窗口来中制进程，所以会将exit赋值为true
	 *
	 * 一旦一个共享变量（类的成员变量、类的静态成员变量）被volatile修饰之后，那么就具备了两层语义：
	 * 保证了不同线程对这个变量进行操作时的可见性，即一个线程修改了某个变量的值，这新值对其他线程来说是立即可见的。
	 * 禁止进行指令重排序。
	 */
    public volatile boolean exit = false;
    private OutputStream          outputStream;
    private ObjectOutputStream    objectOutputStream;
    /* 写线程的构造函数 */
    public WriteThread(OutputStream outputStream,ObjectOutputStream objectOutputStream){
        this.outputStream       = outputStream;
        this.objectOutputStream = objectOutputStream;
    }

    @Override
    public void run(){
        while(true){
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            if(exit){
                try {
                    objectOutputStream.close();
                    outputStream.close();
                }catch (Exception e){
                    e.printStackTrace();
                    break;
                }
                break;
            }
            //监听id == 0的消息队列（需要发送的信息）
            while(clientSocket.queue.isEmtry(0)){};
            //任何event都会先将消息放入队列缓存中，然后写进程再从缓存中读取消息并于服务端交流
            clientProtocol message = clientSocket.queue.read(0);
            try {
                objectOutputStream.writeObject(message);
                Thread.sleep(500);
            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
            /*
             * type为1是注销请求，当写线程读取到时，就直接关闭输出流，关闭写监听
             */
            if(message.getType()==1){
                try {
                    Thread.sleep(10000);
                    System.out.println("客户端关闭写监听");
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                try {
                    objectOutputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                try {
                    outputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                break;
            }
        }
        System.out.println("写线程结束");
    }
}
