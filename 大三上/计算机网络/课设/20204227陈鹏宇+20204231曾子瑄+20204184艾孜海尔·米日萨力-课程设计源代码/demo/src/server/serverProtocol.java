package server;

import client.clientProtocol;

import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Set;


/*
 * ���̶߳���Э��󣬻ᵽ��ģ���Э����н���
 */

//�������Ϣ����
public class serverProtocol {
	// �����û���������û�����
    private static online online = new online();
    private static manager manager = new manager();

    //������Ϣ����������Ϣ�����ش�ת������Ϣ�б�
    public static List<clientProtocol> Parsing(clientProtocol message) throws UnsupportedEncodingException {
        int type = message.getType();
        //��Э������󽫷�����Ϣ�б�
        List<clientProtocol> list = new ArrayList<clientProtocol>();
        /*****************************��¼��Ϣ*****************************/
        if(type == 0) {
        	//��ȡID��Ϣ
            int id = message.getFromID();
            //��ȡ������Ϣ
            String password = new String(message.getData(), "utf-8");
            //��֤�Ƿ���ڸ��û�
            clients trueUser = manager.select(id);
            //��������ڴ��û�������noUser
            if (trueUser == null) {
                /*
                 * ��¼�ظ��¼���װ��Э�飬�ֶ�˵������
                 * @ 3: ��¼�ظ��¼���ʶ�ֶ�
                 * @ 0: ԴIDΪ0��˵���Ƿ���˷��͵���Ϣ
                 * @ 1: Ŀ�Ķ�ֻ��һ��
                 * @ new int[]{id}: Ŀ�Ķ�Ϊid
                 * @ 0: data����Ϊ�ı�
                 * @ data: �����װ�����ݣ��˴�Ϊ"noUser"
                 */
                list.add(new clientProtocol(3, 0, 1, new int[]{id}, 0, "noUser".getBytes("UTF-8")));
                return list;
            }
            //��֤����
            if (trueUser.getPassword().equals(password)) {
            	//��������ȷ�򽫸��û����������û�����
                online.add(id);
                /*
                 * ���˾������ݲ�ͬ�⣬����ͬ��
                 */
                list.add(new clientProtocol(3, 0, 1, new int[]{id}, 0, "success".getBytes("UTF-8")));// ��װ�ظ�Э��
                return list;
            } else {
                list.add(new clientProtocol(3, 0, 1, new int[]{id}, 0, "passwordError".getBytes("UTF-8")));
                return list;
            }
            /*****************************ע����Ϣ*****************************/
        }else if(type == 1) {
            int id = message.getFromID();
            clients trueUser = manager.select(id);
            //�����ڴ��û�
            if (trueUser == null) {
                list.add(new clientProtocol(4, 0, 1, new int[]{id}, 0, "noUser".getBytes("UTF-8")));
                return list;
            }
            //ע���ɹ��������߹������Ƴ�
            online.remove(id);
            /*
             * ע���ظ��¼���װ��Э�飬�ֶ�˵������
             * @ 4: ע���ظ��¼���ʶ�ֶ�
             * @ 0: ԴIDΪ0��˵���Ƿ���˷��͵���Ϣ
             * @ 1: Ŀ�Ķ�ֻ��һ��
             * @ new int[]{id}: Ŀ�Ķ�Ϊid
             * @ 0: data����Ϊ�ı�
             * @ data: �����װ�����ݣ��˴�Ϊ"success"
             */
            list.add(new clientProtocol(4, 0, 1, new int[]{id}, 0, "success".getBytes("UTF-8")));// ��װ�ظ�Э��
            return list;
            /*****************************ע����Ϣ*****************************/
        } else if(type == 2) {
            int id;
            do {
                id = new Random().nextInt(900) + 100;  //�������100-999����������Ϊ�û�����ΨһID
            } while (manager.select(id) != null);
            String data = new String(message.getData(), "utf-8");
            //��Э��data�з�����û���������
            String[] datas = data.split(",");
            String password = datas[1];
            String name = datas[0];
            //�������û����������û�����ģ��
            clients user = new clients();
            user.setId(id);
            user.setName(name);
            user.setPassword(password);
            manager.insert(user);
            //��װ�ظ�Э��
            /*
             * ע��ظ��¼���װ��Э�飬�ֶ�˵������
             * @ 5: ע��ظ��¼���ʶ�ֶ�
             * @ 0: ԴIDΪ0��˵���Ƿ���˷��͵���Ϣ
             * @ 1: Ŀ�Ķ�ֻ��һ��
             * @ new int[]{id}: Ŀ�Ķ�Ϊid
             * @ 0: data����Ϊ�ı�
             * @ data: �����װ�����ݣ��˴�Ϊ"success"
             */
            list.add(new clientProtocol(5, 0, 1, new int[]{id}, 0, "success".getBytes("UTF-8")));
            return list;
            /*****************************������Ϣ*****************************/
        } else if(type == 10){
            int     id = message.getFromID();
            int  toLen = message.getLenToID();
            int[] toID = message.getToID();
            //���ת����
            for(int i = 0; i < toLen; i++){
            	/*
                 * �����¼���װ��Э�飬�ֶ�˵������
                 * @ 11: �����¼���ʶ�ֶ�
                 * @ id: ԴIDΪ�ͻ��˷��ͷ�
                 * @ 1: Ŀ�Ķ�ֻ��һ�������ｫid�б��еĿͻ��˷ֿ�����
                 * @ new int[]{toID[i]}: Ŀ�Ķ�Ϊ����һ��
                 * @ message.getDatatype(): data����
                 * @ message.getData(): �����װ������
                 */
                list.add(new clientProtocol(11, id, 1, new int[]{toID[i]}, message.getDatatype(),message.getData()));
            }
            return list;
            /*****************************��ȡ�����б���Ϣ*****************************/
        }else if(type == 12){
            /*
             * ��ʱdataTypeΪ�����û�������data�洢�����û�ID��������ÿ���û�ͨ��,�ָ�
             * �����ʽΪID1 User1, ID2 User2, ID3 User3�Դ�����
             */
            StringBuffer data = new StringBuffer();
            Set<Integer> set  = online.get();
            for (Integer integer:set){
                data.append(integer);
                data.append(" ");
                data.append(manager.select(integer).getName());
                data.append(",");
            }
            data.deleteCharAt(data.length()-1);
            /*
             * �����б��¼���װ��Э�飬�ֶ�˵������
             * @ 13: �����б��¼���ʶ�ֶ�
             * @ 0: ԴIDΪ�����
             * @ 1: Ŀ�Ķ�ֻ��һ���������������б��
             * @ new int[]{message.getFromID()}: Ŀ�Ķ�
             * @ set.size(): data���ͣ�������庬��Ϊ��������
             * @ data.toString().getBytes("utf-8"): �����û�������Ϣ
             */
            list.add(new clientProtocol(13, 0, 1, new int[]{message.getFromID()}, set.size(),data.toString().getBytes("utf-8")));
            return list;
        }
        //Э�������̬��չ
        return null;
    }
}
