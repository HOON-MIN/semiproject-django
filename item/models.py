from django.db import models

# Create your models here.
from config.models import MyModel

class ItemList(MyModel):
    #등록순 상품 리스트 ( 메인 리스트 )
    def new_itemList(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select i_no,i_name,i_price,round(i_price*1.5) as sale,i_comm,i_img from item order by 1 desc'
        cursor.execute(sql)
        res = cursor.fetchall()
        print(cursor)
        print('type===> ',type(res))
        cursor.close()
        conn.close()
        return res

    # 상품 상세페이지
    def detail_item(self,num):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select i_no,i_name,i_price,i_category1,i_category2,i_comm,i_img from item where i_no=%s'
        cursor.execute(sql,num)
        res = cursor.fetchone()
        print(res)
        cursor.close()
        conn.close()
        return res

    # 검색 상품 페이지
    def search_item(self,search):
        conn = self.myconn()
        cursor = conn.cursor()
        print(search)
        print(type(search))
        sql = "select i_no,i_name,i_price,round(i_price*1.5) as sale,i_comm,i_img from item where i_name like %s order by 1 desc"
        cursor.execute(sql,'%%%s%%' % search)
        res=cursor.fetchall()
        cursor.close()
        conn.close()
        return res

    #상품 등록
    def registration_item(self,items):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'insert into item values(null,%s,%s,%s,%s,%s,%s,12)'
        cursor.execute(sql,items)
        cursor.close()
        conn.commit()
        conn.close()

    #상품 인기 차트
    def chart_item(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select i_name, sum(click) sum from item group by i_name order by sum desc limit 5'
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res