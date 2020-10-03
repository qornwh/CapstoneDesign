package com.example.joljak.firebase_modul;

import android.util.Log;

import androidx.annotation.NonNull;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;
import java.util.Map;

public class MyFirebase {

    private static MyFirebase myFirebase = null;
    private FirebaseFirestore firebaseFirestore = null;
    private DocumentReference docRef;

    private MyFirebase(){
        firebaseFirestore = FirebaseFirestore.getInstance();
        docRef = firebaseFirestore.collection("test12").document("test13");
    }

    public static MyFirebase getInstance(){
        if(myFirebase == null){
            myFirebase = new MyFirebase();
        }
        return myFirebase;
    }

    public void writeFirestore_data(Fdata fdata){

        Map<String, Object> updates = new HashMap<>();
        String line = "{"+
                "car="+fdata.getCar()+", "+
                "code="+fdata.getId()+", "+
                "img="+fdata.getImg()+", "+
                "name="+fdata.getName()+", "+
                "phone="+fdata.getPhone()+
                "}";
        Map<String, Object> updates2 = new HashMap<>();
        updates2.put("car", fdata.getCar());
        updates2.put("img", fdata.getImg());
        updates2.put("code", fdata.getId());
        updates2.put("phone", fdata.getPhone());
        updates2.put("name", fdata.getName());
        updates.put(fdata.getImg(), updates2);
        Log.d("하이"+fdata.getImg(), ""+line);

        firebaseFirestore.collection("test12").document("test13").update(updates).addOnCompleteListener(new OnCompleteListener<Void>() {
            @Override
            public void onComplete(@NonNull Task<Void> task) {
                boolean data = task.isSuccessful();
                Log.d("update firestore", "result : "+ data);
            }
        });
    }

    //테스트용
    public boolean readFirestore_data(Fdata fdata){
        docRef.get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>(){
            @Override
            public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                if(task.isSuccessful())
                {
                    DocumentSnapshot document = task.getResult();
                    if(document.exists()){

                        Log.d("read firestore data", "Document data"+document.getData());
                    }
                    else
                    {
                        Log.d("read firestore data failed", "No such data");
                    }
                }
                else
                {
                    Log.d("read firestore", "get failed with", task.getException());
                }
            }
        });

        return false;
    }

    //테스트용
    public Fdata readFirestore_data_privit(final Fdata fdata){
        final Fdata _fdata = new Fdata();;
        docRef.get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>(){
            @Override
            public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                if(task.isSuccessful())
                {
                    DocumentSnapshot document = task.getResult();
                    if(document.exists()){
                        if(document.getData().get(fdata.getName()+fdata.getCar()) == null){
                            Log.d("read firestore data", "Document data no match");
                        }
                        else{
                            String data = document.getData().get(fdata.getName()+fdata.getCar()).toString();
                            data = data.trim();
                            data = data.replaceAll("\\{", "");
                            data = data.replaceAll("\\}", "");
                            String datas[] = data.split(",");

                            _fdata.setId(datas[1].split("=")[1]);
                            _fdata.setCar(datas[2].split("=")[1]);
                            _fdata.setName(datas[4].split("=")[1]);
                            _fdata.setPhone(datas[3].split("=")[1]);

                            Log.d("read firestore data", "Document data"+data);
                        }
                    }
                    else
                    {
                        Log.d("read firestore data failed", "No such data");
                    }
                }
                else
                {
                    Log.d("read firestore", "get failed with", task.getException());
                }
            }
        });

        return _fdata;
    }
}
