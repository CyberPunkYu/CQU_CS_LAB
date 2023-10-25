package client;

import java.util.*;

/*
 * 事件管理，将客户端调用封装为协议，并解析返回协议，类似远程调用
 * 包含注册、登录、注销、发送消息、获取在线用户信息等事件
 * 所有事件都会先封装成协议，然后写入id为0的消息队列中，写线程再从中读取发送给服务端
 */
public class event {
    private static int time = 10000;
    /**********************************注册*************************************/
    public int register(String name, String password){
        try {
        	// 将得到的用户名和密码封装成data
            byte[] data = (name + "," + password).getBytes("utf-8");
            /*
             * 注册事件封装成协议，字段说明如下
             * @ 2: 注册事件标识字段
             * @ 0: 还没有注册成功，没有具体id
             * @ 1: 目的端只有一个
             * @ new int[]{0}: 为0说明发往服务器端
             * @ 0: data类型为文本
             * @ data: 具体封装的数据
             */
            clientProtocol message = new clientProtocol(2, 0, 1, new int[]{0}, 0, data);
            /*
             * 由于需要写进程发送出去，所以要先放入id = 0的消息队列中
             */
            clientSocket.queue.write(0,message);
            //等待服务端处理
            long start = System.currentTimeMillis();
            /*
             * 持续监测id为5的消息队列，其中存放着注册是否成功的消息
             * 为什么要加上循环呢：
             * 服务器端对注册的处理需要时间，需等待一段时间再进行判断
             */
            while(clientSocket.queue.isEmtry(5)){ if(System.currentTimeMillis() - start > time){ break; } }// 等待时间结束
            
            if(clientSocket.queue.isEmtry(5)) {
                return -1;//-1为注册失败，注册成功返回用户的id
            } else {
            	// 提取ID为5的消息队列
                clientProtocol message1 = clientSocket.queue.read(5);
                // 清空
                while(!clientSocket.queue.isEmtry(5)){ clientSocket.queue.read(5); }
                // 这里返回的其实就是本客户端的id
                return message1.getToID()[0];
            }
        }catch (Exception e){
            e.printStackTrace();//注册失败
            return -1;
        }
    }

    /**********************************登录*************************************/
    public boolean login(int id, String password){
        try {
            byte[] data = password.getBytes("utf-8");
            /*
             * 登录事件封装成协议，字段说明如下
             * @ 0: 登录事件标识字段
             * @ id: 客户端id
             * @ 1: 目的端只有一个
             * @ new int[]{0}: 为0说明发往服务器端
             * @ 0: data类型为文本
             * @ data: 具体封装的数据，此处为密码信息
             */
            clientProtocol message = new clientProtocol(0, id, 1, new int[]{0}, 0, data);
            clientSocket.queue.write(0, message);
            //等待服务端处理
            long start = System.currentTimeMillis();
            //持续监测id为3的消息队列，处理登录事件的队列
            while(clientSocket.queue.isEmtry(3)){
                /*
                 * 同上
                 */
                if(System.currentTimeMillis()-start > time){ break; }
            }
            if(clientSocket.queue.isEmtry(3)){
                return false;
            } else {
            	// 服务器端会返回登录是否成功
                clientProtocol message1 = clientSocket.queue.read(3);
                // 清空
                while(!clientSocket.queue.isEmtry(3)){ clientSocket.queue.read(3); }
                if(new String(message1.getData(),"utf-8").equals("success")){ return true; }
                return false;
            }
        }catch (Exception e){
            e.printStackTrace();
            return false;
        }
    }

    /**********************************注销*************************************/
    public void unlogin(int id, String password){
        try {
            byte[] data = password.getBytes("utf-8");
            /*
             * 注销事件封装成协议，字段说明如下
             * @ 1: 注销事件标识字段
             * @ id: 客户端id
             * @ 1: 目的端只有一个
             * @ new int[]{0}: 为0说明发往服务器端
             * @ 0: data类型为文本
             * @ data: 具体封装的数据，此处为密码信息
             */
            clientProtocol message = new clientProtocol(1, id, 1, new int[]{0}, 0, data);
            clientSocket.queue.write(0,message);
            //等待服务端处理
            long start = System.currentTimeMillis();
            while(clientSocket.queue.isEmtry(4)){
                /*
                 * 同上
                 */
                if(System.currentTimeMillis()-start > time){ break; }
            }
            if(clientSocket.queue.isEmtry(4)){
                return;
            }else{
                //清空
                while(!clientSocket.queue.isEmtry(4)){ clientSocket.queue.read(4); }
                return;
            }
        }catch (Exception e){
            e.printStackTrace();
        }
    }
    
    /**********************************发送消息*************************************/
    public void transfor(int id,int lenToID,int [] toID,String dataType,byte[] data){
        /*
         * 发送事件封装成协议，字段说明如下
         * @ 10: 发送事件标识字段
         * @ id: 客户端id
         * @ lenToID: 目的端个数
         * @ toID: 目的端ID数组
         * @ dataType: data类型
         * @ data: 具体封装的数据
         */
        clientProtocol message = new clientProtocol(10, id, lenToID, toID, dataType, data);
        clientSocket.queue.write(0,message);
    }

    /**********************************获取列表*************************************/
    public List<Map<Integer,String>> getOnlineUsers(int id){
        /*
         * 获取列表事件封装成协议，字段说明如下
         * @ 12: 获取列表事件标识字段
         * @ id: 客户端id
         * @ 1: 目的端只有一个
         * @ new int[]{0}: 为0说明发往服务器端
         * @ 0: data类型为文本
         * @ data: 具体封装的数据
         */
        clientProtocol message = new clientProtocol(12, id, 1, new int[]{0}, 0, "".getBytes());
        clientSocket.queue.write(0, message);
        List<Map<Integer,String>> list = new ArrayList<Map<Integer, String>>();
        //等待服务端处理
        long start = System.currentTimeMillis();
        while(clientSocket.queue.isEmtry(13)){
            /*
             * 同上
             */
            if(System.currentTimeMillis()-start > time){ break; }
        }
        //持续监测id为13的消息队列
        if(clientSocket.queue.isEmtry(13)){
            return null;
        }else{
        	//此处封装的数据为在线用户名
            clientProtocol message1 = clientSocket.queue.read(13);
            //清空
            while(!clientSocket.queue.isEmtry(13)){ clientSocket.queue.read(13); }
            try {
                String[] user = new String(message1.getData(), "UTF-8").split(",");
                for (int i = 0; i < user.length; i++) {
                    Map<Integer,String> map = new HashMap<Integer, String>();
                    // 将user信息分隔为ID+用户名，放入map键值对中，再加入list
                    String[] one_user = user[i].split(" ");
                    map.put(Integer.parseInt(one_user[0]),one_user[1]);
                    list.add(map);
                }
                return list;
            }catch (Exception e){
                e.printStackTrace();
                return null;
            }
        }
    }
}
