package server;

import client.clientProtocol;


import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

/*
 * д�����ɶ����̴�
 * ��ȡ��ID��Ӧ����Ϣ���У�����ͻ���ͨ��
 */

public class writeThread extends Thread{
    private int id;//���
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
            //��ȡ��id����Ϣ����
            boolean isClose = false;
            while(!isClose) {
                Thread.sleep(300);
                //�ȴ���Ϣ���в�Ϊ��
                while(serverSocket.Queues.isEmtry(id)){}
                clientProtocol message = serverSocket.Queues.read(id);
                //����ע���ظ���Ϣ����ע���ɹ���������߳�
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

