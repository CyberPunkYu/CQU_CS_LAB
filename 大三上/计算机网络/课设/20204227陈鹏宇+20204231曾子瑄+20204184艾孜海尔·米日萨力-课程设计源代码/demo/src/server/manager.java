package server;

import java.util.HashMap;
import java.util.Map;

//�û���Ϣ����������ɾ�Ĳ��û�id���û���������
public class manager {
    private static Map<Integer, clients> map = new HashMap<Integer, clients>();
    public clients select(int id){ return map.get(id); }
    public void delete(int id){ map.remove(id); }
    public void update(clients user){ map.remove(user.getId()); map.put(user.getId(),user); }
    public void insert(clients user){ map.putIfAbsent(user.getId(), user); }
}