package server;

import client.clientProtocol;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;


/*
 * server socket main����
 * ����������Ҫ�ȶԸ�socket������Ӧ����ϢMAP
 * ֮��ִ��main������ѡ������˿ڣ�����serversocket���ȴ��ͻ��˵����ӣ����ӳɹ��������߳�
 * �����Ƕ����������������Ҫ����ѭ������Ƿ����µĿͻ�������
 */
public class serverSocket {
    //������Ϣ���й������������Ϣ���й�����
    public static serverINFO<Integer,clientProtocol> Queues = new serverINFO<Integer,clientProtocol>();

    public static void main(String [] args) {
        try {
            // ����ָ���Ķ˿�
            int port = 65532; //65532  46188
            ServerSocket server = new ServerSocket(port);
            //��Ϊ���TCP���ӵı�ţ���ÿ�����ӣ����������߳�
            System.out.println("����������ɹ����ȴ�TCP����");
            while (true) {
                Socket socket = server.accept();
                System.out.println("���ӳɹ�");
                //������
                InputStream inputStream = socket.getInputStream();
                System.out.println("��������ȡ�ɹ�");
                //��װ����������
                ObjectInputStream objectInputStreams = new ObjectInputStream(inputStream);
                OutputStream outputStream = socket.getOutputStream();
                ObjectOutputStream objectOutputStream = new ObjectOutputStream(outputStream);
                System.out.println("�������߳�");
                //�������̣߳�д�߳��ڵ�¼�ɹ��󴴽�
                new readThread(inputStream, objectInputStreams, outputStream,objectOutputStream,server, socket).start();
            }
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}