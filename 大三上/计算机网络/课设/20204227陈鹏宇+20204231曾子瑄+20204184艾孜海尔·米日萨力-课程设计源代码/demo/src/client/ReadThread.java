package client;

import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;

public class ReadThread extends Thread {
    /* 
     * 异常终止指示，由于官方进程终止函数如Stop等过于不安全，所以需要通过exit来确认进程是否终止，
	 * 通常情况下，是在run函数结束后自动终止，但由于用户可能会通过关闭窗口来中制进程，所以会将exit赋值为true
	 *
	 * 一旦一个共享变量（类的成员变量、类的静态成员变量）被volatile修饰之后，那么就具备了两层语义：
	 * 保证了不同线程对这个变量进行操作时的可见性，即一个线程修改了某个变量的值，这新值对其他线程来说是立即可见的。
	 * 禁止进行指令重排序。
	 * 
	 * 其实有两种方法关闭线程
	 * 一是异步终止，客户手动关闭窗口后，exit赋值为true
	 * 二是同步终止，客户手动关闭窗口后，exit赋值为true，但检测时还是false，是通过解析服务器端发送的注销成功消息关闭的进程
	 */
    public volatile boolean exit = false;
    private InputStream          inputStream;
    private ObjectInputStream    objectInputStream;
    /* 读线程的构造函数 */
    public ReadThread(InputStream inputStream, ObjectInputStream objectInputStream){
        this.inputStream       = inputStream;
        this.objectInputStream = objectInputStream;
    }

    @Override
    public void run(){
        while(true) {
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            if(exit){
                try {
                    objectInputStream.close();
                    inputStream.close();
                }catch (Exception e){
                    e.printStackTrace();
                    break;
                }
                break;
            }
            //接收信息
            boolean isClose = false;
            clientProtocol message = null;
            while (true) {
                try {
                    message = (clientProtocol) objectInputStream.readObject();
                    /*
                     * 此处需要额外监听type = 4 的协议（注销请求），如果收到，则客户端将关闭读监听，即关闭输入输出流
                     */
                    if(message.getType()==4 && new String(message.getData(),"utf-8").equals("success")){
                        isClose = true;
                        break;
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
                if (message == null) {
                    continue;
                } else {
                    break;
                }
            }
            //将读到的消息加入指定的队列缓冲区
            clientSocket.queue.write(message.getType() , message);
            /*
             * 根据协议可知，如果type为11，则是接收其他客户端的消息（由服务器端参与转发）
             */
            if (message.getType() == 11){ System.out.print("收到从 " + message.getFromID() + " 发送的数据 "); }
            System.out.println("接收的类型为 " + message.getType());
            if(isClose){
                try {
                    Thread.sleep(10000);
                    System.out.println("客户端关闭读监听");
                    objectInputStream.close();
                    inputStream.close();
                } catch (IOException | InterruptedException e) {
                    e.printStackTrace();
                }
                break;
            }
        }
        System.out.println("读线程结束");
    }
}
