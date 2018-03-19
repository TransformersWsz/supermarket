import pymysql

class Update:
    def __init__(self):
        pass

    def connectdb(self):
        conn = pymysql.connect(
            host='localhost',
            user='root',
            passwd='root',
            db='jxc',
            port=3306,
            charset='utf8'
        )
        self.db = conn
        return conn.cursor()

    def update(self,cursor,sql,values):
        try:
            cursor.execute(sql,values)
            self.db.commit()
            return 1
        except:
            print("update error!!!")
            self.db.rollback()
            return -1


