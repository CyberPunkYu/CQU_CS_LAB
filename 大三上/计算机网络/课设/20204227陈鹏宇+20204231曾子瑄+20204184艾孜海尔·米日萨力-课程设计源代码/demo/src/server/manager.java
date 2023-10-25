package server;

import java.util.HashMap;
import java.util.Map;

//用户信息管理，用于增删改查用户id，用户名和密码
public class manager {
    private static Map<Integer, clients> map = new HashMap<Integer, clients>();
    public clients select(int id){ return map.get(id); }
    public void delete(int id){ map.remove(id); }
    public void update(clients user){ map.remove(user.getId()); map.put(user.getId(),user); }
    public void insert(clients user){ map.putIfAbsent(user.getId(), user); }
}