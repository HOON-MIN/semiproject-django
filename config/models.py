import pymysql as py

class MyModel:
    def myconn(self):
        conn = py.connect(host='192.168.0.50', #자신ip
                          port=3306,
                          user='semiDemo', #mysql만든 아이디
                          passwd='kosmo113',#만든아이디 비밀번호
                          db='semiDemo', #안에서 사용하는 db이름
                          charset='utf8')
        return conn
