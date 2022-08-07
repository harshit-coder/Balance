# Using flask to make an api
# import necessary libraries and functions
import requests
import datetime

import time
from datetime import date

from flask import Flask, jsonify, request, render_template, url_for

import json

# creating a Flask app
import psycopg2

app = Flask(__name__, template_folder='templates', static_folder='static')


def create_comection():
    conn = psycopg2.connect(
        host="ec2-44-208-88-195.compute-1.amazonaws.com",
        database="d7h8ea9nje87du",
        user="kiewksyxofbvrr",
        password="3a2ae2dda46fbf735c5846485e5387ce62e9cf10a99ce3ead179d50807386819")
    cur = conn.cursor()

    return conn,cur


@app.route("/", methods=['GET', 'POST'])
def home():
    conn,cur = create_comection()
    if request.method == 'POST':
        print(request.data)
        if request.json:
            data = request.json
            profit = 0
            selling_price = int(data.get("sp")) if data.get("sp") else 0
            cost_price = int(data.get("cp")) if data.get("cp") else 0
            ghar_kharch = int(data.get("gk")) if data.get("gk") else 0
            ed = data.get("ed") if data.get("ed") else date.today().strftime("%d/%m/%Y")
            profit = selling_price - cost_price
            date_of_inserting = date.today().strftime("%d/%m/%Y")
            time_of_inserting = time.strftime("%I:%M %p")
            sql = 'INSERT INTO balance_price (selling_price, cost_price, ghar_kharch, profit,date,time)VALUES (%s, %s, %s, %s,%s, %s)'
            cur.execute(sql, (selling_price, cost_price, ghar_kharch, profit, ed, time_of_inserting))
            conn.commit()
            cur.close()
            conn.close()

        return {"message": "success", "date": date.today().strftime("%d/%m/%Y")}

    else:
        selling_price = 0
        cost_price = 0
        ghar_kharch = 0
        today_date = date.today().strftime("%d/%m/%Y")
        cur.close()
        conn.close()
        return render_template("Entry.html", selling_price=selling_price, cost_price=cost_price,
                               ghar_kharch=ghar_kharch, date=today_date)


@app.route("/table", methods=['GET', 'POST'])
def tables():
    conn, cur = create_comection()
    l1 = []
    dt = {}
    sp = 0
    cp = 0
    gk = 0
    pf = 0
    l1 = []
    l2 = []
    balance = 0
    if request.method == 'POST':
        print(request.data)
        date_1 = request.json
        date_2 = date_1.get("c_date")
        sql = 'SELECT * FROM balance_price where date = \'{}\' ORDER BY id'.format(date_2)
        cur.execute(sql)
        l2 = cur.fetchall()
        if len(l2) > 0:
            for i in l2:
                l1.append({'time': i[6],
                           'id': i[7],
                           'selling_price': i[0],
                           'cost_price': i[1],
                           'ghar_kharch': i[2],
                           'profit': i[3]})
                sp = sp + i[0]
                cp = cp + i[1]
                gk = gk + i[2]
                pf = pf + i[3]

            balance = gk - pf

        conn.commit()
        cur.close()
        conn.close()
        return {"l1": l1, "balance": balance, "date_2": date_2}
        # return render_template("Table.html", table=l1, balance=balance, date=date_1)
    else:
        date = datetime.date.today()
        today_date = date.strftime("%d/%m/%Y")
        sql = 'SELECT * FROM balance_price where date = %s ORDER BY id'
        cur.execute(sql, (today_date,))
        l2 = cur.fetchall()
        if len(l2) > 0:
            for i in l2:
                l1.append({'time': i[6],
                           'id': i[7],
                           'selling_price': i[0],
                           'cost_price': i[1],
                           'ghar_kharch': i[2],
                           'profit': i[3]})
                sp = sp + i[0]
                cp = cp + i[1]
                gk = gk + i[2]
                pf = pf + i[3]
            balance = gk - pf
        conn.commit()
        cur.close()
        conn.close()
        return render_template("Table.html", table=l1, balance=balance, date_2=today_date)


@app.route("/result", methods=['GET', 'POST'])
def results():
    conn, cur = create_comection()
    if request.method == 'POST':
        data = request.json
        start_date = data.get('s_date')
        end_date = data.get('e_date')
        start_date_1 = datetime.date(int(start_date.split("/")[2]), int(start_date.split("/")[1]),
                                     int(start_date.split("/")[0]))
        end_date_1 = datetime.date(int(end_date.split("/")[2]), int(end_date.split("/")[1]),
                                   int(end_date.split("/")[0]))
        s_m = start_date_1.strftime("%B")
        e_m = end_date_1.strftime("%B")

        res = start_date_1 + datetime.timedelta(days=end_date_1.day)
        d_r = dates_range(res, start_date_1, end_date_1)
        tuple_dr = tuple(d_r)
        sql_sp = 'SELECT SUM(selling_price) FROM balance_price where date IN {}'.format(tuple_dr)
        sql_cp = 'SELECT SUM(cost_price) FROM balance_price where date IN  {}'.format(tuple_dr)
        sql_gk = 'SELECT SUM(ghar_kharch) FROM balance_price where date IN  {}'.format(tuple_dr)

        cur.execute(sql_sp)
        sum_sp = cur.fetchone()
        cur.execute(sql_cp)
        sum_cp = cur.fetchone()
        cur.execute(sql_gk)
        sum_gk = cur.fetchone()
        if sum_sp and sum_cp and sum_gk:
            profit = int(sum_sp[0]) - int(sum_cp[0])
            balance = sum_gk[0] - profit
            sp=sum_sp[0]
            cp = sum_cp[0]
            gk = sum_gk[0]
        else:
            profit=0
            balance=0
            sp = 0
            cp=0
            gk=0
        daterange = start_date + "-" + end_date
        cur.close()
        conn.close()
        return {'sum_sp': sp, 'sum_cp': cp, 'sum_gk': gk, 'profit': profit, 'balance': balance,
                'month': daterange}


    else:
        test_date = datetime.datetime.now()
        previous_month = test_date.month - 1
        if test_date.month != 1:
            test_date = datetime.datetime(test_date.year, previous_month, 1)
        else:
            test_date = datetime.datetime(test_date.year - 1, previous_month, 1)

        nxt_mnth = test_date.replace(day=28) + datetime.timedelta(days=4)
        res = nxt_mnth - datetime.timedelta(days=nxt_mnth.day)
        start_date = test_date
        end_date = res
        prev_mon = start_date.strftime("%B")
        d_r = dates_range(res, start_date, end_date)
        tuple_dr = tuple(d_r)
        print(tuple_dr)
        sql_sp = 'SELECT SUM(selling_price) FROM balance_price where date IN {}'.format(tuple_dr)
        sql_cp = 'SELECT SUM(cost_price) FROM balance_price where date IN  {}'.format(tuple_dr)
        sql_gk = 'SELECT SUM(ghar_kharch) FROM balance_price where date IN  {}'.format(tuple_dr)

        cur.execute(sql_sp)
        sum_sp = cur.fetchone()
        cur.execute(sql_cp)
        sum_cp = cur.fetchone()
        cur.execute(sql_gk)
        sum_gk = cur.fetchone()
        if sum_sp and sum_cp and sum_gk:
            profit = int(sum_sp[0]) - int(sum_cp[0])
            balance = sum_gk[0] - profit
            sp=sum_sp[0]
            cp = sum_cp[0]
            gk = sum_gk[0]
        else:
            profit=0
            balance=0
            sp = 0
            cp=0
            gk=0
        cur.close()
        conn.close()
        return render_template("Result.html", sum_sp=sp, sum_cp=cp, sum_gk=gk, profit=profit,
                               balance=balance, month=prev_mon)


@app.route("/delete", methods=['GET', 'POST'])
def delete_table():
    conn, cur = create_comection()
    if request.method == "POST":
        data = request.json
        id = data.get("id")
        c_date = data.get("c_date")
        sql = 'DELETE FROM balance_price WHERE id =%s'
        cur.execute(sql, (id,))
        conn.commit()
        all_data = {
            "c_date": c_date}
        res = requests.post(url="http://127.0.0.1:5000/table", json=all_data)
        data = json.loads(res.text)
        cur.close()
        conn.close()
        return {"l1": data["l1"], "balance": data["balance"], "date_2": all_data["c_date"]}


@app.route("/edit", methods=['GET', 'POST'])
def edit_table():
    conn, cur = create_comection()
    data = request.json
    id = data.get("id")
    selling_price = int(data.get("sp"))
    cost_price = int(data.get("cp"))
    ghar_kharch = int(data.get("gk"))
    c_date = data.get("c_date")
    profit = selling_price - cost_price
    sql = 'UPDATE balance_price set selling_price=%s, cost_price=%s, ghar_kharch=%s, profit = %s where id  = %s'
    cur.execute(sql, (selling_price, cost_price, ghar_kharch, profit, id))
    conn.commit()
    all_data = {
        "c_date": c_date}
    res = requests.post(url="https://dailybalanceapp.herokuapp.com/table", json=all_data)
    data = json.loads(res.text)
    cur.close()
    conn.close()
    return {"l1": data["l1"], "balance": data["balance"], "date_2": all_data["c_date"]}


def dates_range(res, start_date, end_date):
    l1 = []
    for i in range(0, res.day):
        l1.append(start_date.strftime("%d/%m/%Y"))
        start_date = start_date + datetime.timedelta(days=1)
    return l1


@app.route("/history", methods=['GET', 'POST'])
def history():
    conn, cur = create_comection()
    l1 = []
    dt = {}
    sp = 0
    cp = 0
    gk = 0
    pf = 0
    l1 = []
    l2 = []
    balance = 0
    date = datetime.date.today()
    sql = 'SELECT * FROM balance_price ORDER BY id DESC'
    cur.execute(sql)
    l2 = cur.fetchall()
    if len(l2) > 0:
        for i in l2:
            l1.append({'time': i[6],
                       'date': i[5],
                       'id': i[7],
                       'selling_price': i[0],
                       'cost_price': i[1],
                       'ghar_kharch': i[2],
                       'profit': i[3]})
            sp = sp + i[0]
            cp = cp + i[1]
            gk = gk + i[2]
            pf = pf + i[3]
        balance = gk - pf
    conn.commit()
    cur.close()
    conn.close()
    return render_template("History.html", table=l1, balance=balance)


# driver function
if __name__ == '__main__':
    app.run(debug=True)
