package com.example.joljak.camera_modul;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.hardware.Camera;
import android.os.Environment;
import android.util.Log;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.ViewGroup;

import androidx.annotation.NonNull;

import java.io.IOException;

public class MyCamera implements SurfaceHolder.Callback {

    private Camera camera;
    private SurfaceHolder surfaceHolder;
    private SurfaceView surfaceView;

    public MyCamera(Context context, SurfaceView surfaceView){
        super();

        this.surfaceView = surfaceView;
        surfaceHolder = surfaceView.getHolder();
        surfaceHolder.addCallback(this);
        surfaceHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);
    }

    public Camera getCamera() {
        return camera;
    }

    @Override
    public void surfaceCreated(@NonNull SurfaceHolder surfaceHolder) {
        try{
            camera = Camera.open(1);
        }catch (Exception e){

        }

        Camera.Parameters parameters;
        parameters = camera.getParameters();
//        parameters.setPreviewFrameRate(60);
        parameters.setPreviewSize(1280, 720);
        camera.setParameters(parameters);
        camera.setDisplayOrientation(90);
        try{
            float w = surfaceView.getHeight()*(float)(720.0/1280.0);
            int h = surfaceView.getHeight();
            ViewGroup.LayoutParams Lp = surfaceView.getLayoutParams();
            Lp.width = (int)w;
            Lp.height = h;
            surfaceHolder.setFixedSize((int)w , h);
            surfaceView.setLayoutParams(Lp);
            Log.i("사이즈", "w : "+w+" h : "+surfaceView.getHeight());
            camera.setPreviewDisplay(surfaceHolder);
            camera.startPreview();
        }catch (IOException e){
            e.printStackTrace();
        }
    }

    @Override
    public void surfaceChanged(@NonNull SurfaceHolder surfaceHolder, int i, int i1, int i2) {

    }

    @Override
    public void surfaceDestroyed(@NonNull SurfaceHolder surfaceHolder) {
        camera.stopPreview();
        camera.release();
        camera = null;
    }
}
