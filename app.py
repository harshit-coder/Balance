# Using flask to make an api
# import necessary libraries and functions

import datetime
import time
from datetime import date
import config
from flask  import abort
import git
from flask import Flask, request, render_template, jsonify

from app_methods import create_comection, date_compare, fetch_balance_price_data, dates_range2, dates_range_by_month, fetch_paid_data, fetch_personal_purchase_results, fetch_purchase_data, sp_cp_gk_validation, date_validation, purchase_validation

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
        start_date = data.get('s_date')
        end_date = data.get('e_date')
        start_date_1, end_date_1 = date_compare(start_date,end_date)
        if config.PASSED_LAST_DATE == 'exclude':
            res = end_date_1 - start_date_1
        else:
            end_date_1 = end_date_1 + datetime.timedelta(days=1)
            res = end_date_1 - start_date_1
       
        tuple_dr = tuple(dates_range2(res.days, start_date_1))
        res = fetch_personal_purchase_results(tuple_dr)
        return jsonify(res),200

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
    data = fetch_balance_price_data()
    return render_template("History.html", 
                           table=data.get('l1'), 
                           balance=data.get('balance'),
                           sp=data.get('sp'),
                            cp=data.get('cp'),
                            gk=data.get('gk'),
                            pf=data.get('pf'),)
    
    
@app.route("/purchase_table_history", methods=['GET', 'POST'])
def purchase_table_history():
    data = fetch_purchase_data()
    return render_template("purchase_history.html",
                           l1=data.get('l1'),
                           total_to_pay=data.get('total_to_pay'),
                           total_paid_extra=data.get('total_paid_extra'),
                           )

@app.route("/paid_table_history", methods=['GET', 'POST'])
def paid_table_history():
    data = fetch_paid_data()
    return render_template("paid_history.html",
                           l1=data.get('l1')
                           )
    

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
        
        
@app.route("/purchase", methods=['GET', 'POST'])
def purchase_table():
    if request.method == 'POST':
        start_fetch_date = request.json.get("sc_date")
        end_fetch_date = request.json.get("ec_date")
        start_date_1, end_date_1 = date_compare(start_fetch_date,end_fetch_date)
        if config.PASSED_LAST_DATE == 'exclude':
            res = end_date_1 - start_date_1
        else:
            end_date_1 = end_date_1 + datetime.timedelta(days=1)
            res = end_date_1 - start_date_1
       
        tuple_dr = tuple(dates_range2(res.days, start_date_1))
        data = fetch_purchase_data(tuple_dr,start_fetch_date,end_fetch_date)
        print(data)
        return jsonify(data)
    else:
        this_month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        start_date = datetime.date(year, this_month, 1)
        if config.PASSED_LAST_DATE == 'exclude':
            res = datetime.date.today() - start_date
        else:
            res = datetime.date.today() - start_date +  datetime.timedelta(days=1)

        print(res.days)
        tuple_dr = tuple(dates_range2(res.days, start_date))
        print(tuple_dr)
        data = fetch_purchase_data(tuple_dr,start_date.strftime("%d/%m/%Y"),datetime.date.today().strftime("%d/%m/%Y"))
        print(data)

        return render_template("purchased.html",
                                l1=data.get('l1'),
                                total_to_pay=data.get('total_to_pay'),
                                total_paid_extra=data.get('total_paid_extra'),
                                s_date=data.get('s_date'),
                                e_date=data.get('e_date'),
                                curr_date=data.get('curr_date'))


@app.route("/paid", methods=['GET', 'POST'])
def paid_table():
    if request.method == 'POST':
        start_fetch_date = request.json.get("sc_date")
        end_fetch_date = request.json.get("ec_date")
        start_date_1, end_date_1 = date_compare(start_fetch_date,end_fetch_date)
        if config.PASSED_LAST_DATE == 'exclude':
            res = end_date_1 - start_date_1
        else:
            end_date_1 = end_date_1 + datetime.timedelta(days=1)
            res = end_date_1 - start_date_1
       
        tuple_dr = tuple(dates_range2(res.days, start_date_1))
        data = fetch_paid_data(tuple_dr,start_fetch_date,end_fetch_date)
        print(data)
        return jsonify(data)
    else:
        this_month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        start_date = datetime.date(year, this_month, 1)
        if config.PASSED_LAST_DATE == 'exclude':
            res = datetime.date.today() - start_date
        else:
            res = datetime.date.today() - start_date +  datetime.timedelta(days=1)

        print(res.days)
        tuple_dr = tuple(dates_range2(res.days, start_date))
        print(tuple_dr)
        data = fetch_paid_data(tuple_dr,start_date.strftime("%d/%m/%Y"),datetime.date.today().strftime("%d/%m/%Y"))
        print(data)

        return render_template("paid.html",
                                l1=data.get('l1'),
                                s_date=data.get('s_date'),
                                e_date=data.get('e_date'),
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
    print(res)
    return jsonify(res)


@app.route("/purchase_table_delete", methods=['GET', 'POST'])
def purchase_table_delete():
    conn, cur = create_comection()
    data = request.json
    id = data.get("id")
    sc_date = date_validation(data.get('sc_date'))
    ec_date = date_validation(data.get('ec_date'))
    start_date_1, end_date_1 = date_compare(sc_date,ec_date)
    if config.PASSED_LAST_DATE == 'exclude':
        res = end_date_1 - start_date_1
    else:
        end_date_1 = end_date_1 + datetime.timedelta(days=1)
        res = end_date_1 - start_date_1

    tuple_dr = tuple(dates_range2(res.days, start_date_1))
    sql = 'DELETE FROM purchase_details WHERE id =%s'
    cur.execute(sql, (id,))
    conn.commit()
    cur.close()
    conn.close()
    res = fetch_purchase_data(tuple_dr,sc_date, ec_date)
    print(res)
    return jsonify(res)


@app.route("/paid_table_delete", methods=['GET', 'POST'])
def paid_table_delete():
    conn, cur = create_comection()
    data = request.json
    id = data.get("id")
    sc_date = date_validation(data.get('sc_date'))
    ec_date = date_validation(data.get('ec_date'))
    start_date_1, end_date_1 = date_compare(sc_date,ec_date)
    if config.PASSED_LAST_DATE == 'exclude':
        res = end_date_1 - start_date_1
    else:
        end_date_1 = end_date_1 + datetime.timedelta(days=1)
        res = end_date_1 - start_date_1

    tuple_dr = tuple(dates_range2(res.days, start_date_1))
    sql = 'DELETE FROM amount_paid_details WHERE id =%s'
    cur.execute(sql, (id,))
    conn.commit()
    cur.close()
    conn.close()
    res = fetch_paid_data(tuple_dr,sc_date, ec_date)
    print(res)
    return jsonify(res)


@app.route("/personal_purchase_table_edit", methods=['GET', 'POST'])
def personal_purchase_table_edit():
    try:
        conn, cur = create_comection()
        data = request.json
        id = data.get("id")
        sp, cp, gk = sp_cp_gk_validation(data)
        desc = data.get('desc').strip()
        ed = date_validation(data.get('ed'))
        profit = sp - cp
        sql = 'UPDATE balance_price set selling_price=%s, cost_price=%s, ghar_kharch=%s, profit = %s ,description = %s where id  = %s'
        cur.execute(sql, (sp, cp, gk, profit, desc, id))
        conn.commit()
        res = fetch_balance_price_data(ed)
        return jsonify(res)
    except Exception as e:
        raise e

@app.route("/purchase_table_edit", methods=['GET', 'POST'])
def purchase_table_edit():
    try:
        if request.json:
            conn, cur = create_comection()
            data = request.json
            id = data.get("id")
            amt = purchase_validation(data.get('purchase'))
            desc = data.get('desc').strip()
            sc_date = date_validation(data.get('sc_date'))
            ec_date = date_validation(data.get('ec_date'))
            sql = "UPDATE purchase_details SET  purchase_amount=%s, `desc`=%s  WHERE id=%s;"
            cur.execute(sql, (amt, desc, id))
            conn.commit()
            start_date_1, end_date_1 = date_compare(sc_date, ec_date)
            if config.PASSED_LAST_DATE == 'exclude':
                res = end_date_1 - start_date_1
            else:
                end_date_1 = end_date_1 + datetime.timedelta(days=1)
                res = end_date_1 - start_date_1
            tuple_dr = tuple(dates_range2(res.days, start_date_1))
            res =fetch_purchase_data(tuple_dr,sc_date,ec_date)
            print(res)
            return jsonify(res)
    except Exception as e:
        raise e
    
@app.route("/paid_table_edit", methods=['GET', 'POST'])
def paid_table_edit():
    try:
        if request.json:
            conn, cur = create_comection()
            data = request.json
            id = data.get("id")
            amt = purchase_validation(data.get('paid'))
            desc = data.get('desc').strip()
            sc_date = date_validation(data.get('sc_date'))
            ec_date = date_validation(data.get('ec_date'))
            sql = "UPDATE amount_paid_details SET  amount_paid=%s, `desc`=%s  WHERE id=%s;"
            cur.execute(sql, (amt, desc, id))
            conn.commit()
            start_date_1, end_date_1 = date_compare(sc_date, ec_date)
            if config.PASSED_LAST_DATE == 'exclude':
                res = end_date_1 - start_date_1
            else:
                end_date_1 = end_date_1 + datetime.timedelta(days=1)
                res = end_date_1 - start_date_1
            tuple_dr = tuple(dates_range2(res.days, start_date_1))
            res =fetch_paid_data(tuple_dr,sc_date,ec_date)
            print(res)
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
            ed = date_validation(data.get('ed'))
            desc = data.get('desc').strip()
            profit = sp - cp
            time_of_inserting = time.strftime("%I:%M %p")
            sql = 'INSERT INTO balance_price (selling_price, cost_price, ghar_kharch, profit,date,time,description)VALUES (%s, %s, %s, %s,%s, %s, %s)'
            cur.execute(sql, (sp, cp, gk, profit, ed, time_of_inserting, desc))
            conn.commit()
            cur.close()
            conn.close()
            res = fetch_balance_price_data(ed)
            return jsonify(res)
    except Exception as e:
        raise e

@app.route("/purchase_table_add", methods=['GET', 'POST'])
def purchase_table_add():
    try:
        if request.json:
            conn, cur = create_comection()
            data = request.json
            amt = purchase_validation(data.get('purchase'))
            ed = date_validation(data.get('ed'))
            desc = data.get('desc').strip()
            time_of_inserting = time.strftime("%I:%M %p")
            sql= "INSERT INTO purchase_details (`date`, `time`, purchase_amount, `Full paid`, `desc`) VALUES(%s, %s, %s, 0, %s);"
            cur.execute(sql, (ed, time_of_inserting, amt, desc))
            conn.commit()
            cur.close()
            conn.close()
            res =fetch_purchase_data((ed,),ed,ed)
            print(res)
            return jsonify(res)
    except Exception as e:
        raise e
    
@app.route("/paid_table_add", methods=['GET', 'POST'])
def paid_table_add():
    try:
        if request.json:
            conn, cur = create_comection()
            data = request.json
            amt = purchase_validation(data.get('paid'))
            ed = date_validation(data.get('ed'))
            desc = data.get('desc').strip()
            time_of_inserting = time.strftime("%I:%M %p")
            sql = "INSERT INTO amount_paid_details (`date`, `time`, amount_paid, `desc`) VALUES(%s, %s, %s, %s);"
            cur.execute(sql, (ed, time_of_inserting, amt, desc))
            conn.commit()
            cur.close()
            conn.close()
            res =fetch_paid_data((ed,),ed,ed)
            print(res)
            return jsonify(res)
    except Exception as e:
        raise e


# driver function
if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1',port=5002)

