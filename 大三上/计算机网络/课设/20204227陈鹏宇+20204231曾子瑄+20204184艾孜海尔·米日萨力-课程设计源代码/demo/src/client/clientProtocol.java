package client;
import java.io.Serializable;

/*
 * Э�飬����Э��ļ�ƣ�����Э����ͨ�ż����˫�����빲ͬ��ӵ�һ��Լ����
 * ����ô���������ӡ���ô������ʶ��ȡ�ֻ���������Լ���������֮������໥ͨ�Ž�����
 * ������Ҫ���ǣ��﷨�����塢ʱ��
 * �Զ���Ӧ�ò�Э�飬���пͻ��˺ͷ���˵�ͨ�Ŷ�����Э��
 * 
 * �﷨����Ҫ�ṹ����
 * Э�����͡�ԴID��Ŀ��ID������Ŀ��ID���顢�������͡������ֶ�
 * Э�����;������£�
 * 0 Ϊ��¼����      1 Ϊע������   2 Ϊע������
 * 3,4,5Ϊ����˻ظ�����¼/ע��/ע��    �ɹ�/ʧ��
 * 10 Ϊ������Ϣ���� 11 Ϊ��Ϣ�ظ�(�ͻ����յ�����Ϣtype)  
 * 12Ϊ��ȡ�����û�����  13 Ϊ�����û�״̬�ظ� 100 Ϊ�쳣�ظ�
 * ���壺
 * ��Э���ʹ�ó�����Ҫ�漰����C/Sͨ�ŵ��¼����磺��¼����¼�ظ���ע�ᣬע��ظ���
 * ʱ��û�����̫���ӣ���Ҫ��ÿ������󣬽��շ������뷢�ͷ����лظ���
 */

public class clientProtocol implements Serializable {
	private static final long serialVersionUID = 1L;
	public clientProtocol(){}
    public clientProtocol(int type,int sourceID,int lenToID,int[] destinID,int datatype,byte[] data){
        this.type=type;//����
        this.sourceID=sourceID;//����ID
        this.lenToID=lenToID;//Ŀ��ID����
        this.destinID=destinID;//Ŀ��ID����
        this.datatype=String.valueOf(datatype);//�������� 0Ϊ�ı�
        this.data=data;//���������
    }
    public clientProtocol(int type,int sourceID,int lenToID,int[] destinID,String datatype,byte[] data){
        this.type=type;
        this.sourceID=sourceID;
        this.lenToID=lenToID;
        this.destinID=destinID;
        this.datatype=datatype;
        this.data=data;
    }

    private int type; 
    private int sourceID;//���Ƿ���˻ظ����Ϊ 0
    private int lenToID;
    private int[] destinID;
    private String datatype;
    private byte[] data;
    /*Э���д����*/
    public byte[] getData() { return data; }
    public String getDatatype() { return datatype; }
    public int getFromID() { return sourceID; }
    public int getLenToID() { return lenToID; }
    public int getType() { return type; }
    public int[] getToID() { return destinID; }
    public void setData(byte[] data) { this.data = data; }
    public void setDatatype(int datatype) { this.datatype = String.valueOf(datatype); }
    public void setDatatype(String datatype) { this.datatype = datatype; }
    public void setFromID(int sourceID) { this.sourceID = sourceID; }
    public void setLenToID(int lenToID) { this.lenToID = lenToID; }
    public void setToID(int[] destinID) { this.destinID = destinID; }
    public void setType(int type) { this.type = type; }
    public String getDataTypeString(){ return datatype; }
}
