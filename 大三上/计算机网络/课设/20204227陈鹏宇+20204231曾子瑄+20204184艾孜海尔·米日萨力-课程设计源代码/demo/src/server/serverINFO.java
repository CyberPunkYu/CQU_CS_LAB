package server;

import java.util.HashMap;
import java.util.Map;
import java.util.LinkedList;

/*
 * һ������˽��̶�Ӧһ����Ϣ����MAP�����ڴ洢����ͻ��˵�ͨ��Э��
 * MAP�в�ͬ�ļ���Ӧ��ͬ���͵�Э����Ϣ�������ѯ
 * 
 * ��clientINFO��ͬ���ǣ�serverINFO�����洢��ͬtype��Э����Ϣ��Ҳ�洢��ͬ�û�ID��ת����Ϣ
 */


//�����Ϣ���й���ģ��
public class serverINFO<T1,T2> {
	
	/* ������Ϣ���� */
	public class MessageQueue<T> {
	    private LinkedList<T> queue = new LinkedList<T>();
	    public synchronized void push_message(T message){ queue.addLast(message); }//����д
	    public T get_message(){ return queue.getFirst(); }//���ж�
	    public T pop_message(){ return queue.removeFirst(); }//������Ϣ
	    public boolean empty() { return queue.isEmpty(); }
	    public int get_length(){ return queue.size(); }
	}
	
	/* ����MAPʵ��ÿ��ID��Ӧ����Ϣ���� */
    private Map<T1,MessageQueue<T2>> queues = new HashMap<T1,MessageQueue<T2>>();
    //����Ϣ����id ���һ����Ϣ
    public void write(T1 id,T2 message){ queues.get(id).push_message(message); }
    //����Ϣ����id�ж�ȡһ����Ϣ
    public T2 read(T1 id){ return queues.get(id).pop_message(); }
    //��id��Ӧ����Ϣ���в�����ʱ������һ���µ���Ϣ����id
    public void putIfAbsent(T1 id){ queues.putIfAbsent(id,new MessageQueue<T2>()); }
    //ɾ��id��Ӧ����Ϣ����
    public void delete(T1 id){ queues.remove(id); }
    //�ж�id ��Ӧ����Ϣ�����Ƿ����
    public boolean isExist(T1 id){ return queues.get(id)!=null; }
    //id��Ӧ����Ϣ�����Ƿ�Ϊ��
    public boolean isEmtry(T1 id){ return queues.get(id).empty(); }
}
