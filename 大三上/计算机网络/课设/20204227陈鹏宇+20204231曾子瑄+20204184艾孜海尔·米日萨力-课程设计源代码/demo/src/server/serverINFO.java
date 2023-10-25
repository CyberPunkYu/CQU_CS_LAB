package server;

import java.util.HashMap;
import java.util.Map;
import java.util.LinkedList;

/*
 * 一个服务端进程对应一个消息队列MAP，用于存储其与客户端的通信协议
 * MAP中不同的键对应不同类型的协议信息，方便查询
 * 
 * 与clientINFO不同的是，serverINFO不仅存储不同type的协议信息，也存储不同用户ID的转发信息
 */


//多个消息队列管理模块
public class serverINFO<T1,T2> {
	
	/* 基础消息队列 */
	public class MessageQueue<T> {
	    private LinkedList<T> queue = new LinkedList<T>();
	    public synchronized void push_message(T message){ queue.addLast(message); }//串行写
	    public T get_message(){ return queue.getFirst(); }//并行读
	    public T pop_message(){ return queue.removeFirst(); }//弹出消息
	    public boolean empty() { return queue.isEmpty(); }
	    public int get_length(){ return queue.size(); }
	}
	
	/* 基于MAP实现每个ID对应的消息队列 */
    private Map<T1,MessageQueue<T2>> queues = new HashMap<T1,MessageQueue<T2>>();
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
    //id对应的消息队列是否为空
    public boolean isEmtry(T1 id){ return queues.get(id).empty(); }
}
