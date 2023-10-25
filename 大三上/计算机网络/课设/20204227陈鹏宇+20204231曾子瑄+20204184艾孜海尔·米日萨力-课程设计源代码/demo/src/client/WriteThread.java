package client;

import java.io.*;

public class WriteThread extends Thread {
    /* 
     * �쳣��ָֹʾ�����ڹٷ�������ֹ������Stop�ȹ��ڲ���ȫ��������Ҫͨ��exit��ȷ�Ͻ����Ƿ���ֹ��
	 * ͨ������£�����run�����������Զ���ֹ���������û����ܻ�ͨ���رմ��������ƽ��̣����ԻὫexit��ֵΪtrue
	 *
	 * һ��һ�������������ĳ�Ա��������ľ�̬��Ա��������volatile����֮����ô�;߱����������壺
	 * ��֤�˲�ͬ�̶߳�����������в���ʱ�Ŀɼ��ԣ���һ���߳��޸���ĳ��������ֵ������ֵ�������߳���˵�������ɼ��ġ�
	 * ��ֹ����ָ��������
	 */
    public volatile boolean exit = false;
    private OutputStream          outputStream;
    private ObjectOutputStream    objectOutputStream;
    /* д�̵߳Ĺ��캯�� */
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
            //����id == 0����Ϣ���У���Ҫ���͵���Ϣ��
            while(clientSocket.queue.isEmtry(0)){};
            //�κ�event�����Ƚ���Ϣ������л����У�Ȼ��д�����ٴӻ����ж�ȡ��Ϣ���ڷ���˽���
            clientProtocol message = clientSocket.queue.read(0);
            try {
                objectOutputStream.writeObject(message);
                Thread.sleep(500);
            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
            /*
             * typeΪ1��ע�����󣬵�д�̶߳�ȡ��ʱ����ֱ�ӹر���������ر�д����
             */
            if(message.getType()==1){
                try {
                    Thread.sleep(10000);
                    System.out.println("�ͻ��˹ر�д����");
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
        System.out.println("д�߳̽���");
    }
}
