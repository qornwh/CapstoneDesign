import pymongo
import time
from pprint import pprint

class box():

    def __init__(self, id = str(time.strftime('%Y-%m-%d', time.localtime(time.time()))), data ='123'):
        self.connection = pymongo.MongoClient('localhost', 27017)

        self.db = self.connection.mytest1
        self.collection = self.db.test01
        self.doc_name = id
        self.doc_value = data

        _doc = self.db_find(self, id, data)
        if(_doc == None):
            self.db_document(self, id, data)
            print("Create document")

    #문서 찾기
    @staticmethod
    def db_find(self, id, data):
        _docs = self.collection.find_one({id : data})
        return _docs

    #생성
    @staticmethod
    def db_document(self, id, data):
        self.doc_name = id
        self.doc_value = data
        self.collection.insert(
            [{
                id: data
            }]
        )

    #추가
    @staticmethod
    def db_add(self, name, time, number):
        self.collection.update(
            {self.doc_name: self.doc_value},
            {'$addToSet':{name:{time:number}}}
        )

    #업데이트
    @staticmethod
    def db_update(self, id, data):
        self.collection.update({self.doc_name: self.doc_value}, {'$set': {id: data}})

    #삭제
    @staticmethod
    def db_del(self, id, data):
        self.db.test01.remove({id : data,}, True)

    #모두 출력
    @staticmethod
    def db_allPrint(self, id, data):
        pprint(self.db_find(id, data))

    def __del__(self):
        self.connection.close()



