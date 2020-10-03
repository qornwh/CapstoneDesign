package com.example.joljak.firebase_modul;

public class Fdata {
    private String name;
    private String id;
    private String car;
    private String img;
    private String phone;

    public Fdata(String name, String id, String car, String img, String phone) {
        this.name = name;
        this.id = id;
        this.car = car;
        this.img = img;
        this.phone = phone;
    }

    public Fdata() {
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getCar() {
        return car;
    }

    public void setCar(String car) {
        this.car = car;
    }

    public String getImg() {
        return img;
    }

    public void setImg(String img) {
        this.img = img;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
