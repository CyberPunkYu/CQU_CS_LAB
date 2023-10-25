package server;

import client.clientProtocol;
import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;

/*
 * ���̶߳�ȡ����Ϣ�����ͨ��Э��������Э����н���
 * �Խ������Э������жϺ󣬽�����Ӧ�Ĵ���
 * ��ת����Э���ٷ�����Ϣ������
 */
//������Ϣ���߳�
public class readThread extends Thread {
    //������
    private InputStream        inputStream;
    private ObjectInputStream  objectInputStream;
    //�����
    private OutputStream       outputStream;
    private ObjectOutputStream objectOutputStream;
    private ServerSocket       server; // �����socket
    private Socket             client; // �ͻ���socket
    //���̳߳�ʼ��
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
            boolean isClose = false;     // ���̹߳رձ�־
            boolean isOpenWrite = false; // д�߳���Ҫͨ�����߳̿���
            //�������
            while (!isClose) {
                //��ȡЭ�����
                clientProtocol clientProtocol = (clientProtocol) objectInputStream.readObject();
                //������Ϣ����������Ϣ�����ش�ת������Ϣ�б�
                List<clientProtocol> relist = serverProtocol.Parsing(clientProtocol);
                //������Ϣ����ת������
                for (clientProtocol message : relist) {
                	//����Э�飬����ת����Ŀ�Ķ�
                    for (int i = 0; i < message.getLenToID(); i++) {
                    	/*
                    	 * ע�⣺�ɷ�����ת����Э��������Ҫ���¼��ظ����ͺ�ת����Ϣ���ͣ���IDΪ3 4 5
                    	 * ת����Ϣ��ʵ��ȡ����ȫת����ֻ��Ҫ�ж�ÿ����Ϣ��Ŀ����Ƿ��0����������ת����ȥ
                    	 * 
                    	 * ��ע�⣬���message�������̶߳����ģ������Ƕ���֮�󾭹������������Ҫת������Ϣ
                    	 */
                        /*****************************��¼�ظ���Ϣ*****************************/
                        if(message.getType() == 3){
                            if(new String(message.getData(), "utf-8").equals("success")){
                                //��¼�ɹ�����id����Ϣ���У���������Ϣ���м���д�߳�
                                System.out.println("��¼�ɹ�");
                                //������ӦID����Ϣ����
                                serverSocket.Queues.putIfAbsent(message.getToID()[0]);
                                //д�߳�����
                                if(!isOpenWrite) {
                                    System.out.println("����д�߳�");
                                    //������ӦID��д����
                                    new writeThread(message.getToID()[0], outputStream, objectOutputStream, server, client).start();
                                    isOpenWrite=true;
                                }
                            }
                        }
                        /*****************************ע��ظ���Ϣ*****************************/
                        if(message.getType() == 5) {
                            System.out.println("ע��ɹ�");
                            //������ӦID����Ϣ����
                            serverSocket.Queues.putIfAbsent(message.getToID()[0]);
                            //д�߳�����
                            if(!isOpenWrite) {
                                System.out.println("����д�߳�");
                                //������ӦID��д����	
                                new writeThread(message.getToID()[0], outputStream, objectOutputStream, server, client).start();
                                isOpenWrite=true;
                            }
                        }
                        /*****************************ת����Ϣ*****************************/
                        if(message.getToID()[i]!=0) {
                            if (serverSocket.Queues.isExist(message.getToID()[i])) {
                                System.out.println("ת������");
                                //������Ϣд���ӦID������
                                serverSocket.Queues.write(message.getToID()[i], message);
                            } else {
                                //���շ��ڷ��ͺ����ǰ�ر�������
                                try {
                                    serverSocket.Queues.write(message.getFromID(), new clientProtocol(100, 0, 1, new int[]{message.getFromID()}, 0, "unlogin".getBytes("utf-8")));
                                }catch (Exception e){
                                    e.printStackTrace();
                                }
                            }
                        }
                    }
                    /*****************************ע����Ϣ*****************************/
                    //�ɷ���˹رո�client������
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
            //20s��ر�TCP����
            Thread.sleep(20000);
            client.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}