package com.example.joljak;


import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;


import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.example.joljak.firebase_modul.MyStorage;
import com.example.joljak.phone_modul.Cache;
import com.example.joljak.phone_modul.MyPhone;
import com.example.joljak.tflite_modul.BitmapUtil;
import com.example.joljak.tflite_modul.Facer;
import com.example.joljak.tflite_modul.Tflite_reader;
import com.example.joljak.util_modul.MyBitmap;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.storage.StorageReference;
import com.gun0912.tedpermission.PermissionListener;
import com.gun0912.tedpermission.TedPermission;

import java.io.IOException;
import java.util.ArrayList;


public class MainActivity extends Progress_Loading {

    Button m_input,m_car_out,m_personal;
    Cache cache;
    Facer facer;

    private Bitmap myBytes;
    private final int inputSize = 112;

    public SharedPreferences pref;
    private static boolean _first_data = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        boolean first = _first_data;

        //findViewById :xml파일 id@ 찾음
        m_input=findViewById(R.id.m_input);
        m_car_out=findViewById(R.id.m_car_out);
        m_personal=findViewById(R.id.m_personal);

        facer = new Facer(this);
        cache = new Cache(this);

        //Loading
        startProgress();

        //tensorflow loding
        try{
            //input size 112
            Tflite_reader tflite_reader = Tflite_reader.instance(this, "mobile_face_net.tflite", 112);
            Log.w("tflite","created");
        } catch (Exception e){
            Log.w("Exception",""+e.toString());
            Log.w("tflite Exception","loding error");
            Toast.makeText(getApplicationContext(), "model file read failed : rebuild please", Toast.LENGTH_SHORT).show();
        }

        if(!first){
            m_input.setEnabled(false);
            m_car_out.setEnabled(false);
            m_personal.setEnabled(false);

            TedPermission.with(getApplicationContext())
                    .setPermissionListener(permissionListener)
                    .setRationaleMessage("카메라 권한이 필요합니다.")
                    .setDeniedMessage("거부하셨습니다.")
                    .setPermissions(Manifest.permission.WRITE_EXTERNAL_STORAGE, Manifest.permission.CAMERA, Manifest.permission.READ_PHONE_STATE)
                    .check();
            try {
                String _data = cache.Read();
                if(_data == "" || _data == null || _data.length() < 1){
                    Toast.makeText(this.getApplicationContext(),"기존 정보 없음.", Toast.LENGTH_SHORT).show();
                    m_input.setEnabled(true);
                    progressOFF();
                }else{
                    String[] _datas = _data.split(",");
                    //이름 자동차번호 폰번 코드
                    String name = _datas[0].split(" ")[1];
                    String car = _datas[1].split(" ")[1];
                    String phone = getPhoneNum();
                    //이제 사진을 들고오고 정보를 저장한다.
                    MyBitmap.myName = name;
                    Toast.makeText(getApplicationContext(), "기존 정보 수신중 ... ", Toast.LENGTH_SHORT).show();
                    download(name+car, MyStorage.getInstance().getStorageRef());
                }
            } catch (IOException e) {
                progressOFF();
                e.printStackTrace();
            }
            MainActivity._first_data = true;
        }
        else{
            progressOFF();
        }

        //차입력 버튼 눌렸을 경우
        m_input.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent=new Intent(MainActivity.this,Car_Information.class);
                startActivity(intent);
            }
        });
        //개인정보 버튼 눌렸을 경우
        m_personal.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent_inf=new Intent(MainActivity.this,Car_Info.class);
                startActivity(intent_inf);
            }
        });

        m_car_out.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent_car_out=new Intent(MainActivity.this, Car_Out.class);
                startActivity(intent_car_out);
            }
        });
    }

    PermissionListener permissionListener = new PermissionListener() {
        @Override
        public void onPermissionGranted() {
            Toast.makeText(getApplicationContext(), "권한이 허용됨", Toast.LENGTH_SHORT).show();
        }

        @Override
        public void onPermissionDenied(ArrayList<String> deniedPermissions) {
            Toast.makeText(getApplicationContext(), "권한이 거부됨", Toast.LENGTH_SHORT).show();
            finishAffinity();
            System.runFinalization();
            System.exit(0);
        }
    };

    private void download(String name,StorageReference storageRef){
        StorageReference islandRef = storageRef.child("test1/"+name+".jpg");

        final long ONE_MEGABYTE = 1024 * 1024;
        islandRef.getBytes(ONE_MEGABYTE).addOnSuccessListener(new OnSuccessListener<byte[]>() {
            @Override
            public void onSuccess(byte[] bytes) {
                myBytes = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
                MyBitmap.myImages = facer.getFacesBoxs_btimap(myBytes, getApplicationContext());

                if(MyBitmap.myImages.size()>1){
                    Bitmap _bit = BitmapUtil.resizeSquare(MyBitmap.myImages.get(1), inputSize);
                    Tflite_reader.instance().set_recoginzeImage(_bit,false,MyBitmap.myName);
                    m_input.setEnabled(true);
                    m_car_out.setEnabled(true);
                    m_personal.setEnabled(true);
                    Toast.makeText(getApplicationContext(), "기존 정보 수신완료 ", Toast.LENGTH_SHORT).show();
                }
                else{
                    Toast.makeText(getApplicationContext(), "기존 캐시를 지우고 다시 실행시켜 주세요.", Toast.LENGTH_SHORT).show();
                }
                progressOFF();
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception exception) {
                Toast.makeText(getApplicationContext(), "기존 정보 수신실패 ", Toast.LENGTH_SHORT).show();
                progressOFF();
            }
        });
    }

    @SuppressLint({"MissingPermission", "HardwareIds"})
    public String getPhoneNum() {
        TelephonyManager tm = (TelephonyManager) getSystemService(this.TELEPHONY_SERVICE);
        String my_phone_num = tm.getLine1Number();
        if (my_phone_num != null) {
            my_phone_num = my_phone_num.replace("+82", "0");
        }
        MyPhone.setMy_phone(my_phone_num);

        return my_phone_num;
    }
}

  /*  class BackgroundThread extends Thread{
        String mydata = "";
        int val = 0;

        private String Server_IP = "192.168.137.1";
        private int Server_PORT = 55555;
        private int Server_PACKET_SIZE = 1024;

        private Socket socket;
        private InputStream is;
        private OutputStream os;

        public BackgroundThread(){

        }

        public BackgroundThread(String _data){
            mydata = _data;
        }

        @Override
        public void run() {
            socket = new Socket();
            SocketAddress addr = new InetSocketAddress(Server_IP, Server_PORT);
            try {
                socket.connect(addr);
                Log.i("Server and Client", "Connect : OK");
                String _data = sendNrecv("phone : out = 12치1234");
                Log.i("test_Data", "_Data : "+_data);

                val = Integer.parseInt(_data);
                if(val > 300){
                    Bundle bundle = new Bundle();
                    bundle.putString("park", "자동차를 빼오기 시작합니다.");

                    Message message = myHandler.obtainMessage();
                    message.setData(bundle);

                    myHandler.sendMessage(message);
                }else if(val == -34){
                    Bundle bundle = new Bundle();
                    bundle.putString("park", "이미 자동차가 나오고 있습니다.");

                    Message message = myHandler.obtainMessage();
                    message.setData(bundle);

                    myHandler.sendMessage(message);
                }else{
                    Bundle bundle = new Bundle();
                    bundle.putString("park", "현재 자동차가 주차되어 있지 않습니다.");

                    Message message = myHandler.obtainMessage();
                    message.setData(bundle);

                    myHandler.sendMessage(message);
                }

            } catch (IOException e) {
                e.printStackTrace();
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

    class MyHandler extends Handler{
        Context mContext;
        @Override
        public void handleMessage(@NonNull Message msg) {
            super.handleMessage(msg);

            Bundle bundle = msg.getData();
            String _data = bundle.getString("park");

            Toast.makeText(getApplicationContext(), ""+_data, Toast.LENGTH_SHORT).show();
        }
    }*/