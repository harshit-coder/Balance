



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
