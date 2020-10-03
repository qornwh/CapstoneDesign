package com.example.joljak.tflite_modul;

import android.content.Context;
import android.content.res.AssetFileDescriptor;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.os.Trace;
import android.util.Log;
import android.util.Pair;

import org.tensorflow.lite.Interpreter;

import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.HashMap;
import java.util.Map;

public class Tflite_reader {

    private ByteBuffer imgData;
    private int[] intValues;
    //임베딩길이 192
    private static final int OUTPUT_SIZE = 192;
    private int inputSize;
    // Float model
    private static final float IMAGE_MEAN = 128.0f;
    private static final float IMAGE_STD = 128.0f;
    private boolean isModelQuantized = false;
    private float[][] embeedings;
    private HashMap<String, float[]> embeedings_models;
    public Interpreter tfLite;

    private int numBytesPerChannel = 4;

    private static Tflite_reader tflite_reader = null;

    /*
    텐서플로우 라이트 초기화
    모든것은 instance함수로 접근
    처음만 매개변수를 넘기고 쓰고 생성된 후에는
    매개변수가 없는 아래의 함수를 사용하면 됨.
     */
    public static Tflite_reader instance(Context context, String modelFilename, int inputSize) throws IOException{
        if(tflite_reader == null){
            Log.v("create","tflite !!!");
            tflite_reader = new Tflite_reader(context, modelFilename, inputSize);
            Log.v("create","tflite instance create !!!");
        }
        return tflite_reader;
    }

    //tflite_reader객체가 생성된 후에 사용
    public static Tflite_reader instance(){
        if(tflite_reader == null){
            Log.w("Worring","tflite instance not create!!!");
        }
        return tflite_reader;
    }

    /*
    실제 텐서플로우 라이트 생성자 부분
    나도 잘모름
    intValues          : 들어올 이미지 사이즈는 112 * 112로 무조권 바꾸어 넣는다
    imgData            : 실제로 들어오는 이미지는 1 * 112 * 112 * 3 * 4 이므로 그것을 저장할 버퍼
    embeedings_models  : 초기에 이미지를 텐서라이트로 연산후 결과값을 저장할 배열 객체
    Interpreter        : 텐서플로우라이트 객체를 생성할 핵심
     */
    private Tflite_reader(Context context, String modelFilename, int inputSize) throws IOException {
        this.inputSize = inputSize;
        intValues = new int[inputSize * inputSize];
        imgData = ByteBuffer.allocateDirect(1 * inputSize * inputSize * 3 * numBytesPerChannel);
        imgData.order(ByteOrder.nativeOrder());
        embeedings_models = new HashMap<>();
        AssetManager assetManager = context.getAssets();

        tfLite = new Interpreter(loadModelFile(assetManager, modelFilename));
    }

    private static MappedByteBuffer loadModelFile(AssetManager assets, String modelFilename)
            throws IOException {
        AssetFileDescriptor fileDescriptor = assets.openFd(modelFilename);
        FileInputStream inputStream = new FileInputStream(fileDescriptor.getFileDescriptor());
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = fileDescriptor.getStartOffset();
        long declaredLength = fileDescriptor.getDeclaredLength();
        return fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
    }

    /*
    이 함수는 매칭시킬 초기에 이미지들을 텐서플로우라이트로 연산후 결과값을
    embeedings변수에 저장한다
     */
    public void set_recoginzeImage(final Bitmap bitmap, boolean storeExtra, String name){

        bitmap.getPixels(intValues, 0, bitmap.getWidth(), 0, 0, bitmap.getWidth(), bitmap.getHeight());

        imgData.rewind();
        for (int i = 0; i < inputSize; ++i) {
            for (int j = 0; j < inputSize; ++j) {
                int pixelValue = intValues[i * inputSize + j];
                if (isModelQuantized) {
                    // Quantized model
                    imgData.put((byte) ((pixelValue >> 16) & 0xFF));
                    imgData.put((byte) ((pixelValue >> 8) & 0xFF));
                    imgData.put((byte) (pixelValue & 0xFF));
                } else { // Float model
                    imgData.putFloat((((pixelValue >> 16) & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                    imgData.putFloat((((pixelValue >> 8) & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                    imgData.putFloat(((pixelValue & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                }
            }
        }

        Object[] inputArray = {imgData};
        Map<Integer, Object> outputMap = new HashMap<>();

        embeedings = new float[1][OUTPUT_SIZE];
        outputMap.put(0, embeedings);

        Trace.beginSection("run");
        tfLite.runForMultipleInputsOutputs(inputArray, outputMap);
        Trace.endSection();

        embeedings_models.put(name, embeedings[0]);

        Log.v("msg",name+" : 입력완료");
    }

    /*
    이 함수는 매칭될 이미지 즉 캡쳐된 사진 이미지를 텐서라이트로 연산후 결과값을
    embeedings변수에 저장된 값과 비교해
    맞는지 아닌지 출력하는 함수
     */
    public String get_target_N_emb(final Bitmap bitmap, boolean storeExtra){

        bitmap.getPixels(intValues, 0, bitmap.getWidth(), 0, 0, bitmap.getWidth(), bitmap.getHeight());

        imgData.rewind();
        for (int i = 0; i < inputSize; ++i) {
            for (int j = 0; j < inputSize; ++j) {
                int pixelValue = intValues[i * inputSize + j];
                if (isModelQuantized) {
                    // Quantized model
                    imgData.put((byte) ((pixelValue >> 16) & 0xFF));
                    imgData.put((byte) ((pixelValue >> 8) & 0xFF));
                    imgData.put((byte) (pixelValue & 0xFF));
                } else { // Float model
                    imgData.putFloat((((pixelValue >> 16) & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                    imgData.putFloat((((pixelValue >> 8) & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                    imgData.putFloat(((pixelValue & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
                }
            }
        }

        Object[] inputArray = {imgData};
        Map<Integer, Object> outputMap = new HashMap<>();

        embeedings = new float[1][OUTPUT_SIZE];
        outputMap.put(0, embeedings);

        tfLite.runForMultipleInputsOutputs(inputArray, outputMap);

        Pair<String, Float> data = findNearest(embeedings[0]);

        //1보다 크면 맞지 않기 때문에
        if(data.second > 1.0){
            Log.v("msg","매칭 실패");
            String _data = "unknown";
            return _data;
        }

        Log.v("msg",data.first+" = 비교완료");

        if(data == null){
            Log.v("get_target_N_emb","no match data!!!");

            return null;
        }
        else if(data != null){
            Log.v("get_target_N_emb",data.first+" : "+ data.second);
            String _data = data.first+" : "+ data.second;
            return _data;
        }

        return null;
    }

    // embeedings변수와 캡쳐된 이미지값과 비교하는 함수 for문으로 반복하면서 비교
    private Pair<String, Float> findNearest(float[] emb) {

        Pair<String, Float> ret = null;
        for (Map.Entry<String, float[]> entry : embeedings_models.entrySet()) {
            final String name = entry.getKey();
            final float[] knownEmb = entry.getValue();

            float distance = 0;
            for (int i = 0; i < emb.length; i++) {
                float diff = emb[i] - knownEmb[i];
                distance += diff*diff;
            }
            distance = (float) Math.sqrt(distance);
            if (ret == null || distance < ret.second) {
                ret = new Pair<>(name, distance);
            }
        }

        return ret;
    }
}

// 임베딩 층이 192인 이유는
// 입력의 길이는 112
// 임베딩 차원을 192로 설정한것 같다.
// 그래서 특징을 192개로 나눈거일 수 있다? 아직 모르겟다
//
// 예시
//# 문장 토큰화와 단어 토큰화
//        text=[['Hope', 'to', 'see', 'you', 'soon'],['Nice', 'to', 'see', 'you', 'again']]
//
//        # 각 단어에 대한 정수 인코딩
//        text=[[0, 1, 2, 3, 4],[5, 1, 2, 3, 6]]
//
//        # 위 데이터가 아래의 임베딩 층의 입력이 된다.
//        Embedding(7, 2, input_length=5)
//        # 7은 단어의 개수. 즉, 단어 집합(vocabulary)의 크기이다.
//        # 2는 임베딩한 후의 벡터의 크기이다.
//        # 5는 각 입력 시퀀스의 길이. 즉, input_length이다.
//
//        # 각 정수는 아래의 테이블의 인덱스로 사용되며 Embeddig()은 각 단어에 대해 임베딩 벡터를 리턴한다.
//        +------------+------------+
//        |   index    | embedding  |
//        +------------+------------+
//        |     0      | [1.2, 3.1] |
//        |     1      | [0.1, 4.2] |
//        |     2      | [1.0, 3.1] |
//        |     3      | [0.3, 2.1] |
//        |     4      | [2.2, 1.4] |
//        |     5      | [0.7, 1.7] |
//        |     6      | [4.1, 2.0] |
//        +------------+------------+
//        # 위의 표는 임베딩 벡터가 된 결과를 예로서 정리한 것이고 Embedding()의 출력인 3D 텐서를 보여주는 것이 아님.


