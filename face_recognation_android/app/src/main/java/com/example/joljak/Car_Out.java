package com.example.joljak;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.hardware.Camera;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.telephony.TelephonyManager;
import android.util.Log;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

import com.example.joljak.camera_modul.MyCamera;
import com.example.joljak.firebase_modul.Fdata;
import com.example.joljak.firebase_modul.MyFirebase;
import com.example.joljak.firebase_modul.MyStorage;
import com.example.joljak.phone_modul.Cache;
import com.example.joljak.phone_modul.MyPhone;
import com.example.joljak.tflite_modul.BitmapUtil;
import com.example.joljak.tflite_modul.Facer;
import com.example.joljak.tflite_modul.Tflite_reader;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.lang.reflect.Array;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketAddress;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.util.ArrayList;

public class Car_Out extends AppCompatActivity {

    private EditText EditText_name, EditText_phone, EditText_car_number;
    private Button btn_back, btn_in, btn_capture;
    private ImageView iv;
    private boolean _state = false;

    // tftlite
    private int inputSize = 112;

    // 카메라
    private MyCamera myCamera;
    private Camera.PictureCallback pictureCallback;
    private Bitmap myBitmap;
    private Matrix rotateMatrix;

    //캐시
    private Cache cache;
    private Facer facer;
    Car_Out.MyHandler myHandler = new Car_Out.MyHandler();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car_out);

        EditText_car_number = findViewById(R.id.carout_number);
        EditText_phone = findViewById(R.id.carout_phone);
        EditText_name = findViewById(R.id.carout_name);
        btn_back = findViewById(R.id.carout_back);
        btn_in = findViewById(R.id.carout_in);
        btn_capture = findViewById(R.id.carout_capture);
        iv = findViewById(R.id.carout_sideView);

        facer = new Facer(this);
        cache =  new Cache(this);
        rotateMatrix = new Matrix();
        rotateMatrix.postRotate(270);
        try{
            String _data = cache.Read();
            if(_data == ""){
                Intent intent_main = new Intent(Car_Out.this, Car_Information.class);
                startActivity(intent_main);
                Toast.makeText(this.getApplicationContext(),"정보 등록창으로 이동합니다.", Toast.LENGTH_LONG).show();
            }else{
                String[] _datas = _data.split(",");
                //이름 자동차번호 폰번 코드
                EditText_name.setText(_datas[0].split(" ")[1]);
                EditText_car_number.setText(_datas[1].split(" ")[1]);
                EditText_phone.setText(getPhoneNum());
            }
        }catch (IOException e){
            e.printStackTrace();
        }

        myCamera = new MyCamera(this, (SurfaceView)findViewById(R.id.carout_img));
        btn_capture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                myCamera.getCamera().takePicture(null, null, pictureCallback);
            }
        });

        btn_in.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ArrayList<Bitmap> _bitmaps = facer.getFacesBoxs_btimap(myBitmap, getApplicationContext());
                Bitmap _bitmap = BitmapUtil.resizeSquare(_bitmaps.get(1), inputSize);
                String str1 = Tflite_reader.instance().get_target_N_emb(_bitmap, false);
                Log.i("printf result", ""+str1);
                if(str1 == null || str1 == "unknown") {
                    Toast.makeText(getApplicationContext(), "얼굴인증을 실패했습니다. "+str1, Toast.LENGTH_SHORT).show();
                    btn_capture.setBackgroundColor(0xD3D3D3);
                }else{
                    Toast.makeText(getApplicationContext(), "얼굴인증이 완료되었습니다. "+str1, Toast.LENGTH_SHORT).show();
                    showDialog();
                }
            }
        });

        pictureCallback = new Camera.PictureCallback() {
            @Override
            public void onPictureTaken(byte[] bytes, Camera camera) {
                Bitmap bit = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
                myBitmap = Bitmap.createBitmap(bit, 0,0,bit.getWidth(), bit.getHeight(), rotateMatrix, false);
                Log.i("사이즈", "bit w: "+myBitmap.getWidth()+" h: "+ myBitmap.getHeight());
                _state = true;
                ArrayList<Bitmap> _bits = facer.getFacesBoxs_btimap(myBitmap, getApplicationContext());
                if(_bits.size() > 1){
                    btn_capture.setBackgroundColor(0x5BF44336);
                    iv.setImageBitmap(_bits.get(0));
                    // myBitmap = _bits.get(1);
                    _state = true;
                    btn_in.setEnabled(true);
                }
                myCamera.getCamera().startPreview();
            }
        };

        btn_back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent_main = new Intent(Car_Out.this, MainActivity.class);
                startActivity(intent_main);
            }
        });
    }

    public void intent() {
        final Intent intent = new Intent(Car_Out.this, MainActivity.class);
        startActivity(intent);
    }

    public void showDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(Car_Out.this);
        builder.setTitle("내정보");
        builder.setMessage("자동차를 빼오시겠습니까?");

        builder.setPositiveButton("확인", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                dialogInterface.dismiss();
                //파이썬과 소켓통신 넣기
                BackgroundThread thread = new BackgroundThread(EditText_car_number.getText().toString());
                thread.start();
                long start = System.currentTimeMillis();
                while(true){
                    long end = System.currentTimeMillis();
                    if(end - start > 2000){
                        break;
                    }
                }
                intent();
            }
        });

        builder.setNegativeButton("취소", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                dialogInterface.dismiss();
            }
        });
        builder.show();
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

    //서버와 소켓 통신 스레드
    class BackgroundThread extends Thread{
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
                socket.connect(addr, 1500);
                Log.i("Server and Client", "Connect : OK");
                String _data = sendNrecv("phone : out = "+mydata);
                Log.i("test_Data", "_Data : "+_data);

                val = Integer.parseInt(_data);
                if(val < 100){
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

            }catch (SocketTimeoutException e) {
                Log.d("Socket connect","not connect");

                Bundle bundle = new Bundle();
                bundle.putString("park", "현재 서버와 연결되어 있지 않습니다.");

                Message message = myHandler.obtainMessage();
                message.setData(bundle);

                myHandler.sendMessage(message);
                e.printStackTrace();
            }catch (IOException e) {
                Log.d("Socket connect","not connect");

                Bundle bundle = new Bundle();
                bundle.putString("park", "현재 서버와 연결되어 있지 않습니다.");

                Message message = myHandler.obtainMessage();
                message.setData(bundle);

                myHandler.sendMessage(message);
                e.printStackTrace();
            }catch (Exception e) {
                Log.d("Socket Error","Error");
                e.printStackTrace();
            }finally {
                try{
                    socket.close();
                }catch (IOException e){
                    e.printStackTrace();
                    Log.d("socket","close");
                }
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

    //핸들러
    class MyHandler extends Handler {
        @Override
        public void handleMessage(@NonNull Message msg) {
            super.handleMessage(msg);

            Bundle bundle = msg.getData();
            String _data = bundle.getString("park");

            Toast.makeText(getApplicationContext(), ""+_data, Toast.LENGTH_SHORT).show();
        }
    }
}
