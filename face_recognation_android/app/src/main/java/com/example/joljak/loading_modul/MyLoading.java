package com.example.joljak.loading_modul;

import android.app.Activity;
import android.app.Application;
import android.graphics.drawable.ColorDrawable;
import android.text.TextUtils;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatDialog;

import com.bumptech.glide.Glide;
import com.example.joljak.R;

public class MyLoading  extends Application {
    private static MyLoading baseApplication;

    AppCompatDialog progressDialog;

    public static MyLoading getInstance(){
        return  baseApplication;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        baseApplication = this;
    }

    public void progressON(Activity activity, String message){
        if (activity == null || activity.isFinishing()) {
            return;
        }

        if (progressDialog != null && progressDialog.isShowing()) {
            progressSET(message);
        } else {
            progressDialog = new AppCompatDialog(activity);
            progressDialog.setCancelable(false);
            //백그라운드 색상
            progressDialog.getWindow().setBackgroundDrawable(new ColorDrawable(android.graphics.Color.TRANSPARENT));
            //여기서 레이아웃 지정 해줘야 할듯 매개변수로
            progressDialog.setContentView(R.layout.activity_progress_loading);
            progressDialog.show();
        }

        ImageView imageView =(ImageView)progressDialog.findViewById(R.id.progress_image);
        Glide.with(this).load(R.raw.loader).into(imageView);

        TextView textView = (TextView)progressDialog.findViewById(R.id.progress_text);
        if (!TextUtils.isEmpty(message)) {
            textView.setText(message);
        }
    }

    public void progressSET(String message){
        if (progressDialog == null || !progressDialog.isShowing()) {
            return;
        }

        TextView tv_progress_message = (TextView) progressDialog.findViewById(R.id.progress_text);
        if (!TextUtils.isEmpty(message)) {
            tv_progress_message.setText(message);
        }
    }

    public void progressOFF(){
        if (progressDialog != null && progressDialog.isShowing()) {
            progressDialog.dismiss();
        }
    }
}
