package client;

import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectInputStream;

public class ReadThread extends Thread {
    /* 
     * �쳣��ָֹʾ�����ڹٷ�������ֹ������Stop�ȹ��ڲ���ȫ��������Ҫͨ��exit��ȷ�Ͻ����Ƿ���ֹ��
	 * ͨ������£�����run�����������Զ���ֹ���������û����ܻ�ͨ���رմ��������ƽ��̣����ԻὫexit��ֵΪtrue
	 *
	 * һ��һ�������������ĳ�Ա��������ľ�̬��Ա��������volatile����֮����ô�;߱����������壺
	 * ��֤�˲�ͬ�̶߳�����������в���ʱ�Ŀɼ��ԣ���һ���߳��޸���ĳ��������ֵ������ֵ�������߳���˵�������ɼ��ġ�
	 * ��ֹ����ָ��������
	 * 
	 * ��ʵ�����ַ����ر��߳�
	 * һ���첽��ֹ���ͻ��ֶ��رմ��ں�exit��ֵΪtrue
	 * ����ͬ����ֹ���ͻ��ֶ��رմ��ں�exit��ֵΪtrue�������ʱ����false����ͨ�������������˷��͵�ע���ɹ���Ϣ�رյĽ���
	 */
    public volatile boolean exit = false;
    private InputStream          inputStream;
    private ObjectInputStream    objectInputStream;
    /* ���̵߳Ĺ��캯�� */
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
            //������Ϣ
            boolean isClose = false;
            clientProtocol message = null;
            while (true) {
                try {
                    message = (clientProtocol) objectInputStream.readObject();
                    /*
                     * �˴���Ҫ�������type = 4 ��Э�飨ע�����󣩣�����յ�����ͻ��˽��رն����������ر����������
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
            //����������Ϣ����ָ���Ķ��л�����
            clientSocket.queue.write(message.getType() , message);
            /*
             * ����Э���֪�����typeΪ11�����ǽ��������ͻ��˵���Ϣ���ɷ������˲���ת����
             */
            if (message.getType() == 11){ System.out.print("�յ��� " + message.getFromID() + " ���͵����� "); }
            System.out.println("���յ�����Ϊ " + message.getType());
            if(isClose){
                try {
                    Thread.sleep(10000);
                    System.out.println("�ͻ��˹رն�����");
                    objectInputStream.close();
                    inputStream.close();
                } catch (IOException | InterruptedException e) {
                    e.printStackTrace();
                }
                break;
            }
        }
        System.out.println("���߳̽���");
    }
}
