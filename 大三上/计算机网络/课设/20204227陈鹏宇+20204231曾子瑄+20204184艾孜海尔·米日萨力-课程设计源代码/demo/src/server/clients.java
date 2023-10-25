package server;

/*
 * 客户信息类，包含对象id，用户名，密码，包含读写操作
 * 当一个客户端注册成功后，会在服务端自动生成一个client并加入manager用户管理类中
 * 但一个客户端注销并不会将其删除，因为只要服务端没有关闭，该用户还能通过manager中存储的信息登录进来
 */
public class clients {
    private int id;
    private String name;
    private String password;
    public String getName() { return name; }
    public String getPassword() { return password; }
    public int getId() { return id; }
    public void setName(String name) { this.name = name; }
    public void setPassword(String password) { this.password = password; }
    public void setId(int id) { this.id = id; }
}