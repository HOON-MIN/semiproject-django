from django.db import models
from django.http import request
from django.shortcuts import redirect

# Create your models here.
from config.models import MyModel

class MybasketDao(MyModel):
    def listMybasket(self,request):
        mem_no = request.session['mem_no']
        mem_no2 = str(mem_no)
        conn = self.myconn()
        cursor = conn.cursor()
        sql_select ="""
        select @ROWNUM := @ROWNUM +1 as r_num, b_num, i_name, i_price, totalPrice, b_stock  from (
        select b.b_num, i.i_name, i.i_price, i.i_price*b.b_stock as totalPrice, b.b_stock from basket b
        inner join item i on i.i_no = b.i_no  and mem_no = 
        """+"'"+mem_no2+"'"+""" 
        order by b.b_num desc) a  WHERE (@ROWNUM := 0)=0
        """
        cursor.execute(sql_select)
        listv = cursor.fetchall()
        print(listv)
        cursor.close()
        conn.close()
        return listv

    # 장바구니 디테일
    # select b.b_num, b.i_no, i.i_name, i.i_price, i.i_category1, i.i_category2, i.i_price*b.b_stock as totalPrice, b.b_stock from basket	b, item i where i.i_no = b.i_no and b.b_num = 7;
    def basketDetail(self, bnum):
        bnum2 = str(bnum)
        print(bnum2)
        conn = self.myconn()
        cursor = conn.cursor()
        sql_select ='select b.b_num, b.i_no, i.i_name, i.i_price, i.i_category1,' \
                    ' i.i_category2, i.i_price*b.b_stock as totalPrice, b.b_stock' \
                    ' from basket b, item i where i.i_no = b.i_no and b.b_num ='+bnum2
        cursor.execute(sql_select)
        detail = cursor.fetchone()
        print(detail)
        cursor.close()
        conn.close()
        return detail
    # 장바구니 추가 확인
# insert into basket values(basket_seq.nextVal,  # {mem_no}, #{i_no}, #{b_stock})

    # 장바구니 수정
    def basketUpdate(self, data):
        conn = self.myconn()
        sql_update = 'update basket set b_stock ='+data[0]+' where b_num = '+data[1]
        cursor = conn.cursor()
        cursor.execute(sql_update)
        cursor.close()
        conn.commit()
        conn.close()
    # 장바구니 삭제
    def basketDelete(self, bnum):
        conn = self.myconn()
        sql_delete = 'delete from basket where b_num= %s'
        cursor = conn.cursor()
        cursor.execute(sql_delete, bnum)
        cursor.close()
        conn.commit()
        conn.close()
# 장바구니 구매
# insert into item values(
# 		orders_seq.nextVal,#{mem_no},#{i_no},#{b_stock},'상품준비중',
# 		#{ordersvo.ord_address},#{ordersvo.ord_name},sysdate,null,null)
#     def insertBasket(self, data):
#         conn = self.myconn()
#         cursor = conn.cursor()
#         sql_insert = "insert into basket values(null,:mem_no,:i_no,:b_stock)"
#         print('con=>', cursor)
#         # ord_no,mem_no,i_no,ord_count,i_status,ord_address,ord_name,ord_date,ord_edate,ord_cdate,rcnt
#         cursor.execute(sql_insert, data)
#         cursor.close()
#         conn.commit()
#         conn.close()

    ## 장바구니 폼으로 불러오기
    def basketordersform(self, bnum):
        bnum2 = str(bnum)
        print(bnum2)
        conn = self.myconn()
        cursor = conn.cursor()
        sql_select = "select i.i_no, i.i_name, i.i_price, i.i_price*b.b_stock as totalPrice, " \
                     "b.b_stock,b.b_num, mem_no from basket b, item i where i.i_no = b.i_no  " \
                     "and b_num =" + bnum2
        print('con=>', cursor)
        cursor.execute(sql_select)
        select = cursor.fetchone()
        print(select)
        cursor.close()
        conn.close()
        return select

    # 장바구니에서 주문하기
    def baOrderInsert(self, data):
        conn = self.myconn()
        sql_ordInsert = "insert into orders values(null,%s,%s,%s," \
                        "'상품준비중',%s,%s,sysdate(),null,null,null)"
        cursor = conn.cursor()
        cursor.execute(sql_ordInsert, data)
        cursor.close()
        conn.commit()
        conn.close()
