package com.example.joljak.firebase_modul;

import android.graphics.Bitmap;
import android.net.Uri;
import android.util.Log;

import androidx.annotation.NonNull;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.io.ByteArrayOutputStream;

public class MyStorage {

    private static MyStorage myStorage;
    FirebaseStorage storage;
    StorageReference storageRef;
    StorageReference mountainsRef;

    private MyStorage(){
        storage = FirebaseStorage.getInstance();
        storageRef = storage.getReference();
        mountainsRef = storageRef.child("test1");
    }

    public static MyStorage getInstance(){
        if(myStorage ==null){
            myStorage = new MyStorage();
        }
        return myStorage;
    }

    public StorageReference getStorageRef(){
        return storageRef;
    }

    //테스트용
    public void Upload(Fdata fdata, Bitmap bitmap){
        StorageReference imageRef = storageRef.child("test1/"+fdata.getName()+fdata.getCar()+".jpg");
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos);
        byte[] data = baos.toByteArray();

        Log.d("byte stream", "data : "+data.length);

        UploadTask uploadTask = imageRef.putBytes(data);

        uploadTask.addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Log.d("storage failed","onFailure");
            }
        }).addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
            @Override
            public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {
                Log.d("storage success","onSuccess");
            }
        });
    }

    //테스트용
    private void download(String name){
        StorageReference islandRef = storageRef.child("test1/"+name+".jpg");

        final long ONE_MEGABYTE = 1024 * 1024;
        islandRef.getBytes(ONE_MEGABYTE).addOnSuccessListener(new OnSuccessListener<byte[]>() {
            @Override
            public void onSuccess(byte[] bytes) {
                // Data for "images/island.jpg" is returns, use this as needed
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception exception) {
                // Handle any errors
            }
        });
    }
}
