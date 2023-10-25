package server;

import java.util.HashSet;
import java.util.Set;

// 客户在线人数管理，基于Set，保证不会重复加入
public class online {
    private static Set<Integer> list = new HashSet<Integer>();
    public void add(int id){ list.add(id); }
    public Set<Integer> get(){ return list; }
    public void remove(int id){ list.remove(id); }
}