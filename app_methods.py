import datetime

import mysql.connector
from mysql.connector import Error
import config


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
        raise e


def fetch_balance_price_data(date):
    conn, cur = create_comection()
    sp = 0
    cp = 0
    gk = 0
    pf = 0
    l1 = []
    balance = 0
    sql = 'SELECT * FROM balance_price where date = \'{}\' ORDER BY id'.format(date)
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
                       'desc': i[7]})
            sp = sp + i[3]
            cp = cp + i[4]
            gk = gk + i[5]
            pf = pf + i[6]

        balance = pf - gk

    conn.commit()
    cur.close()
    conn.close()
    return {"l1": l1, "balance": balance, "date_2": date, "sp": sp, "cp": cp, "gk": gk, "pf": pf, "curr_date": datetime.date.today().strftime("%d/%m/%Y")}


def dates_range_by_month(start_date):
    nxt_mnth = start_date.replace(day=28) + datetime.timedelta(days=4)
    res = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)
    d_r = dates_range2(res, start_date)
    tuple_dr = tuple(d_r)
    print(tuple_dr)
    return tuple_dr


def dates_range2(res, start_date):
    try:
        l1 = []
        for i in range(1, res.day + 1):
            l1.append(start_date.strftime("%d/%m/%Y"))
            start_date = start_date + datetime.timedelta(days=1)
        return l1
    except Exception as e:
        print(res,type)
        raise e


def fetch_personal_purchase_results(rang_e):
    conn, cur = create_comection()
    profit = 0
    balance = 0
    sp = 0
    cp = 0
    gk = 0
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


def sp_cp_gk_validation(data):
    selling_price = int(data.get("sp")) if data.get("sp") and len(str(data.get("sp").strip())) > 0 else 0
    cost_price = int(data.get("cp")) if data.get("cp") and len(str(data.get("cp").strip())) > 0 else 0
    ghar_kharch = int(data.get("gk")) if data.get("gk") and len(str(data.get("gk"))) > 0 else 0
    if selling_price == cost_price == ghar_kharch == 0:
        raise "Please enter something"
    return selling_price,cost_price,ghar_kharch


def date_validation(data):
    if data.get("ed") and len(str(data.get("ed").strip())) > 0:
        ed = data.get("ed")
        ed = datetime.date(int(ed.split("/")[2]), int(ed.split("/")[1]),
                                     int(ed.split("/")[0]))
        if ed > datetime.datetime.now().date:
            raise "Please don't enter a future date"
    else:
        raise "Please give a valid date"


def date_compare(data):
    start_date = data.get('s_date')
    end_date = data.get('e_date')
    date_validation(start_date_1)
    date_validation(end_date_1)
    start_date_1 = datetime.date(int(start_date.split("/")[2]), int(start_date.split("/")[1]),
                                     int(start_date.split("/")[0]))
    end_date_1 = datetime.date(int(end_date.split("/")[2]), int(end_date.split("/")[1]),
                                   int(end_date.split("/")[0]))
    if start_date_1 > end_date_1:
        raise "Please enter proper dates"
    return start_date_1,end_date_1