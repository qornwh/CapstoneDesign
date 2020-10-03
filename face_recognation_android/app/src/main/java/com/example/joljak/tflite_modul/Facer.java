package com.example.joljak.tflite_modul;

import android.content.Context;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.RectF;
import android.util.Log;
import android.util.SparseArray;

import com.google.android.gms.vision.Frame;
import com.google.android.gms.vision.face.Face;
import com.google.android.gms.vision.face.FaceDetector;

import java.util.ArrayList;

public class Facer {
    private FaceDetector faceDetector;

    public Facer(Context context){
        faceDetector = new FaceDetector.Builder(context).setTrackingEnabled(false).build();
        if(!faceDetector.isOperational()){
            Log.w("warring","no open faceDetector");
        }
    }

    /*
        이 함수의 역할은 캡쳐된 이미지에서
        얼굴을 잘라낸다
     */
    public ArrayList<Bitmap> getFacesBoxs_btimap(Bitmap bitmap, Context context){
        // 주의사항
        // ArrayList 0번에는 원본이미지가 들어간다
        // 그후 1, 2, 3, 순번대로 크롭된 얼굴이미지가 들어간다
        Bitmap myBitmap = bitmap.copy(Bitmap.Config.ARGB_8888, true);
        ArrayList<Bitmap> bitmaps = new ArrayList<>();

        Frame frame = new Frame.Builder().setBitmap(myBitmap).build();
        SparseArray<Face> faces = faceDetector.detect(frame);

        Canvas tempCanvas = new Canvas(myBitmap);
        tempCanvas.drawBitmap(myBitmap, 0, 0, null);
        Paint myRectPaint = new Paint();
        myRectPaint.setStrokeWidth(5);
        myRectPaint.setColor(Color.RED);
        myRectPaint.setStyle(Paint.Style.STROKE);

        boolean _done = bitmaps.add(myBitmap);

        for(int i=0; i<faces.size(); i++) {
            Face thisFace = faces.valueAt(i);
            float x1 = thisFace.getPosition().x;
            float y1 = thisFace.getPosition().y;
            float x2 = x1 + thisFace.getWidth()+1;
            float y2 = y1 + thisFace.getHeight()+1;
            tempCanvas.drawRoundRect(new RectF(x1, y1, x2, y2), 2, 2, myRectPaint);
            boolean _add = bitmaps.add(Bitmap.createBitmap(myBitmap, (int) x1, (int) y1, (int) (x2 - x1), (int) (y2 - y1)));
        }

        Log.i("test bitmap","okok");

        return bitmaps;
    }

}

/*
public ArrayList<Bitmap> getFacesBoxs(String fileName, Context context){
    // 주의사항 이거는 assets폴더의 사진 접근 함수 오버로딩
    // ArrayList 0번에는 원본이미지가 들어간다
    // 그후 1, 2, 3, 순번대로 크롭된 얼굴이미지가 들어간다
    Bitmap myBitmap;
    ArrayList<Bitmap> bitmaps = new ArrayList<>();
    myBitmap = getFromImgAssets(fileName, context);

    Frame frame = new Frame.Builder().setBitmap(myBitmap).build();
    SparseArray<Face> faces = faceDetector.detect(frame);

    Canvas tempCanvas = new Canvas(myBitmap);
    tempCanvas.drawBitmap(myBitmap, 0, 0, null);
    Paint myRectPaint = new Paint();
    myRectPaint.setStrokeWidth(5);
    myRectPaint.setColor(Color.RED);
    myRectPaint.setStyle(Paint.Style.STROKE);

    //이것은 add 리턴값이 존재해서 그냥 boolean 변수에 저장해둠. 안쓰이는 변수이므로 크게 신경 x
    boolean _1 = bitmaps.add(myBitmap);

    for(int i=0; i<faces.size(); i++) {
        Face thisFace = faces.valueAt(i);
        float x1 = thisFace.getPosition().x;
        float y1 = thisFace.getPosition().y;
        float x2 = x1 + thisFace.getWidth();
        float y2 = y1 + thisFace.getHeight();
        tempCanvas.drawRoundRect(new RectF(x1, y1, x2, y2), 2, 2, myRectPaint);
        boolean add = bitmaps.add(Bitmap.createBitmap(myBitmap, (int) x1, (int) y1, (int) (x2 - x1), (int) (y2 - y1)));
    }

    return bitmaps;
}

    public ArrayList<Bitmap> getFacesBoxs(Bitmap bitmap, Context context){
        // 주의사항 이거는 assets폴더의 사진 접근 함수 오버로딩
        // ArrayList 0번에는 원본이미지가 들어간다
        // 그후 1, 2, 3, 순번대로 크롭된 얼굴이미지가 들어간다
        ArrayList<Bitmap> bitmaps = new ArrayList<>();

        Frame frame = new Frame.Builder().setBitmap(bitmap).build();
        SparseArray<Face> faces = faceDetector.detect(frame);

        Canvas tempCanvas = new Canvas(bitmap);
        tempCanvas.drawBitmap(bitmap, 0, 0, null);
        Paint myRectPaint = new Paint();
        myRectPaint.setStrokeWidth(5);
        myRectPaint.setColor(Color.RED);
        myRectPaint.setStyle(Paint.Style.STROKE);

        //이것은 add 리턴값이 존재해서 그냥 boolean 변수에 저장해둠. 안쓰이는 변수이므로 크게 신경 x
        boolean _1 = bitmaps.add(bitmap);

        for(int i=0; i<faces.size(); i++) {
            Face thisFace = faces.valueAt(i);
            float x1 = thisFace.getPosition().x;
            float y1 = thisFace.getPosition().y;
            float x2 = x1 + thisFace.getWidth();
            float y2 = y1 + thisFace.getHeight();
            tempCanvas.drawRoundRect(new RectF(x1, y1, x2, y2), 2, 2, myRectPaint);
            boolean add = bitmaps.add(Bitmap.createBitmap(bitmap, (int) x1, (int) y1, (int) (x2 - x1), (int) (y2 - y1)));
        }

        return bitmaps;
    }


    public FaceDetector getFaceDetector(){
        return faceDetector;
    }

    //에셋에서 파일을 들고오기위한 함수
    //에셋은 폴더
    public Bitmap getFromImgAssets(String fileName, Context context){

        Bitmap bit = null;
        BitmapFactory.Options options = new BitmapFactory.Options();
        options.inMutable=true;

        try {
            AssetManager assetManager = context.getResources().getAssets();
            InputStream inputStream = assetManager.open(fileName);
            bit = BitmapFactory.decodeStream(inputStream, new Rect(), options);
            if (bit == null){
                return null;
            }
            inputStream.close();

        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }

        return bit;
    }
 */