package com.example.joljak.sock_modul;

import android.content.Context;
import android.util.Log;
import android.widget.Toast;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.URLDecoder;
import java.util.logging.Handler;
import java.util.logging.LogRecord;

public class MySock extends Thread{

    private Socket socket;
    private InputStream is;
    private OutputStream os;

    private String my_data;
    private Context context;

    private static String Server_IP = "192.168.137.1";
    private static int Server_PORT = 55555;
    private static int Server_PACKET_SIZE = 1024;

    public MySock(String data, Context context){
        my_data = data;
        this.context = context;
    }

    @Override
    public void run() {
        try {
            socket = new Socket();
            SocketAddress addr = new InetSocketAddress(Server_IP, Server_PORT);
            socket.connect(addr);
            Log.i("Server and Client", "Connect : OK");
            String _data = sendNrecv("phone : "+my_data);
            Log.i("test_Data", "_Data : "+_data);
        } catch (IOException e) {
            e.printStackTrace();
            Log.i("Server and Client", "Connect : ERROR");
        } catch (Exception e){
            e.printStackTrace();
            Log.i("Server and Client", "ERROR");
        }
    }

    public String sendNrecv(String data){
        String _data = "";
        byte[] _bytes = data.getBytes();
        try {
            os = socket.getOutputStream();
            os.write(_bytes);
            byte[] _bytes2 = new byte[Server_PACKET_SIZE];
            is = socket.getInputStream();
            int trem = is.read(_bytes2);
            _data = new String(_bytes2, 0, trem, "UTF-8");
            Log.i("Socket Send data", "send = "+_data);
        } catch (IOException e) {
            e.printStackTrace();
            Log.i("Socket Send data", "sendNrecv : ERROR");
        }
        return _data;
    }
}


