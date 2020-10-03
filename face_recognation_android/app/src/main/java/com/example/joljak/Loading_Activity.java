package com.example.joljak;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
/*
* 로딩창 안씀
* */
public class Loading_Activity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading);
        startLoading();
    }


    private void startLoading() {
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                //---메인이 번저실행 한다면 주석처리 해야 할 부분---
                Intent intent = new Intent(getBaseContext(), MainActivity.class);
                startActivity(intent);
                //----------------------
                finish();
            }
        }, 2000);
    }

}