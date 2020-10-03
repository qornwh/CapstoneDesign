package com.example.joljak;

import android.annotation.SuppressLint;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.hardware.Camera;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
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
import com.example.joljak.util_modul.MyBitmap;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;

public class Car_Information extends Progress_Loading {

    EditText EditText_name, EditText_car_number, EditText_phone;
    //이름,차 번호, 폰번호
    Button input_button, out_button, btncapture;
    ImageView iv;
    private boolean _state = false;

    private Facer facer;
    private final int inputSize = 112;

    // 카메라
    private MyCamera myCamera;
    private Camera.PictureCallback pictureCallback;
    private Bitmap myBitmap;
    private Matrix rotateMatrix;

    //캐시
    private Cache cache;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_car_information);

        // xml
        EditText_name = findViewById(R.id.EditText_name);
        EditText_car_number = findViewById(R.id.EditText_car_number);
        EditText_phone = findViewById(R.id.EditText_phone);
        input_button = findViewById(R.id.input_button);
        out_button = findViewById(R.id.out_button);
        iv = findViewById(R.id.sideView);
        btncapture = findViewById(R.id.b_capture);

        EditText_phone.setText(getPhoneNum());
        rotateMatrix = new Matrix();
        rotateMatrix.postRotate(270);

        cache = new Cache(this);
        facer = new Facer(this);

        input_button.setEnabled(false);

        try{
            String _data = cache.Read();
            Log.d("cache read", "data : "+_data);
            if(_data != ""){
                String[] _datas = _data.split(",");
                //이름 자동차번호 폰번 코드
                EditText_name.setText(_datas[0].split(" ")[1]);
                EditText_car_number.setText(_datas[1].split(" ")[1]);
            }
        }catch (IOException e){
            e.printStackTrace();
        }

        myCamera = new MyCamera(this, (SurfaceView)findViewById(R.id.c_face));
        btncapture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                myCamera.getCamera().takePicture(null, null, pictureCallback);
            }
        });

        input_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                showDialog();
            }
        });

        pictureCallback = new Camera.PictureCallback() {
            @Override
            public void onPictureTaken(byte[] bytes, Camera camera) {

                Bitmap bit = BitmapFactory.decodeByteArray(bytes, 0, bytes.length);
                myBitmap = Bitmap.createBitmap(bit, 0,0,bit.getWidth(), bit.getHeight(), rotateMatrix, false);
                Log.i("사이즈", "bit w: "+myBitmap.getWidth()+" h: "+ myBitmap.getHeight());
                ArrayList<Bitmap> _bits = facer.getFacesBoxs_btimap(myBitmap, getApplicationContext());
                if(_bits.size() > 1){
                    btncapture.setBackgroundColor(0x5BF44336);
                    iv.setImageBitmap(_bits.get(0));
                    // myBitmap = _bits.get(1);
                    _state = true;
                    input_button.setEnabled(true);
                }
                myCamera.getCamera().startPreview();
            }
        };

        out_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent_main = new Intent(Car_Information.this, MainActivity.class);
                startActivity(intent_main);
            }
        });
    }

    public void intent() {
        final Intent intent = new Intent(Car_Information.this, MainActivity.class);
        startActivity(intent);
    }

    public void showDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(Car_Information.this);
        builder.setTitle("내정보");
        builder.setMessage("저장 하시겠습니까?");

        builder.setPositiveButton("확인", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialogInterface, int i) {
                dialogInterface.dismiss();
                startProgress();
                Fdata fdata = new Fdata();
                fdata.setName(EditText_name.getText().toString());
                fdata.setPhone(EditText_phone.getText().toString());
                fdata.setCar(EditText_car_number.getText().toString());
                fdata.setImg(EditText_name.getText().toString()+EditText_car_number.getText().toString());
                fdata.setId("1234");
                MyFirebase.getInstance().writeFirestore_data(fdata);
                String _data = "" +
                        "name " + fdata.getName()+",\r\n"+
                        "car_number " + fdata.getCar();
                try{
                    Log.d("cache write", "data : "+_data);
                    cache.Write(_data);
                }catch (IOException e){
                    e.printStackTrace();
                }
                Upload2(fdata, myBitmap, MyStorage.getInstance().getStorageRef());
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
    //파이어베이스 스토리지 이미지 추가
    public void Upload2(Fdata fdata, Bitmap bitmap, StorageReference storageRef){
        StorageReference imageRef = storageRef.child("test1/"+fdata.getName()+fdata.getCar()+".jpg");
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 60, baos);
        byte[] data = baos.toByteArray();

        Log.d("byte stream", "data : "+data.length);

        UploadTask uploadTask = imageRef.putBytes(data);

        uploadTask.addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Log.d("storage failed","onFailure");
                progressOFF();
            }
        }).addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
            @Override
            public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {
                Log.d("storage success and update cache","onSuccess");
                updateCache(EditText_name.getText().toString());
                progressOFF();
                intent();
            }
        });
    }

    private void updateCache(String name){
        MyBitmap.myImages = facer.getFacesBoxs_btimap(myBitmap,getApplicationContext());
        if(MyBitmap.myImages.size()>1){
            Bitmap _bit = BitmapUtil.resizeSquare(MyBitmap.myImages.get(1), inputSize);
            Tflite_reader.instance().set_recoginzeImage(_bit,false,MyBitmap.myName);
            Toast.makeText(getApplicationContext(), "기존 정보 수신완료 ", Toast.LENGTH_SHORT).show();
        }
        else{
            Toast.makeText(getApplicationContext(), "기존 캐시를 지우고 다시 실행시켜 주세요.", Toast.LENGTH_SHORT).show();
        }
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