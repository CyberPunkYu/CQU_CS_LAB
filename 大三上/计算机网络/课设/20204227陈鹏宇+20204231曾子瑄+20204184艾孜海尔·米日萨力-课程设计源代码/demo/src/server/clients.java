package server;

/*
 * �ͻ���Ϣ�࣬��������id���û��������룬������д����
 * ��һ���ͻ���ע��ɹ��󣬻��ڷ�����Զ�����һ��client������manager�û���������
 * ��һ���ͻ���ע�������Ὣ��ɾ������ΪֻҪ�����û�йرգ����û�����ͨ��manager�д洢����Ϣ��¼����
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