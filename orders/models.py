from django.db import models, transaction

from config.models import MyModel

class OrdersDao(MyModel):
    # 일반회원 - 구매하기
    def ordInsert(self, data):
        '''
        "insert into item values(null,:mem_no,:i_no,:ord_count" \
                     ",'상품준비중',:ord_address,:ord_name,now(), null,null,null);"
        '''
        sql_ordInsert = "insert into item values(null,%s,%s,%s" \
                     ",'상품준비중',%s,%s,sysdate(), null,null,null);"
        conn = self.myconn()
        cursor = conn.cursor()
        # cursor.execute(sql_insert, pwd=pwdv, writer=writerv, subject=subjectv, content=contentv)
        cursor.execute(sql_ordInsert, data)
        cursor.close()
        conn.commit()
        conn.close()

# ---------------- 보류 ------------------
    # 회원이 주문 시(item insert) 구매한 상품의 재고가 줄어들도록! stock update
    # def ordStockUpdate(self, num):
    #     conn = self.myconn()
    #     cursor = conn.cursor()
    #     sql_update = """
    #         update stock set s_stock = s_stock - (select ord_count from item where ord_no = :1 )
    #         where s_no = (select i_no from item where ord_no = :1)
    #     """
    #     cursor.execute(sql_update, num)
    #     cursor.close()
    #     conn.commit()
    #     conn.close()

    # 관리자 - 일반회원들의 구매목록 정보 리스트
    def adminOrdList(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql_select = """
        select @ROWNUM := @ROWNUM +1 as r_num, ord_no, i_name, ord_count,totalPrice, 
        mem_name,ord_name,ord_address, i_status,ord_date, ord_edate, ord_cdate from (
            select o.ord_no ord_no, o.ord_name ord_name, o.mem_no mem_no,  
            o.i_no i_no, o.ord_count ord_count, i.i_price*o.ord_count totalPrice, 
            o.i_status i_status, o.ord_address ord_address, o.ord_date ord_date, 
            o.ord_edate ord_edate, o.ord_cdate ord_cdate, m.mem_name mem_name, i.i_name i_name
            from orders o 
            inner join item i on i.i_no = o.i_no
            inner join member m on o.mem_no = m.mem_no 
            order by o.ord_no desc
        ) a WHERE (@ROWNUM := 0)=0
        """
        cursor.execute(sql_select)
        listv = cursor.fetchall()
        cursor.close()
        conn.close()
        return listv

    # 관리자 - 구매목록 detail ----------------------------
    def adminOrdDetail(self, ord_nov):
        print(f"adminOrdDetail models ord_nov => {ord_nov}")
        conn = self.myconn()
        cursor = conn.cursor()
        sql = """
            select o.ord_no, o.ord_name, m.mem_name, i.i_name, i.i_price, 
            o.ord_count, i.i_price*o.ord_count as totalPrice,
            i.i_img, o.ord_address, o.ord_date, o.ord_edate, o.ord_cdate, o.i_status
            from orders o inner join item i on o.i_no=i.i_no
            inner join member m  on o.mem_no = m.mem_no 
            where o.ord_no = %s
        """
        cursor.execute(sql, ord_nov)
        res = cursor.fetchone()
        cursor.close()
        conn.commit()
        conn.close()
        return res

    def adminOrdUpdate(self, data):
        conn = self.myconn()
        cursor = conn.cursor()
        sql_update = """
            CALL OrdUpProc(%s, %s, %s, %s)
        """
        cursor.execute(sql_update, data)
        cursor.close()
        conn.commit()
        conn.close()

    def adminOrdDelete(self, ord_nov):
        conn = self.myconn()
        cursor = conn.cursor()
        sql_delete = """
            delete from item where ord_no = %s
        """
        cursor.execute(sql_delete, ord_nov)
        cursor.close()
        conn.commit()
        conn.close()

    def adminOrdDeleteCheck(self, ord_nov):
        conn = self.myconn()
        cursor = conn.cursor()
        sql_ck = """
            select count(*) from item where i_status = '주문취소' and ord_no = %s
        """
        cursor.execute(sql_ck, ord_nov)
        res = cursor.fetchone()
        print(f"adminOrdDeleteCheck cnt => {res}")
        cursor.close()
        conn.commit()
        conn.close()
        return res
# -------------------------------------------
# 관리자 - 고객으로부터 주문 취소 요청 들어온 상황
# => cancel테이블 insert / item update / stock 재고 update
    def adminCanIns(self, indata, updata):
        conn = self.myconn()
        cursor = conn.cursor()
        sql_ins = """
                insert into cancel values(null, %s, sysdate(), %s)
            """
        cursor.execute(sql_ins, indata)
        print("여기는 adminCanIns models ins 성공")
        sql_up = """
            update item set i_status = '주문취소', rcnt = 0, 
                ord_cdate = (select cdate from cancel where ord_no = %s) 
                where ord_no = %s
        """
        cursor.execute(sql_up, updata)
        print("여기는 adminCanIns models up 성공")
        cursor.close()
        conn.commit()
        conn.close()

    # def adminCanOrdUp(self, num):
    #     conn = self.myconn()
    #     cursor = conn.cursor()
    #     print("adminCanOrdUp 1")
    #     sql_up = """
    #         update item set i_status = '주문취소', rcnt = 0,
    #             ord_cdate = (select cdate from cancel where ord_no = :1)
    #             where ord_no = :1
    #     """
    #     cursor.execute(sql_up, num)
    #     print("adminCanOrdUp 2")
    #     cursor.close()
    #     conn.commit()
    #     conn.close()
    #     print("여기는 adminCanOrdUp models 성공")

# ------------------- 주문 취소 - item update
    # def adminCanOrdUp(self, ord_nov):
    #     conn = self.myconn()
    #     cursor = conn.cursor()
    #     sql_ordCanUpdate = """
    #         update item set i_status = '주문취소', rcnt = 0, ord_cdate = sysdate() where ord_no = %s
    #     """
    #     cursor.execute(sql_ordCanUpdate, ord_nov)
    #     cursor.close()
    #     conn.commit()
    #     conn.close()
# ------------------- 주문 취소 - stock 재고 update
    # def adminCanStockUp(self, s_nov):
    #     conn = self.myconn()
    #     cursor = conn.cursor()
    #     sql_ordStockUpdate = """
    #         update stock set s_stock = s_stock+ 2 where s_no = 2
    #     """
    #     cursor.execute(sql_ordStockUpdate, s_nov)
    #     cursor.close()
    #     conn.commit()
    #     conn.close()
  # 'select o.ord_no, i.i_name, o.ord_count, i.i_price*o.ord_count as totalPrice, o.ord_name, o.ord_address, o.i_status, o.rcnt, i.i_no ' \
        #                      'from item o, item i, member m where i.i_no = o.i_no and o.mem_no=m.mem_no and m.mem_no = %s order by o.ord_no desc'
 ## 일반회원 - 리스트
class MyorderDao(MyModel):
     def listMyorders(self,request):
        mem_no = request.session['mem_no']
        mem_no2 = str(mem_no)
        print(mem_no)
        conn = self.myconn()
        cursor = conn.cursor()
        sql_select = """
        select @ROWNUM := @ROWNUM +1 as r_num,  ord_name, i_name, ord_count,
    	totalPrice, ord_address, i_status, i_no, ord_address, rcnt from (
        select o.ord_no, i.i_name , o.ord_name,
    	o.ord_count, i.i_price*o.ord_count as totalPrice,
    	o.i_status, o.ord_address, o.i_no, o.rcnt
    	from orders o
        inner join item i on i.i_no = o.i_no
        inner join member m on o.mem_no = m.mem_no 
        and m.mem_no = 
        """+"'"+mem_no2+"'"+""" 
        order by o.ord_no desc
        ) a WHERE (@ROWNUM := 0)=0;
        """
        cursor.execute(sql_select)
        # """+"'"+mem_no2+"'"+"""
        # print(cursor.fetchall())
        # print(type(cursor.fetchall())) # <class 'list'>
        select = cursor.fetchall()
        cursor.close()
        conn.close()
        return select


class myChart(MyModel):
    def odersChart(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql ='select i.i_name, i.i_no, ordTotalCnt, i.i_img from ' \
             '(select i_no, sum(ord_count) as ordTotalCnt from orders ' \
             'group by i_no order by ordTotalCnt desc) a, item i where  a.i_no = i.i_no'
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()















