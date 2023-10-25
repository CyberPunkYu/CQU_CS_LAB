package client;

import java.util.HashMap;
import java.util.Map;
import java.util.LinkedList;

/*
 * ÿ����һ���ͻ��˽��̣��ͻ�����һ����Ӧ����ϢMAP�����ڴ洢�������˵�ͨ��Э��
 * MAP�в�ͬ�ļ���Ӧ��ͬ���͵�Э����Ϣ�������ѯ
 */

//����MAP�Ķ���Ϣ���й���
public class clientINFO<T1,T2> {
	
	/* ������Ϣ���� */
	public class MessageQueue<T> {
	    private LinkedList<T> queue = new LinkedList<T>();
	    //����д����ͬ������ֹ����߳�ͬʱд��
	    public synchronized void push_message(T message){ queue.addLast(message); }
	    public T get_message(){  return queue.getFirst(); }//���ж�
	    public T pop_message(){ return queue.removeFirst(); }//������Ϣ
	    public boolean empty() { return queue.isEmpty(); }
	    public int get_length(){ return queue.size(); }
	}
	
	//����MAP��ÿ�����͵�Э�齨����Ϣ���У������ȡ
    private Map<T1, MessageQueue<T2>> queues = new HashMap<T1, MessageQueue<T2>>();
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
    //�ж�id��Ӧ����Ϣ�������Ƿ�Ϊ��
    public boolean isEmtry(T1 id){ return queues.get(id).empty(); }
}
