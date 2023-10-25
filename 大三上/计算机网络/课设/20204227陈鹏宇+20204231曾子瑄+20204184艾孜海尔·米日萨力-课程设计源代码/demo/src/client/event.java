package client;

import java.util.*;

/*
 * �¼��������ͻ��˵��÷�װΪЭ�飬����������Э�飬����Զ�̵���
 * ����ע�ᡢ��¼��ע����������Ϣ����ȡ�����û���Ϣ���¼�
 * �����¼������ȷ�װ��Э�飬Ȼ��д��idΪ0����Ϣ�����У�д�߳��ٴ��ж�ȡ���͸������
 */
public class event {
    private static int time = 10000;
    /**********************************ע��*************************************/
    public int register(String name, String password){
        try {
        	// ���õ����û����������װ��data
            byte[] data = (name + "," + password).getBytes("utf-8");
            /*
             * ע���¼���װ��Э�飬�ֶ�˵������
             * @ 2: ע���¼���ʶ�ֶ�
             * @ 0: ��û��ע��ɹ���û�о���id
             * @ 1: Ŀ�Ķ�ֻ��һ��
             * @ new int[]{0}: Ϊ0˵��������������
             * @ 0: data����Ϊ�ı�
             * @ data: �����װ������
             */
            clientProtocol message = new clientProtocol(2, 0, 1, new int[]{0}, 0, data);
            /*
             * ������Ҫд���̷��ͳ�ȥ������Ҫ�ȷ���id = 0����Ϣ������
             */
            clientSocket.queue.write(0,message);
            //�ȴ�����˴���
            long start = System.currentTimeMillis();
            /*
             * �������idΪ5����Ϣ���У����д����ע���Ƿ�ɹ�����Ϣ
             * ΪʲôҪ����ѭ���أ�
             * �������˶�ע��Ĵ�����Ҫʱ�䣬��ȴ�һ��ʱ���ٽ����ж�
             */
            while(clientSocket.queue.isEmtry(5)){ if(System.currentTimeMillis() - start > time){ break; } }// �ȴ�ʱ�����
            
            if(clientSocket.queue.isEmtry(5)) {
                return -1;//-1Ϊע��ʧ�ܣ�ע��ɹ������û���id
            } else {
            	// ��ȡIDΪ5����Ϣ����
                clientProtocol message1 = clientSocket.queue.read(5);
                // ���
                while(!clientSocket.queue.isEmtry(5)){ clientSocket.queue.read(5); }
                // ���ﷵ�ص���ʵ���Ǳ��ͻ��˵�id
                return message1.getToID()[0];
            }
        }catch (Exception e){
            e.printStackTrace();//ע��ʧ��
            return -1;
        }
    }

    /**********************************��¼*************************************/
    public boolean login(int id, String password){
        try {
            byte[] data = password.getBytes("utf-8");
            /*
             * ��¼�¼���װ��Э�飬�ֶ�˵������
             * @ 0: ��¼�¼���ʶ�ֶ�
             * @ id: �ͻ���id
             * @ 1: Ŀ�Ķ�ֻ��һ��
             * @ new int[]{0}: Ϊ0˵��������������
             * @ 0: data����Ϊ�ı�
             * @ data: �����װ�����ݣ��˴�Ϊ������Ϣ
             */
            clientProtocol message = new clientProtocol(0, id, 1, new int[]{0}, 0, data);
            clientSocket.queue.write(0, message);
            //�ȴ�����˴���
            long start = System.currentTimeMillis();
            //�������idΪ3����Ϣ���У������¼�¼��Ķ���
            while(clientSocket.queue.isEmtry(3)){
                /*
                 * ͬ��
                 */
                if(System.currentTimeMillis()-start > time){ break; }
            }
            if(clientSocket.queue.isEmtry(3)){
                return false;
            } else {
            	// �������˻᷵�ص�¼�Ƿ�ɹ�
                clientProtocol message1 = clientSocket.queue.read(3);
                // ���
                while(!clientSocket.queue.isEmtry(3)){ clientSocket.queue.read(3); }
                if(new String(message1.getData(),"utf-8").equals("success")){ return true; }
                return false;
            }
        }catch (Exception e){
            e.printStackTrace();
            return false;
        }
    }

    /**********************************ע��*************************************/
    public void unlogin(int id, String password){
        try {
            byte[] data = password.getBytes("utf-8");
            /*
             * ע���¼���װ��Э�飬�ֶ�˵������
             * @ 1: ע���¼���ʶ�ֶ�
             * @ id: �ͻ���id
             * @ 1: Ŀ�Ķ�ֻ��һ��
             * @ new int[]{0}: Ϊ0˵��������������
             * @ 0: data����Ϊ�ı�
             * @ data: �����װ�����ݣ��˴�Ϊ������Ϣ
             */
            clientProtocol message = new clientProtocol(1, id, 1, new int[]{0}, 0, data);
            clientSocket.queue.write(0,message);
            //�ȴ�����˴���
            long start = System.currentTimeMillis();
            while(clientSocket.queue.isEmtry(4)){
                /*
                 * ͬ��
                 */
                if(System.currentTimeMillis()-start > time){ break; }
            }
            if(clientSocket.queue.isEmtry(4)){
                return;
            }else{
                //���
                while(!clientSocket.queue.isEmtry(4)){ clientSocket.queue.read(4); }
                return;
            }
        }catch (Exception e){
            e.printStackTrace();
        }
    }
    
    /**********************************������Ϣ*************************************/
    public void transfor(int id,int lenToID,int [] toID,String dataType,byte[] data){
        /*
         * �����¼���װ��Э�飬�ֶ�˵������
         * @ 10: �����¼���ʶ�ֶ�
         * @ id: �ͻ���id
         * @ lenToID: Ŀ�Ķ˸���
         * @ toID: Ŀ�Ķ�ID����
         * @ dataType: data����
         * @ data: �����װ������
         */
        clientProtocol message = new clientProtocol(10, id, lenToID, toID, dataType, data);
        clientSocket.queue.write(0,message);
    }

    /**********************************��ȡ�б�*************************************/
    public List<Map<Integer,String>> getOnlineUsers(int id){
        /*
         * ��ȡ�б��¼���װ��Э�飬�ֶ�˵������
         * @ 12: ��ȡ�б��¼���ʶ�ֶ�
         * @ id: �ͻ���id
         * @ 1: Ŀ�Ķ�ֻ��һ��
         * @ new int[]{0}: Ϊ0˵��������������
         * @ 0: data����Ϊ�ı�
         * @ data: �����װ������
         */
        clientProtocol message = new clientProtocol(12, id, 1, new int[]{0}, 0, "".getBytes());
        clientSocket.queue.write(0, message);
        List<Map<Integer,String>> list = new ArrayList<Map<Integer, String>>();
        //�ȴ�����˴���
        long start = System.currentTimeMillis();
        while(clientSocket.queue.isEmtry(13)){
            /*
             * ͬ��
             */
            if(System.currentTimeMillis()-start > time){ break; }
        }
        //�������idΪ13����Ϣ����
        if(clientSocket.queue.isEmtry(13)){
            return null;
        }else{
        	//�˴���װ������Ϊ�����û���
            clientProtocol message1 = clientSocket.queue.read(13);
            //���
            while(!clientSocket.queue.isEmtry(13)){ clientSocket.queue.read(13); }
            try {
                String[] user = new String(message1.getData(), "UTF-8").split(",");
                for (int i = 0; i < user.length; i++) {
                    Map<Integer,String> map = new HashMap<Integer, String>();
                    // ��user��Ϣ�ָ�ΪID+�û���������map��ֵ���У��ټ���list
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
