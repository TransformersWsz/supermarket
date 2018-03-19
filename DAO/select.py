import pymysql

class Select:
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

    def select(self,cursor,sql,values):
        try:
            counts = cursor.execute(sql,values)
            results = cursor.fetchall()
            return counts,results
        except:
            print("select error!!!")

