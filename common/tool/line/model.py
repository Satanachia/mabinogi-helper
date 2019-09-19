import sqlite3
import time
from datetime import datetime


class Model(object):
    def __init__(self):

        dbName = 'maibinogi.db'
        self.conn = sqlite3.connect(dbName)
        self.cur = self.conn.cursor()
        # print('[INFO] connect to %s success' % (dbName))

    def getAll(self, tableName):
        sql = "SELECT * FROM %s;" % (tableName)
        self.cur.execute(sql)
        result = self.cur.fetchall()
        return result

    def getOne(self, tableName, sql):
        sql = "SELECT * FROM %s WHERE %s;" % (tableName, sql)
        self.cur.execute(sql)
        result = self.cur.fetchone()
        return result

    def exists(self, tableName, sql):
        sql = "SELECT * FROM %s WHERE %s;" % (tableName, sql)
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if (result == None):
            return False
        else:
            return True


class Boss(Model):
    tableName = "boss_log"

    def __init__(self):
        self.tableName = "boss_log"
        super().__init__()
        self.createtable()


    def insert(self):
        self.created_at = int(time.mktime(datetime.now().timetuple()))
        sql = ("INSERT INTO %s () VALUES ();" % (self.tableName))

        try:
            self.cur.execute(sql, [])
            self.conn.commit()
            # print('[INFO] INSERT success: %d'%(self.conn.lastrowid))
        except sqlite3.Error as e:
            print("[ERROR] INSERT error: %s"%(str(e)))

#TODO make migrate
    def createtable(self):
        self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='%s';" % (self.tableName))
        if(self.cur.fetchone() is None):
            try:
                sql = "create table %s (\
                    id         INTEGER PRIMARY KEY  autoincrement  NOT NULL,\
                    created_at INTEGER  not null);" % (self.tableName)
                if (self.cur.execute(sql)):
                    print("[INFO] Create table success")
            except sqlite3.Error as e:
                print("[ERROR] Create table error: %s"%(str(e)))

