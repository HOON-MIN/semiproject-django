from django.db import models

#import cx_Oracle as ora

from config.models import MyModel

class LogModel(MyModel):
    def __init__(self,msg):
        self.msg = msg
    def loginCheck(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "select mem_name, mem_no from member where mem_id=%s and mem_pw=%s"
        cursor.execute(sql,self.msg)
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res
    def memberlog(self,request):
        user_id = request.session['user_id']
        status = self.msg
        reip = 'no data'
        env = 'no data'
        browser = 'no data'
        try:
            reip = request.META.get('REMOTE_ADDR')
            browser = request.user_agent.browser.family
            if request.user_agent.is_pc:
                env = 'Desktop'
            elif request.user_agent.is_mobile:
                env = 'Mobile'
                if request.user_agent.is_tablet:
                    env = 'Tablet'
            elif request.user_agent.is_tablet and not request.user_agent.is_mobile:
                env = 'Tablet'
            else:
                env = 'Others'
        except:
            pass
        tup1 = (user_id,reip,env,browser,status)
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "insert into memberlog(idn,reip,env,browser,status,sstime) values(%s,%s,%s,%s,%s,sysdate())"
        cursor.execute(sql,tup1)
        cursor.close()
        conn.commit()
        conn.close()

    def findIdPwd(self):
        conn = self.myconn()
        cursor = conn.cursor()
        if len(self.msg) > 2:
            sql = "select mem_pw from member where mem_id=%s and mem_q=%s and mem_a=%s"
            cursor.execute(sql, self.msg)
            res = cursor.fetchone()
            cursor.close()
            conn.close()
            return res
        else:
            sql = "select mem_id from member where mem_name=%s and mem_email=%s"
            cursor.execute(sql, self.msg)
            res = cursor.fetchone()
            cursor.close()
            conn.close()
            return res

class JoinProcess(MyModel):
    def joinmember(self, join_list):
        conn = self.myconn()
        cursor = conn.cursor()
        # mem_no, mem_id, mem_pw, mem_name, mem_jubun, mem_email, mem_phone, mem_adr, sysdate, mem_q, mem_a
        sql = 'insert into member(mem_no, mem_id, mem_pw, mem_name, mem_jubun, mem_email, mem_phone, mem_adr, mem_date, mem_q, mem_a) values(mem_no,%s,%s,%s,%s,%s,%s,%s,sysdate(),%s,%s)'
        cursor.execute(sql, join_list)
        cursor.close()
        conn.commit()
        conn.close()

    def idcheck(self, mem_id):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select count(mem_id) from member where mem_id=%s'
        cursor.execute(sql, mem_id)
        res = cursor.fetchone()
        print('res =======>', res)
        cursor.close()
        conn.close()
        return res

    def emailcheck(self, mem_email):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select count(mem_email) from member where mem_email=%s'
        cursor.execute(sql, mem_email)
        res = cursor.fetchone()
        print('res =======>', res)
        cursor.close()
        conn.close()
        return res


class PagingSet(MyModel):
    def __init__(self, chk_method, request):
        self.chk_method = chk_method
        self.request = request

    def page_list(self):
        if self.chk_method == 'GET':
            searchValue = self.request.GET.get('searchValue', '')
            msg = 'get'
            print(msg)
            return searchValue
        else:
            searchValue = self.request.POST['searchValue']
            msg = 'post'
            print(msg)
            return searchValue

    def searchVal_len(self, searchValue):
        conn = self.myconn()
        cursor = conn.cursor()
        if len(searchValue) > 0:
            sql = "select mem_no, mem_id, mem_name, mem_jubun, mem_email, mem_phone, mem_adr, mem_date from member where mem_name like '%"+searchValue+"%' order by 1 desc"
        else:
            sql = 'select mem_no, mem_id, mem_name, mem_jubun, mem_email, mem_phone, mem_adr, mem_date from member order by 1 desc'
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def count(self):
        conn = self.myconn()
        cursor = conn.cursor()
        count = 'select count(*) from member order by 1 desc'
        cursor.execute(count)
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        return res

class MemberProcess(MyModel):

    def memberDetail(self, mem_no):
        conn = self.myconn()
        cursor = conn.cursor()
        sql_detail = "select mem_no, mem_id, mem_name, mem_jubun, mem_email, mem_phone, mem_adr, mem_date from member where "+mem_no[0]+" = '"+mem_no[1]+"'"
        cursor.execute(sql_detail)
        admemberDetail = cursor.fetchone()
        cursor.close()
        conn.close()
        return admemberDetail

    def memberUpdate(self, list):
        conn = self.myconn()
        cursor = conn.cursor()
        sql_update = "update member set mem_name=%s, mem_phone=%s, mem_adr=%s where mem_no=%s"
        cursor.execute(sql_update, list)
        cursor.close()
        conn.commit()
        conn.close()

    def memberDelete(self, mem_no):
        conn = self.myconn()
        cursor = conn.cursor()
        sql_delete = "delete from member where mem_no=%s"
        cursor.execute(sql_delete, mem_no)
        cursor.close()
        conn.commit()
        conn.close()

class memberChart1(MyModel):
    def genderChart(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "select case when substr(mem_jubun,8,1) in (1,3) then '남성' when substr(mem_jubun,8,1) in (2,4) then '여성' end as gender, count(*) as count from member group by gender"
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return res
    def birthChart(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = """
        select case when (substr(mem_jubun,1,2) between 00 and 09) then '00년대생' 
        when (substr(mem_jubun,1,2) between 50 and 59) then '50년대생' 
        when (substr(mem_jubun,1,2) between 60 and 69) then '60년대생' 
        when (substr(mem_jubun,1,2) between 70 and 79) then '70년대생' 
        when (substr(mem_jubun,1,2) between 80 and 89) then '80년대생' 
        when (substr(mem_jubun,1,2) between 90 and 99) then '90년대생' 
        else '모름' end as birth, count(*) from member group by birth
        """
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return res
    def locChart(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "select SUBSTRING_INDEX(mem_adr, ' ', 1)  as addr1, count(*) from member where mem_id != 'admin' group by addr1 order by addr1 asc"
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return res
    def locChart2(self,msg):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "select SUBSTRING_INDEX(SUBSTRING_INDEX(mem_adr, ' ', 2), ' ', -1)  as addr2 ,count(*) as count from member where mem_id != 'admin' and SUBSTRING_INDEX(mem_adr, ' ', 1) = %s group by addr2 order by addr2 asc;"
        cursor.execute(sql,msg)
        res = cursor.fetchall()
        cursor.close()
        conn.commit()
        conn.close()
        return res

class MemberLogChart(MyModel):
    def envLogChart1(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select env, count(*) as count from memberlog group by env'
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res

    def browserLogChart1(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = 'select browser, count(*) as count from memberlog group by browser'
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res

    def ratioChart1(self):
        conn = self.myconn()
        cursor = conn.cursor()
        sql = "SELECT COUNT(CASE WHEN c.count >= 10 THEN 1 END) AS res1, " \
              "COUNT(CASE WHEN c.count >= 5 AND c.count < 10 THEN 2 END) AS res2, " \
              "COUNT(CASE WHEN c.count >= 1 AND c.count < 5 THEN 3 END) AS res3 " \
              "FROM (SELECT idn, COUNT(*) AS count FROM memberlog WHERE status = 'login' GROUP BY idn) AS c"
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        return res
