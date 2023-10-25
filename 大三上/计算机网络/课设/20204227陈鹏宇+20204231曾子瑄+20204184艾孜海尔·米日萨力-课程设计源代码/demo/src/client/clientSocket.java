package client;

import java.io.*;
import java.net.Socket;

/*
 * client socket main����
 * ����������Ҫ�ȶԸ�socket������Ӧ����ϢMAP������ʼ��MAP��ÿ����Ϣ����
 * ֮��ִ��main����������socket��������д�̣߳�����GUI
 */
public class clientSocket {

    public static clientINFO<Integer, clientProtocol> queue;
    static {
        queue = new clientINFO<Integer, clientProtocol>();
        //���͵���Ϣ���� id == 0
        queue.putIfAbsent(0);
        //���յ���Ϣ���� id == Э��type
        queue.putIfAbsent(3);
        queue.putIfAbsent(4);
        queue.putIfAbsent(5);
        queue.putIfAbsent(11);
        queue.putIfAbsent(13);
        queue.putIfAbsent(100);
    };

    public static void main(String [] args) throws IOException, ClassNotFoundException, EOFException {
        // ��ȡ�ͻ�������
    	String ip1 = new String("192.168.56.1");
    	int port1  = 65532;
    	String ip2 = new String("218.89.171.135");
    	int port2  = 41067;
    	String ip = ip1;
    	int  port = port1;
        Socket client = new Socket(ip, port); //��������192.168.56.1-->������͸103.46.128.49  �������218.89.171.137 218.89.171.135  41067
//        Socket client = new Socket("218.89.171.135", 41067);
        System.out.println("�ͻ����Ƿ����ӳɹ�:" + client.isConnected());
        // �����������ʼ��
        ObjectOutputStream objectOutputStream  = new ObjectOutputStream(client.getOutputStream());
        ObjectInputStream  objectInputStream   = new ObjectInputStream(client.getInputStream());
        // ��д�̳߳�ʼ��
        ReadThread r = new ReadThread(client.getInputStream(),objectInputStream);
        WriteThread w = new WriteThread(client.getOutputStream(),objectOutputStream);
        // ��д�߳�����
        r.start();
        w.start();
        // GUI����
        clientGUI.runGUI(ip, port);
        //���̵߳ȴ���д�߳̽���
        try {
            r.join();
            w.join();
        }catch (Exception e){
            e.printStackTrace();
        }
        System.out.println("�ͻ��˹ر�");
        client.close();
    }
}