#encoding:utf-8
import pymongo
from pymongo import MongoClient
from bson.dbref import DBRef

class MGDB:
    conn = None
    db = None
    def __init__(self, IP, Port, DBName):
        self.conn = MongoClient(IP,Port)
        #db = conn.pyrand
        self.db = self.conn[DBName]
        return
        '''
        for i in range(1,3):
            rnd = random.randint(0,1000)
            ret = col.insert({'val':rnd})
	        ids.append(ret)
        '''
    def insertdata(self,colname,data):
        return self.db[colname].insert(data)
        '''
        for i in range(1,3):
            rnd = random.randint(1000,2000)
            ret = cref.insert({'ball':rnd,'addr':DBRef(collection='setpy',id=ids.pop())})
        '''
    def querydata(self,colname,)
    def close(self):
        self.conn.close()
        return