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
 * GUI部分没有什么好讲的，主要新增了两个进程
 * 一个是读消息队列进程，当窗口建立后开启，一直循环检测是否读取到新信息，直到点击退出
 * 还有一个是刷新进程，实现原理很简单，就是每隔一段时间10s重新获取在线客户名单并显示
 * GUI中所有事件监测的操作都和event.java有关，其中封装了所有的事件
 * ******************亮点*******************
 * 1. 为了方便用户名管理，采用注册功能，将用户名转为唯一的整型ID
 * 2. 有两种方法刷新在线用户列表，一是重新关闭窗口再重新点开，手动刷新，二是线程自动刷新，每隔10s刷新一次
 */

public class clientGUI {
    private static event event = new event();
    private static int id = -1; //登录后获取ID
    private static String passwords = "";
    private static boolean isFile = false;
    private static File selectFile = null;
    //线程异步终止
    private static volatile boolean exit = false;

    public static void runGUI(String ip, int port){
//    	System.out.println(ip);
        //------------------创建登录界面----------------------
        JFrame frame = new JFrame();
        frame.setTitle("Login");//标题
        frame.setSize(400,200);//窗体大小
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE );//关闭时自动退出
        frame.setResizable(true);//设置大小可变
        frame.setLocationRelativeTo(null);//设置居中显示

        JLabel user = new JLabel(" ID :");
        JLabel password =  new JLabel("Password:");

        JTextField userTF = new JTextField(10);
        JPasswordField pwdTF = new JPasswordField(10);

        JButton okB =  new JButton("Login");
        JButton noB =  new JButton("Register");
        // 登录事件监测
        okB.addActionListener(e->{
        	
            boolean isLogin = event.login(Integer.parseInt(userTF.getText()),String.valueOf(pwdTF.getPassword()));
            System.out.println(isLogin);
            if(isLogin){
                frame.dispose();
                id = Integer.parseInt(userTF.getText());
                passwords = String.valueOf(pwdTF.getPassword());
                String title = new String("多人聊天系统-----IP: " + ip + " PORT: " + port);
                mainWindow(title);
            }else{
                JOptionPane.showMessageDialog(null, "登陆失败！请检测ID和密码", "登录失败", JOptionPane.ERROR_MESSAGE);
            }
        });

        // 点击注册生成注册界面
        noB.addActionListener(e1->{
            JFrame frame1 = new JFrame();
            frame1.setTitle("Register");//标题
            frame1.setSize(280,180);//窗体大小
            frame1.setResizable(true);//设置大小可变
            frame1.setLocationRelativeTo(null);//设置居中显示

            JPanel s1 = new JPanel();
            JPanel z1 = new JPanel();
            JPanel x1 = new JPanel();

            JLabel user1 = new JLabel("User Name:");
            JLabel password1 =  new JLabel("Password:");

            JTextField userTF1 = new JTextField(10);
            JTextField pwdTF1 = new JTextField(10);

            JButton okB1 =  new JButton("Register");

            //布局习惯：窗体中布局面板，面板中布局组件
            frame1.setLayout(new BorderLayout());
            frame1.add(s1,BorderLayout.NORTH );
            frame1.add(z1, BorderLayout.CENTER );
            frame1.add(x1,BorderLayout.SOUTH);

            s1.add(user1);
            s1.add(userTF1);
            z1.add(password1);
            z1.add(pwdTF1);
            x1.add(okB1);

            //设置窗体可见性
            frame1.setVisible(true);
            okB1.addActionListener(e2-> {
                int isRegister = event.register(userTF1.getText(),pwdTF1.getText());
                if (isRegister>0) {
                    JOptionPane.showInternalMessageDialog(null, "ID为"+String.valueOf(isRegister),"注册成功", JOptionPane.INFORMATION_MESSAGE);
                    frame1.dispose();
                } else {
                    JOptionPane.showMessageDialog(null, "注册失败", "注册失败", JOptionPane.ERROR_MESSAGE);
                    frame1.dispose();
                }
            });
        });

        JPanel s = new JPanel();
        JPanel z = new JPanel();
        JPanel x = new JPanel();
        //布局习惯：窗体中布局面板，面板中布局组件
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
        //设置窗体可见性
        frame.setVisible(true);
    }

    	
    public static void mainWindow(String title){
        JFrame jFrame = new JFrame();
        jFrame.setTitle(title);
        jFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE );
        jFrame.setResizable(true);

        //关闭事件
        jFrame.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                super.windowClosing(e);
                //终止readThread，writeThread，readQueueThread线程
                //结束消息队列的监听
                exit = true;
                //发送注销信息
                event.unlogin(id,passwords);
            }
        });


        //发送窗口
        JPanel jPanel1 = new JPanel();
        JTextArea input = new JTextArea(2, 27);
        input.setFont(new Font("标楷体", Font.BOLD, 14));
        jPanel1.add(new JScrollPane(input));

        //接收窗口
        JPanel jPanel2 = new JPanel();
        JTextArea output = new JTextArea(12,36);
        output.setFont(new Font("标楷体", Font.BOLD, 14));
        output.append("--------------------------------------聊天界面--------------------------------------\n");
        output.setEditable(false);
        JScrollPane jScrollPane = new JScrollPane(output);

        //读接受到消息队列线程开启
        Thread readQueueThread = new Thread(new Runnable(){
            public void run() {
                try {
                    while (true) {
                        if(exit){
                            return;
                        }
                        //一秒读取一次，减轻CPU负载
                        Thread.sleep(1000);
                        //监听type=11的协议，如果存在，则接受
                        while (clientSocket.queue.isEmtry(11)) { };
                        clientProtocol message = clientSocket.queue.read(11);
                        if (message != null && message.getData()!=null) {
                            if (message.getDataTypeString().equals("0")) {
                                SimpleDateFormat sdf = new SimpleDateFormat();// 格式化时间 
                                sdf.applyPattern("yyyy-MM-dd HH:mm:ss a");// a为am/pm的标记  
                                Date date = new Date();
                                output.append(sdf.format(date) + "\n");
                                output.append(Integer.toString(message.getFromID()) + ": " + new String(message.getData(),"utf-8") + "\n");
                                output.append("\n");
                            }else if(message.getDataTypeString().equalsIgnoreCase("jpg") ||
                                    message.getDataTypeString().equalsIgnoreCase("png") ||
                                    message.getDataTypeString().equalsIgnoreCase("jpeg") ||
                                    message.getDataTypeString().equalsIgnoreCase("bmp")){
                                output.append(Integer.toString(message.getFromID()) + "发送了图片" + "\n");
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
                                output.append(Integer.toString(message.getFromID()) + "发送了文件" + "\n");
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

        //下拉框自动定位到最后一行
        jScrollPane.getViewport().setViewPosition(new Point(0, jScrollPane.getVerticalScrollBar().getMaximum()));
        jPanel2.add(jScrollPane);
        //按钮板
        JPanel jPanel4 = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton jButton1 = new JButton("发送");
        jButton1.setPreferredSize(new java.awt.Dimension(60,40));
        //单击按钮执行的方法
        jButton1.addActionListener(e -> {
            //创建新的窗口
            JFrame frame = new JFrame("请选择对象");
            JPanel panel = new JPanel();
            //根据在线人信息填充复选框
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

            //传输按钮
            JButton jButton = new JButton("发送");

            jButton.addActionListener(e1 ->{
                try {
                    byte[] bytes = null;
                    //读取 input 的值
                    String inputTest = input.getText();
                    //判断传输类型，生成byte
                    String type = "0";
                    if (isFile) {
                        if (selectFile == null) {
                            //不存在文件
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
                    //获取接收对象

                    List<Integer> toLDlist = new ArrayList<Integer>();
                    //读取 复选框的值
                    for (int i = 0; i < jCheckBoxes.length; i++) {
                        if (jCheckBoxes[i].isSelected()) {
                            //复选框内容：name id
                            toLDlist.add(Integer.parseInt(jCheckBoxes[i].getText().split(" ")[1]));
                        }
                        ;
                    }
                    //封装为数组
                    int[] toID = new int[toLDlist.size()];
                    int lentoID = 0;
                    for (Integer integer : toLDlist) {
                        toID[lentoID] = integer;
                        lentoID++;
                        System.out.println("发送对象ID为： " + integer);
                    }

                    if(lentoID<=0){ throw new RuntimeException(); }

                    //调用Event.transfor传输数据
                    event.transfor(id,lentoID,toID,type,bytes);

                    //关闭子jFrame
                    frame.dispose();
                    SimpleDateFormat sdf = new SimpleDateFormat();// 格式化时间 
                    sdf.applyPattern("yyyy-MM-dd HH:mm:ss a");// a为am/pm的标记  
                    Date date = new Date();
                    output.append(sdf.format(date) + "\n");
                    output.append("我: " + inputTest + "\n");
                    input.setText("");
                    jScrollPane.getViewport().setViewPosition(new Point(0, jScrollPane.getVerticalScrollBar().getMaximum()));
                    input.setEditable(true);
                    isFile = false;
                    selectFile = null;
                }catch (Exception e5){
                    e5.printStackTrace();
                    frame.dispose();
                    output.append("发送失败\n");
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
        //添加文件和图片
        ImageIcon icon = new ImageIcon("C:\\JAVA\\demo\\src\\image\\file1.png");
        JButton jButton4 = new JButton(icon);
        jButton4.setOpaque(false);//设置控件是否透明，true为不透明，false为透明
        jButton4.setContentAreaFilled(false);//设置图片填满按钮所在的区域
        jButton4.setMargin(new Insets(100, 0, 0, 0));//设置按钮边框和标签文字之间的距离
        jButton4.setFocusPainted(false);//设置这个按钮是不是获得焦点
        jButton4.setBorderPainted(false);//设置是否绘制边框
        jButton4.setBorder(null);//设置边框

        jButton4.addActionListener(e2 -> {
            JFileChooser jfc=new JFileChooser();
            jfc.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES );
            jfc.showDialog(new JLabel(), "选择");
            File file=jfc.getSelectedFile();
            if(file!=null) {
                input.setText(file.getAbsolutePath());
                //锁定输入框，置文件位
                input.setEditable(false);
                isFile = true;
                selectFile = file;
            }
        });
        jPanel4.add(jButton4);
        
//        JButton jButton5 = new JButton("在线用户");
        ImageIcon icon5 = new ImageIcon("C:\\JAVA\\demo\\src\\image\\list3.png");
        JButton jButton5 = new JButton(icon5);
        jButton5.setOpaque(false);//设置控件是否透明，true为不透明，false为透明
        jButton5.setContentAreaFilled(false);//设置图片填满按钮所在的区域
        jButton5.setMargin(new Insets(0, 0, 0, 0));//设置按钮边框和标签文字之间的距离
        jButton5.setFocusPainted(false);//设置这个按钮是不是获得焦点
        jButton5.setBorderPainted(false);//设置是否绘制边框
        jButton5.setBorder(null);//设置边框
        jButton5.addActionListener(e3 ->{
        	JFrame jFrame5 = new JFrame();
            jFrame5.setTitle("在线用户列表");
            jFrame5.setResizable(true);

            //显示窗口
            JPanel jPanel5 = new JPanel();
            JTextArea online5 = new JTextArea(20,12);
            online5.setEditable(true);
            //获取在线用户列表
            online5.setText("——————————————————————————————————————————\n");
            online5.setFont(new Font("标楷体", Font.BOLD, 15));
            online5.setEditable(false);
            List<Map<Integer,String>> list = event.getOnlineUsers(id);
            if(list.size() > 0) {
                for (Map<Integer, String> map : list) {
                    for (Map.Entry<Integer, String> entry : map.entrySet()) {
                        online5.append("用户： " + entry.getValue());
                        online5.append("\n——————————————————————————————————————————\n");
                    }
                }
            }
		    Thread flushThread = new Thread(new Runnable(){
		    	public void run() {
		    		try {
		    			while (true) {
		    				if (exit) { return; }
		                    Thread.sleep(10000);//减轻CPU负载
		                    //获取在线用户列表
		                    online5.setText("——————————————————————————————————————————\n");
		                    online5.setFont(new Font("标楷体", Font.BOLD, 15));
		                    online5.setEditable(false);
		                    List<Map<Integer,String>> list = event.getOnlineUsers(id);
		                    if(list.size()>0) {
		                        for (Map<Integer, String> map : list) {
		                            for (Map.Entry<Integer, String> entry : map.entrySet()) {
		                                online5.append("用户： " + entry.getValue());
		                                online5.append("\n——————————————————————————————————————————\n");
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
        jPane3.add(jPanel4,BorderLayout.CENTER);//接受窗口
        jPane3.add(jPanel2,BorderLayout.NORTH); //发送窗口
        jPane3.add(jPanel1,BorderLayout.SOUTH); //发送按钮
        jFrame.add(jPane3);
        jFrame.setSize(500, 400);
        jFrame.setVisible(true);
    }
}
