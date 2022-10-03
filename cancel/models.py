from django.db import models

from config.models import MyModel


class CancelDao(MyModel):
    def canList(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql_select = """
            select @ROWNUM := @ROWNUM +1 as r_num, c.ordc_no, i.i_name, o.ord_count, i.i_price*o.ord_count totalPrice,
                c.creason, c.cdate, o.mem_no
                from orders o
                inner join cancel c on o.ord_no = c.ord_no
                inner join item i on i.i_no = o.i_no
                WHERE (@ROWNUM := 0)=0 order by c.ordc_no desc
        """
        cursor.execute(sql_select)
        listv = cursor.fetchall()
        cursor.close()
        conn.close()
        return listv

    def canResult(self):
        conn = self.myconn()
        cursor = conn.cursor()
        # answer = [ans.ans1, ans.ans2, ans.ans3, ans.ans4]
        sql_select = """
            select creason, count(creason) sum1 from cancel group by creason
        """
        cursor.execute(sql_select)
        listv = cursor.fetchall()
        cursor.close()
        conn.close()
        # surveyList = zip(surveyList, answer)
        # for e, ans in surveyList:
        #     print("*"*30)
        #     print(f"{ans} => {e.sum_num}")
        return listv