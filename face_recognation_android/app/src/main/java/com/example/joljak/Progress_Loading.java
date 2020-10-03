package com.example.joljak;

import android.os.Handler;

import androidx.appcompat.app.AppCompatActivity;

import com.example.joljak.loading_modul.MyLoading;

public class Progress_Loading extends AppCompatActivity {

    public void progressON() {
        MyLoading.getInstance().progressON(this, null);
    }

    public void progressON(String message) {
        MyLoading.getInstance().progressON(this, message);
    }

    public void progressOFF() {
        MyLoading.getInstance().progressOFF();
    }

    public void startProgress() {
        progressON("Loading...");
        new Handler().postDelayed(new Runnable() {
            @Override
            public void run() {
                progressOFF();
            }
        }, 5000);
    }
}