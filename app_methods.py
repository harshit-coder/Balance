from copy import deepcopy
import datetime
from werkzeug.exceptions import BadRequest

import mysql.connector
from mysql.connector import Error
import config
from flask import abort


def create_comection():
    try:
        conn = mysql.connector.connect(
            host=config.DATABASE.get("HOST"),
            database=config.DATABASE.get("DATABASE"),
            user=config.DATABASE.get("USERNAME"),
            password=config.DATABASE.get("PASSWORD"))
        cur = conn.cursor()

        return conn, cur
    except Exception as e:
        raise BadRequest(e)

class BadRequestException(Exception):
    def __init__(self, message, status=400):
        if status:
            self.context = status
        super().__init__(message)


def fetch_balance_price_data(date=None):
    try:
        conn, cur = create_comection()
        sp = 0
        cp = 0
        gk = 0
        pf = 0
        l1 = []
        balance = 0
        if date is not None:
            sql = 'SELECT * FROM balance_price where date = \'{}\' ORDER BY STR_TO_DATE(date, "%d/%m/%Y") DESC , id desc '.format(date)
        else:
            sql = 'SELECT * FROM balance_price ORDER BY STR_TO_DATE(date, "%d/%m/%Y") DESC ,id DESC'
        cur.execute(sql)
        l2 = cur.fetchall()
        if len(l2) > 0:
            for i in l2:
                l1.append({'time': i[2],
                        'date': i[1],
                        'id': i[0],
                        'selling_price': i[3],
                        'cost_price': i[4],
                        'ghar_kharch': i[5],
                        'profit': i[6],
                        'desc': i[8]})
                sp = sp + i[3]
                cp = cp + i[4]
                gk = gk + i[5]
                pf = pf + i[6]

            balance = pf - gk

        conn.commit()
        cur.close()
        conn.close()
        return {"l1": l1, "balance": balance, "date_2": date, "sp": sp, "cp": cp, "gk": gk, "pf": pf, "curr_date": datetime.date.today().strftime("%d/%m/%Y")}
    except Exception as e:
        raise BadRequest(e)

def dates_range_by_month(start_date):
    try:
        nxt_mnth = start_date.replace(day=28) + datetime.timedelta(days=4)
        res = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)

        d_r = dates_range2(res.day, start_date)
        tuple_dr = tuple(d_r)
        print(tuple_dr)
        return tuple_dr
    except Exception as e:
        raise BadRequest(e)


def dates_range2(res, start_date):
    try:
        l1 = []
        for i in range(1, res + 1):
            # Remove: print(i)  # This causes BlockingIOError
            l1.append(start_date.strftime("%d/%m/%Y"))
            start_date = start_date + datetime.timedelta(days=1)
        # Remove: print(l1)  # Also problematic
        return l1
    except Exception as e:
        # Replace: print(res,type) with proper logging
        import logging
        logging.error(f"dates_range2 error: {e}")
        raise e


def fetch_personal_purchase_results(rang_e):
    try:
        conn, cur = create_comection()
        profit = 0
        balance = 0
        sp = 0
        cp = 0
        gk = 0
        
        if len(rang_e) == 1:
            one_date = rang_e[0]
            sql_sp = 'SELECT SUM(selling_price) FROM balance_price where date =  \'{}\''.format(one_date)
            sql_cp = 'SELECT SUM(cost_price) FROM balance_price where date =  \'{}\''.format(one_date)
            sql_gk = 'SELECT SUM(ghar_kharch) FROM balance_price where date =  \'{}\''.format(one_date)
        else:  
        
            sql_sp = 'SELECT SUM(selling_price) FROM balance_price where date IN {}'.format(rang_e)
            sql_cp = 'SELECT SUM(cost_price) FROM balance_price where date IN  {}'.format(rang_e)
            sql_gk = 'SELECT SUM(ghar_kharch) FROM balance_price where date IN  {}'.format(rang_e)
        cur.execute(sql_sp)
        sum_sp = cur.fetchone()
        cur.execute(sql_cp)
        sum_cp = cur.fetchone()
        cur.execute(sql_gk)
        sum_gk = cur.fetchone()
        if len(sum_sp) > 0 and sum_sp[0] is not None and len(sum_cp) > 0 and sum_cp[0] is not None and len(sum_gk) > 0 and sum_gk[0] is not None:
            profit = int(sum_sp[0]) - int(sum_cp[0])
            balance = profit - sum_gk[0]
            sp = sum_sp[0]
            cp = sum_cp[0]
            gk = sum_gk[0]
        daterange = rang_e[0] + "-" + rang_e[len(rang_e) - 1]
        cur.close()
        conn.close()
        return {'sum_sp': sp, 'sum_cp': cp, 'sum_gk': gk, 'profit': profit, 'balance': balance,
                'month': daterange}
    except Exception as e:
        raise BadRequest(e)


def sp_cp_gk_validation(data):
    try:
        selling_price = int(data.get("sp")) if data.get("sp") and len(str(data.get("sp").strip())) > 0 else 0
        cost_price = int(data.get("cp")) if data.get("cp") and len(str(data.get("cp").strip())) > 0 else 0
        ghar_kharch = int(data.get("gk")) if data.get("gk") and len(str(data.get("gk"))) > 0 else 0
        if selling_price == cost_price == ghar_kharch == 0:
            raise BadRequestException("Please enter something")
        return selling_price,cost_price,ghar_kharch
    except Exception as e:
        raise e


def purchase_validation(amt):
    try:
        purchase = int(amt) if amt and len(str(amt).strip()) > 0 else 0
        if purchase == 0:
            raise BadRequestException("Please enter something")
        return purchase
    except Exception as e:
        raise e

def date_validation(entered_date):
    if entered_date and len(str(entered_date).strip()) > 0:
        # Normalize format as safety net
        parts = entered_date.split("/")
        if len(parts) == 3:
            day = parts[0].zfill(2)
            month = parts[1].zfill(2)  
            year = parts[2]
            normalized_date = f"{day}/{month}/{year}"
        else:
            normalized_date = entered_date
            
        ed = datetime.date(int(normalized_date.split("/")[2]), 
                          int(normalized_date.split("/")[1]),
                          int(normalized_date.split("/")[0]))
        
        if ed > datetime.date.today():
            raise BadRequest("Please don't enter future dates")
        else:
            return normalized_date
    else:
        raise BadRequest("Please give a valid date")

def date_compare(s_date,e_date):
    start_date = s_date
    end_date = e_date
    date_validation(start_date)
    date_validation(end_date)
    start_date_1 = datetime.date(int(start_date.split("/")[2]), int(start_date.split("/")[1]),
                                     int(start_date.split("/")[0]))
    end_date_1 = datetime.date(int(end_date.split("/")[2]), int(end_date.split("/")[1]),
                                   int(end_date.split("/")[0]))
    if start_date_1 > end_date_1:
        raise BadRequest("Please enter proper dates")
    return start_date_1,end_date_1


def fetch_paid_data(rang_e=None,s_date=None,e_date=None):
    try:
        conn, cur = create_comection()
        l1=[]
        if rang_e is not None:
            if len(rang_e) == 1:
                one_date = rang_e[0]

                sql = 'SELECT * FROM amount_paid_details where date =  \'{}\' ORDER BY id desc'.format(one_date)
            else:  
                sql = 'SELECT * FROM amount_paid_details where date IN {} ORDER BY STR_TO_DATE(date, "%d/%m/%Y") DESC , id desc'.format(rang_e)
        else:
            sql = 'SELECT * FROM amount_paid_details ORDER BY STR_TO_DATE(date, "%d/%m/%Y") DESC , id desc'
        cur.execute(sql)
        l2 = cur.fetchall()
        if len(l2) > 0:
            for i in l2:
                l1.append({'time': i[2],
                        'date': i[1],
                        'id': i[0],
                        'paid': i[3],
                        'desc': i[4]})

        conn.commit()
        cur.close()
        conn.close()
        return {"l1":l1,"s_date":s_date, "e_date":e_date,"curr_date": datetime.date.today().strftime("%d/%m/%Y")}

    except Exception as e:
        raise e
    


def fetch_purchase_data(rang_e=None,s_date=None,e_date=None):
    try:
        conn, cur = create_comection()
        to_pay = 0
        paid_extra = 0
        l1 = []
        purchase = 0
        total_to_pay=0
        total_paid_extra=0
        sql = 'SELECT SUM(purchase_amount) FROM purchase_details'
        cur.execute(sql)
        total_purchased = cur.fetchone()
        sql = 'SELECT SUM(amount_paid) FROM amount_paid_details'
        cur.execute(sql)
        sum_paid = cur.fetchone() 
        sql = 'SELECT * FROM purchase_details ORDER BY STR_TO_DATE(date, "%d/%m/%Y") ASC , id ASC'
        cur.execute(sql)
        l2 = cur.fetchall()
        if total_purchased[0] is not None:
            if  sum_paid[0] is not None:
                if total_purchased[0] >= sum_paid[0]:
                    total_to_pay = total_purchased[0] - sum_paid[0]
                else:
                    total_paid_extra = sum_paid[0] - total_purchased[0]
            else:
                total_to_pay= total_purchased[0]
                total_paid_extra=0

            if len(l2) > 0:
                for i in l2:
                    purchase = purchase + i[3]
                    if sum_paid[0] is not None:
                        if purchase <= sum_paid[0]:
                            dif = 0

                        else:
                            dif = purchase - sum_paid[0] - to_pay
                            to_pay = to_pay + dif
                    else:
                        dif = i[3]
                    d1 = {'time': i[2],
                                'date': i[1],
                                'id': i[0],
                                'purchase': i[3],
                                'to_pay':dif,
                                'desc':i[5]}
                    if rang_e is  None:
                        l1.append(deepcopy(d1))
                    else:
                        if i[1] in rang_e:
                            l1.append(deepcopy(d1))

        conn.commit()
        cur.close()
        conn.close()
        return {"l1":l1, "total_to_pay":total_to_pay,"total_paid_extra":total_paid_extra,"s_date":s_date, "e_date":e_date,"curr_date": datetime.date.today().strftime("%d/%m/%Y")}

    except Exception as e:
        raise e
 
