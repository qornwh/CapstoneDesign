import os, sys
import crypto
sys.modules['Crypto'] = crypto
from firebase import Firebase
import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Firepy:
    def __init__(self):
        __projectId = 'test1-517a7'
        self.config = {
            "apiKey": "AIzaSyCUpy7KkQinLDnxdsLKvw3s8VblEdun-YQ",
            "authDomain": __projectId+".firebaseapp.com",
            "databaseURL": "https://test1.firebaseio.com",
            "storageBucket": __projectId+".appspot.com",
            "serviceAccount": "known/test1-517a7-firebase-adminsdk-qaeyq-5518e3a988.json"
        }
        self.firebase = Firebase(self.config)
        self.storage = self.firebase.storage()
        cred = credentials.Certificate("known/test1-517a7-firebase-adminsdk-qaeyq-5518e3a988.json")
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def load_list_data(self):
        _data = self.db.collection(u'test12').document(u'test13')
        _list = _data.get()
        return _list.to_dict()

    def load_firestore(self, name, car):
        _str = name+car
        _data = self.db.collection(u'test12').document(u'test13')
        _list = _data.get()
        return _list.to_dict()[_str]

    def load_storge(self, path, imgPath):
        self.storage.child(path).download(imgPath)

    def load_list_firestore(self):
        _data = self.storage.child('test1/').list_files()
        return _data
#
# if __name__ == "__main__":
#     firepy = Firepy()
#     try:
#         all_files = firepy.load_list_firestore()
#         for file in all_files:
#             _filename = str(file.name).split("/")[1].lower()
#             try:
#                 print(_filename)
#                 firepy.load_storge(file.name, "./known/"+_filename)
#             except Exception as e:
#                 print(str(e))
#                 print('Download Failed')
#                 #print(str(firepy.load_firestore('류성민','')))
#     except KeyError as key:
#         print('error : ',str(key))
#     except Exception as e:
#         print('error e : ',str(e))
