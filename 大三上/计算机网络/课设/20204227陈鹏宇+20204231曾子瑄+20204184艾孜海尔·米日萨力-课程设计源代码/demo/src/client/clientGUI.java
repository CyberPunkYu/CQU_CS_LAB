package client;

import javax.swing.*;
import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.File;
import java.io.FileOutputStream;
import java.nio.file.Files;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.List;

/*
 * GUI����û��ʲô�ý��ģ���Ҫ��������������
 * һ���Ƕ���Ϣ���н��̣������ڽ���������һֱѭ������Ƿ��ȡ������Ϣ��ֱ������˳�
 * ����һ����ˢ�½��̣�ʵ��ԭ��ܼ򵥣�����ÿ��һ��ʱ��10s���»�ȡ���߿ͻ���������ʾ
 * GUI�������¼����Ĳ�������event.java�йأ����з�װ�����е��¼�
 * ******************����*******************
 * 1. Ϊ�˷����û�����������ע�Ṧ�ܣ����û���תΪΨһ������ID
 * 2. �����ַ���ˢ�������û��б�һ�����¹رմ��������µ㿪���ֶ�ˢ�£������߳��Զ�ˢ�£�ÿ��10sˢ��һ��
 */

public class clientGUI {
    private static event event = new event();
    private static int id = -1; //��¼���ȡID
    private static String passwords = "";
    private static boolean isFile = false;
    private static File selectFile = null;
    //�߳��첽��ֹ
    private static volatile boolean exit = false;

    public static void runGUI(String ip, int port){
//    	System.out.println(ip);
        //------------------������¼����----------------------
        JFrame frame = new JFrame();
        frame.setTitle("Login");//����
        frame.setSize(400,200);//�����С
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE );//�ر�ʱ�Զ��˳�
        frame.setResizable(true);//���ô�С�ɱ�
        frame.setLocationRelativeTo(null);//���þ�����ʾ

        JLabel user = new JLabel(" ID :");
        JLabel password =  new JLabel("Password:");

        JTextField userTF = new JTextField(10);
        JPasswordField pwdTF = new JPasswordField(10);

        JButton okB =  new JButton("Login");
        JButton noB =  new JButton("Register");
        // ��¼�¼����
        okB.addActionListener(e->{
        	
            boolean isLogin = event.login(Integer.parseInt(userTF.getText()),String.valueOf(pwdTF.getPassword()));
            System.out.println(isLogin);
            if(isLogin){
                frame.dispose();
                id = Integer.parseInt(userTF.getText());
                passwords = String.valueOf(pwdTF.getPassword());
                String title = new String("��������ϵͳ-----IP: " + ip + " PORT: " + port);
                mainWindow(title);
            }else{
                JOptionPane.showMessageDialog(null, "��½ʧ�ܣ�����ID������", "��¼ʧ��", JOptionPane.ERROR_MESSAGE);
            }
        });

        // ���ע������ע�����
        noB.addActionListener(e1->{
            JFrame frame1 = new JFrame();
            frame1.setTitle("Register");//����
            frame1.setSize(280,180);//�����С
            frame1.setResizable(true);//���ô�С�ɱ�
            frame1.setLocationRelativeTo(null);//���þ�����ʾ

            JPanel s1 = new JPanel();
            JPanel z1 = new JPanel();
            JPanel x1 = new JPanel();

            JLabel user1 = new JLabel("User Name:");
            JLabel password1 =  new JLabel("Password:");

            JTextField userTF1 = new JTextField(10);
            JTextField pwdTF1 = new JTextField(10);

            JButton okB1 =  new JButton("Register");

            //����ϰ�ߣ������в�����壬����в������
            frame1.setLayout(new BorderLayout());
            frame1.add(s1,BorderLayout.NORTH );
            frame1.add(z1, BorderLayout.CENTER );
            frame1.add(x1,BorderLayout.SOUTH);

            s1.add(user1);
            s1.add(userTF1);
            z1.add(password1);
            z1.add(pwdTF1);
            x1.add(okB1);

            //���ô���ɼ���
            frame1.setVisible(true);
            okB1.addActionListener(e2-> {
                int isRegister = event.register(userTF1.getText(),pwdTF1.getText());
                if (isRegister>0) {
                    JOptionPane.showInternalMessageDialog(null, "IDΪ"+String.valueOf(isRegister),"ע��ɹ�", JOptionPane.INFORMATION_MESSAGE);
                    frame1.dispose();
                } else {
                    JOptionPane.showMessageDialog(null, "ע��ʧ��", "ע��ʧ��", JOptionPane.ERROR_MESSAGE);
                    frame1.dispose();
                }
            });
        });

        JPanel s = new JPanel();
        JPanel z = new JPanel();
        JPanel x = new JPanel();
        //����ϰ�ߣ������в�����壬����в������
        frame.setLayout(new BorderLayout());
        frame.add(s,BorderLayout.NORTH );
        frame.add(z, BorderLayout.CENTER );
        frame.add(x,BorderLayout.SOUTH);

        s.add(user);
        s.add(userTF);
        z.add(password);
        z.add(pwdTF);
        x.add(okB);
        x.add(noB);
        //���ô���ɼ���
        frame.setVisible(true);
    }

    	
    public static void mainWindow(String title){
        JFrame jFrame = new JFrame();
        jFrame.setTitle(title);
        jFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE );
        jFrame.setResizable(true);

        //�ر��¼�
        jFrame.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                super.windowClosing(e);
                //��ֹreadThread��writeThread��readQueueThread�߳�
                //������Ϣ���еļ���
                exit = true;
                //����ע����Ϣ
                event.unlogin(id,passwords);
            }
        });


        //���ʹ���
        JPanel jPanel1 = new JPanel();
        JTextArea input = new JTextArea(2, 27);
        input.setFont(new Font("�꿬��", Font.BOLD, 14));
        jPanel1.add(new JScrollPane(input));

        //���մ���
        JPanel jPanel2 = new JPanel();
        JTextArea output = new JTextArea(12,36);
        output.setFont(new Font("�꿬��", Font.BOLD, 14));
        output.append("--------------------------------------�������--------------------------------------\n");
        output.setEditable(false);
        JScrollPane jScrollPane = new JScrollPane(output);

        //�����ܵ���Ϣ�����߳̿���
        Thread readQueueThread = new Thread(new Runnable(){
            public void run() {
                try {
                    while (true) {
                        if(exit){
                            return;
                        }
                        //һ���ȡһ�Σ�����CPU����
                        Thread.sleep(1000);
                        //����type=11��Э�飬������ڣ������
                        while (clientSocket.queue.isEmtry(11)) { };
                        clientProtocol message = clientSocket.queue.read(11);
                        if (message != null && message.getData()!=null) {
                            if (message.getDataTypeString().equals("0")) {
                                SimpleDateFormat sdf = new SimpleDateFormat();// ��ʽ��ʱ�� 
                                sdf.applyPattern("yyyy-MM-dd HH:mm:ss a");// aΪam/pm�ı��  
                                Date date = new Date();
                                output.append(sdf.format(date) + "\n");
                                output.append(Integer.toString(message.getFromID()) + ": " + new String(message.getData(),"utf-8") + "\n");
                                output.append("\n");
                            }else if(message.getDataTypeString().equalsIgnoreCase("jpg") ||
                                    message.getDataTypeString().equalsIgnoreCase("png") ||
                                    message.getDataTypeString().equalsIgnoreCase("jpeg") ||
                                    message.getDataTypeString().equalsIgnoreCase("bmp")){
                                output.append(Integer.toString(message.getFromID()) + "������ͼƬ" + "\n");
                                String fileName = Integer.toString(message.getFromID()) + "Rec" +
                                        Long.toString(System.currentTimeMillis()) +"."+ message.getDataTypeString();
                                String BASE_DIR = new String("C:\\Users\\111\\Desktop\\");
                                BASE_DIR = BASE_DIR + Integer.toString(message.getToID()[0]);
                                File dic = new File(BASE_DIR);
                                dic.mkdirs();
                                File file = new File(BASE_DIR + "\\" + fileName);                                
                                FileOutputStream fileOutputStream = new FileOutputStream(file);
                                fileOutputStream.write(message.getData());
                                fileOutputStream.close();
                            }else{
                                output.append(Integer.toString(message.getFromID()) + "�������ļ�" + "\n");
                                String fileName = Integer.toString(message.getFromID()) + "Rec" +
                                        Long.toString(System.currentTimeMillis()) +"."+ message.getDataTypeString();
                                String BASE_DIR = new String("C:\\Users\\111\\Desktop\\");
                                BASE_DIR = BASE_DIR + Integer.toString(message.getToID()[0]);
                                File dic = new File(BASE_DIR);
                                dic.mkdirs();
                                File file = new File(BASE_DIR + "\\" + fileName);
                                FileOutputStream fileOutputStream = new FileOutputStream(file);
                                fileOutputStream.write(message.getData());
                                fileOutputStream.close();
                            }
                        }
                    }
                }catch (Exception e){
                    e.printStackTrace();
                }
            }
        });
        readQueueThread.start();

        //�������Զ���λ�����һ��
        jScrollPane.getViewport().setViewPosition(new Point(0, jScrollPane.getVerticalScrollBar().getMaximum()));
        jPanel2.add(jScrollPane);
        //��ť��
        JPanel jPanel4 = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton jButton1 = new JButton("����");
        jButton1.setPreferredSize(new java.awt.Dimension(60,40));
        //������ťִ�еķ���
        jButton1.addActionListener(e -> {
            //�����µĴ���
            JFrame frame = new JFrame("��ѡ�����");
            JPanel panel = new JPanel();
            //������������Ϣ��临ѡ��
            List<Map<Integer,String>> listx = event.getOnlineUsers(id);
            int onlineUserConut = listx.size();
            panel.setLayout(new GridLayout(onlineUserConut+1,1,100,20));
            JCheckBox[] jCheckBoxes = new JCheckBox[onlineUserConut];

            int j = 0;
            for (Map<Integer,String> map:listx){
                for(Map.Entry<Integer,String> entry:map.entrySet()){
                    jCheckBoxes[j] = new JCheckBox("user:" + entry.getValue() + " " + Integer.toString(entry.getKey()));
                    panel.add(jCheckBoxes[j]);
                }
                j++;
            }

            //���䰴ť
            JButton jButton = new JButton("����");

            jButton.addActionListener(e1 ->{
                try {
                    byte[] bytes = null;
                    //��ȡ input ��ֵ
                    String inputTest = input.getText();
                    //�жϴ������ͣ�����byte
                    String type = "0";
                    if (isFile) {
                        if (selectFile == null) {
                            //�������ļ�
                            throw new RuntimeException();
                        } else {
                            int index = selectFile.getName().lastIndexOf(".");
                            if (index == -1) {
                                type = "";
                            }
                            String houZhui = selectFile.getName().substring(index + 1);
                            if (houZhui.equalsIgnoreCase("jpg") ||
                                    houZhui.equalsIgnoreCase("png") ||
                                    houZhui.equalsIgnoreCase("jpeg") ||
                                    houZhui.equalsIgnoreCase("bmp")) {
                                type = houZhui;
                            } else {
                                type = houZhui;
                            }
                            bytes = Files.readAllBytes(selectFile.toPath());
                        }
                    }else {
                        bytes = inputTest.getBytes("utf-8");
                    }
                    //��ȡ���ն���

                    List<Integer> toLDlist = new ArrayList<Integer>();
                    //��ȡ ��ѡ���ֵ
                    for (int i = 0; i < jCheckBoxes.length; i++) {
                        if (jCheckBoxes[i].isSelected()) {
                            //��ѡ�����ݣ�name id
                            toLDlist.add(Integer.parseInt(jCheckBoxes[i].getText().split(" ")[1]));
                        }
                        ;
                    }
                    //��װΪ����
                    int[] toID = new int[toLDlist.size()];
                    int lentoID = 0;
                    for (Integer integer : toLDlist) {
                        toID[lentoID] = integer;
                        lentoID++;
                        System.out.println("���Ͷ���IDΪ�� " + integer);
                    }

                    if(lentoID<=0){ throw new RuntimeException(); }

                    //����Event.transfor��������
                    event.transfor(id,lentoID,toID,type,bytes);

                    //�ر���jFrame
                    frame.dispose();
                    SimpleDateFormat sdf = new SimpleDateFormat();// ��ʽ��ʱ�� 
                    sdf.applyPattern("yyyy-MM-dd HH:mm:ss a");// aΪam/pm�ı��  
                    Date date = new Date();
                    output.append(sdf.format(date) + "\n");
                    output.append("��: " + inputTest + "\n");
                    input.setText("");
                    jScrollPane.getViewport().setViewPosition(new Point(0, jScrollPane.getVerticalScrollBar().getMaximum()));
                    input.setEditable(true);
                    isFile = false;
                    selectFile = null;
                }catch (Exception e5){
                    e5.printStackTrace();
                    frame.dispose();
                    output.append("����ʧ��\n");
                    input.setText("");
                    input.setEditable(true);
                    isFile = false;
                    selectFile = null;
                }
            });
            
            panel.add(jButton);
            frame.add(new JScrollPane(panel));
            frame.setLocation(100, 50);
            frame.setSize(100, 500);
            frame.setVisible(true);
        });

//        jPanel4.add(jButton1);
        //����ļ���ͼƬ
        ImageIcon icon = new ImageIcon("C:\\JAVA\\demo\\src\\image\\file1.png");
        JButton jButton4 = new JButton(icon);
        jButton4.setOpaque(false);//���ÿؼ��Ƿ�͸����trueΪ��͸����falseΪ͸��
        jButton4.setContentAreaFilled(false);//����ͼƬ������ť���ڵ�����
        jButton4.setMargin(new Insets(100, 0, 0, 0));//���ð�ť�߿�ͱ�ǩ����֮��ľ���
        jButton4.setFocusPainted(false);//���������ť�ǲ��ǻ�ý���
        jButton4.setBorderPainted(false);//�����Ƿ���Ʊ߿�
        jButton4.setBorder(null);//���ñ߿�

        jButton4.addActionListener(e2 -> {
            JFileChooser jfc=new JFileChooser();
            jfc.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES );
            jfc.showDialog(new JLabel(), "ѡ��");
            File file=jfc.getSelectedFile();
            if(file!=null) {
                input.setText(file.getAbsolutePath());
                //������������ļ�λ
                input.setEditable(false);
                isFile = true;
                selectFile = file;
            }
        });
        jPanel4.add(jButton4);
        
//        JButton jButton5 = new JButton("�����û�");
        ImageIcon icon5 = new ImageIcon("C:\\JAVA\\demo\\src\\image\\list3.png");
        JButton jButton5 = new JButton(icon5);
        jButton5.setOpaque(false);//���ÿؼ��Ƿ�͸����trueΪ��͸����falseΪ͸��
        jButton5.setContentAreaFilled(false);//����ͼƬ������ť���ڵ�����
        jButton5.setMargin(new Insets(0, 0, 0, 0));//���ð�ť�߿�ͱ�ǩ����֮��ľ���
        jButton5.setFocusPainted(false);//���������ť�ǲ��ǻ�ý���
        jButton5.setBorderPainted(false);//�����Ƿ���Ʊ߿�
        jButton5.setBorder(null);//���ñ߿�
        jButton5.addActionListener(e3 ->{
        	JFrame jFrame5 = new JFrame();
            jFrame5.setTitle("�����û��б�");
            jFrame5.setResizable(true);

            //��ʾ����
            JPanel jPanel5 = new JPanel();
            JTextArea online5 = new JTextArea(20,12);
            online5.setEditable(true);
            //��ȡ�����û��б�
            online5.setText("������������������������������������������������������������������������������������\n");
            online5.setFont(new Font("�꿬��", Font.BOLD, 15));
            online5.setEditable(false);
            List<Map<Integer,String>> list = event.getOnlineUsers(id);
            if(list.size() > 0) {
                for (Map<Integer, String> map : list) {
                    for (Map.Entry<Integer, String> entry : map.entrySet()) {
                        online5.append("�û��� " + entry.getValue());
                        online5.append("\n������������������������������������������������������������������������������������\n");
                    }
                }
            }
		    Thread flushThread = new Thread(new Runnable(){
		    	public void run() {
		    		try {
		    			while (true) {
		    				if (exit) { return; }
		                    Thread.sleep(10000);//����CPU����
		                    //��ȡ�����û��б�
		                    online5.setText("������������������������������������������������������������������������������������\n");
		                    online5.setFont(new Font("�꿬��", Font.BOLD, 15));
		                    online5.setEditable(false);
		                    List<Map<Integer,String>> list = event.getOnlineUsers(id);
		                    if(list.size()>0) {
		                        for (Map<Integer, String> map : list) {
		                            for (Map.Entry<Integer, String> entry : map.entrySet()) {
		                                online5.append("�û��� " + entry.getValue());
		                                online5.append("\n������������������������������������������������������������������������������������\n");
		                            }
		                        }
		                    }
		                }
		            }catch (Exception e){
		                e.printStackTrace();
		            }
		        }
		    });
		    flushThread.start();
            jPanel5.add(new JScrollPane(online5,ScrollPaneConstants.VERTICAL_SCROLLBAR_ALWAYS,ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER));
            jFrame5.setLayout(new BorderLayout());
            jFrame5.add(jPanel5, BorderLayout.CENTER);
            jFrame5.setSize(250, 500);
            jFrame5.setVisible(true);
            
        });
        
        jPanel4.add(jButton5);
        JPanel jPane3 = new JPanel();
        jPanel1.add(jButton1);
        jPane3.setLayout(new BorderLayout());
        jPane3.add(jPanel4,BorderLayout.CENTER);//���ܴ���
        jPane3.add(jPanel2,BorderLayout.NORTH); //���ʹ���
        jPane3.add(jPanel1,BorderLayout.SOUTH); //���Ͱ�ť
        jFrame.add(jPane3);
        jFrame.setSize(500, 400);
        jFrame.setVisible(true);
    }
}
