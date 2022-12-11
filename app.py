# Using flask to make an api
# import necessary libraries and functions

import datetime
import time
from datetime import date

import git
from flask import Flask, request, render_template, jsonify

from app_methods import create_comection, date_compare, fetch_balance_price_data, dates_range2, dates_range_by_month, fetch_personal_purchase_results, sp_cp_gk_validation, date_validation

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/git_update', methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('./Balance')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


@app.route("/personal_purchase_table_results", methods=['GET', 'POST'])
def personal_purchase_table_results():
    if request.method == 'POST':
        data = request.json
        start_date_1, end_date_1 = date_compare(data)
        res = end_date_1 - start_date_1
        tuple_dr = tuple(dates_range2(res, start_date_1))
        res = fetch_personal_purchase_results(tuple_dr)
        return jsonify(res)

    else:
        month = datetime.datetime.now().month
        prev_month = month-1
        year = datetime.datetime.now().year
        if month != 1:
            start_date = datetime.datetime(year, prev_month, 1)
        else:
            start_date = datetime.datetime(year - 1, prev_month, 1)
        tuple_dr = dates_range_by_month(start_date)
        res = fetch_personal_purchase_results(tuple_dr)
        return render_template("Result.html",
                               sum_sp=res['sum_sp'],
                               sum_cp=res['sum_cp'],
                               sum_gk=res['sum_gk'],
                               profit=res['profit'],
                               balance=res['balance'],
                               month=start_date.strftime('%B'))


@app.route("/personal_purchase_table_history", methods=['GET', 'POST'])
def personal_purchase_table_history():
    conn, cur = create_comection()
    sp = 0
    cp = 0
    gk = 0
    pf = 0
    l1 = []
    balance = 0
    date = datetime.date.today()
    sql = 'SELECT * FROM balance_price ORDER BY id DESC'
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
                       'profit': i[6]})
            sp = sp + i[3]
            cp = cp + i[4]
            gk = gk + i[5]
            pf = pf + i[6]
        balance = pf - gk
    conn.commit()
    cur.close()
    conn.close()
    return render_template("History.html", table=l1, balance=balance, sp=sp, cp=cp, gk=gk, pf=pf)


@app.route("/", methods=['GET', 'POST'])
def personal_purchase_table():
    if request.method == 'POST':
        fetch_date = request.json.get("c_date")
        data = fetch_balance_price_data(fetch_date)
        return jsonify(data)
    else:
        date = datetime.date.today()
        today_date = date.strftime("%d/%m/%Y")
        data = fetch_balance_price_data(today_date)
        return render_template("Table.html",
                               table=data.get('l1'),
                               balance=data.get('balance'),
                               date_2=data.get('date_2'),
                               sp=data.get('sp'),
                               cp=data.get('cp'),
                               gk=data.get('gk'),
                               pf=data.get('pf'),
                               curr_date=data.get('curr_date'))


@app.route("/personal_purchase_table_delete", methods=['GET', 'POST'])
def personal_purchase_table_delete():
    conn, cur = create_comection()
    data = request.json
    id = data.get("id")
    c_date = data.get("c_date")
    sql = 'DELETE FROM balance_price WHERE id =%s'
    cur.execute(sql, (id,))
    conn.commit()
    cur.close()
    conn.close()
    res = fetch_balance_price_data(c_date)
    return jsonify(res)


@app.route("/personal_purchase_table_edit", methods=['GET', 'POST'])
def personal_purchase_table_edit():
    try:
        conn, cur = create_comection()
        data = request.json
        id = data.get("id")
        sp, cp, gk = sp_cp_gk_validation(data)
        desc = data.get('desc').strip()
        ed = date_validation(data)
        profit = sp - cp
        sql = 'UPDATE balance_price set selling_price=%s, cost_price=%s, ghar_kharch=%s, profit = %s desc = %s where id  = %s'
        cur.execute(sql, (sp, cp, gk, profit, desc, id))
        conn.commit()
        res = fetch_balance_price_data(ed)
        return jsonify(res)
    except Exception as e:
        raise e


@app.route("/personal_purchase_table_add", methods=['GET', 'POST'])
def personal_purchase_table_add():
    try:
        if request.json:
            conn, cur = create_comection()
            data = request.json
            sp, cp, gk = sp_cp_gk_validation(data)
            ed = date_validation(data)
            desc = data.get('desc').strip()
            profit = sp - cp
            time_of_inserting = time.strftime("%I:%M %p")
            sql = 'INSERT INTO balance_price (selling_price, cost_price, ghar_kharch, profit,date,time,desc)VALUES (%s, %s, %s, %s,%s, %s,%s)'
            cur.execute(sql, (sp, cp, gk, profit, ed, time_of_inserting, desc))
            conn.commit()
            cur.close()
            conn.close()
            res = fetch_balance_price_data(ed)
            return jsonify(res)
    except Exception as e:
        raise e


# driver function
if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=5002)

