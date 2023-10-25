package client;

import java.util.HashMap;
import java.util.Map;
import java.util.LinkedList;

/*
 * 每开启一个客户端进程，就会新增一个对应的消息MAP，用于存储其与服务端的通信协议
 * MAP中不同的键对应不同类型的协议信息，方便查询
 */

//基于MAP的多消息队列管理
public class clientINFO<T1,T2> {
	
	/* 基础消息队列 */
	public class MessageQueue<T> {
	    private LinkedList<T> queue = new LinkedList<T>();
	    //串行写，做同步，防止多个线程同时写入
	    public synchronized void push_message(T message){ queue.addLast(message); }
	    public T get_message(){  return queue.getFirst(); }//并行读
	    public T pop_message(){ return queue.removeFirst(); }//弹出消息
	    public boolean empty() { return queue.isEmpty(); }
	    public int get_length(){ return queue.size(); }
	}
	
	//基于MAP对每个类型的协议建立消息队列，方便读取
    private Map<T1, MessageQueue<T2>> queues = new HashMap<T1, MessageQueue<T2>>();
    //对消息队列id 添加一条信息
    public void write(T1 id,T2 message){ queues.get(id).push_message(message); }
    //从消息队列id中读取一条信息
    public T2 read(T1 id){ return queues.get(id).pop_message(); }
    //当id对应的消息队列不存在时，开启一个新的消息队列id
    public void putIfAbsent(T1 id){ queues.putIfAbsent(id,new MessageQueue<T2>()); }
    //删除id对应的消息队列
    public void delete(T1 id){ queues.remove(id); }
    //判断id 对应的消息队列是否存在
    public boolean isExist(T1 id){ return queues.get(id)!=null; }
    //判断id对应的消息队列中是否为空
    public boolean isEmtry(T1 id){ return queues.get(id).empty(); }
}
