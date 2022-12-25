// const host = 'https://balanceapp.pythonanywhere.com/'
const host = 'http://127.0.0.1:5002/'


function sp_cp_gk_validation(sp, cp, gk) {
    if ((sp === "" & sp.trim().length == 0) & (cp === "" & cp.trim().length == 0) & (gk === "" & gk.trim().length == 0)) {
        console.log("all are empty")
        window.alert("Please enter something")
        document.getElementById("add-sp").value = ""
        document.getElementById("add-cp").value = ""
        document.getElementById("add-gk").value = ""
    }

}


function fetch_PP_table(data) {
    document.getElementById("PP_search_date").value = data["date_2"]
    document.getElementById("PP_add_ed").value = data["curr_date"]
    document.getElementById("PP_balance").innerHTML = `<h3>Balance: ${data["balance"]}</h3>`
    if (data["l1"].length > 0) {
        let d = []
        for (let num = 0; num < data["l1"].length; num++) {
            d += `<tr>
            <td><button type="button" onclick="PP_edit_load(id=${data['l1'][num]['id']},sp=${data['l1'][num]['selling_price']},cp=${data['l1'][num]['cost_price']},gk=${data['l1'][num]['ghar_kharch']},profit=${data['l1'][num]['profit']},desc='${data['l1'][num]['desc']}',c_date='${data['date_2']}')"  data-toggle="modal" data-target="#modal-xl" ><i class="fa-solid fa-pen"></i></button>
            <button type="button"  onclick="PP_del_load(${data['l1'][num]['id']},'${data['date_2']}')" data-toggle="modal" data-target="#modal-sm"><i class="fa-solid fa-trash"></i></button></td>
                <td style="height: 78px; font-size: larger;">${data['l1'][num]['selling_price']}</td>
                <td style="height: 78px; font-size: larger;">${data['l1'][num]['cost_price']}</td>
                <td style="height: 78px; font-size: larger;">${data['l1'][num]['profit']}</td>
                <td style="height: 78px; font-size: larger;">${data['l1'][num]['ghar_kharch']}</td>
                <td style="height: 78px; font-size: larger;">${data['l1'][num]['desc']}</td>

            </tr>`
        }
        d += `<tr>
        <td></td>
                <td style="height: 78px; font-size: larger;">T = ${data['sp']}</td>
                <td style="height: 78px; font-size: larger;">T = ${data['cp']}</td>
                <td style="height: 78px; font-size: larger;">T = ${data['pf']}</td>
                <td style="height: 78px; font-size: larger;">T = ${data['gk']}</td>
        <td></td>
            </tr>`
        document.getElementById("PP_table_rows").innerHTML = d
        document.getElementById("PP_balance").innerHTML = `<h3>Balance: ${data["balance"]}</h3>`
    }
    else {
        document.getElementById("PP_table_rows").innerHTML = ''
        document.getElementById("PP_search_message").innerHTML = `<h3>No records found </h3>`

    }
}


async function PP_tables() {
    try {
        event.preventDefault();
        console.log("hello")
        let PP_search_date = document.getElementById("PP_search_date").value
        date_validation(PP_search_date)
        const all_data = {
            c_date: PP_search_date
        };
    
        const response = await axios.post(host, all_data);
        console.log(response)
        const data = response.data
        fetch_PP_table(data)
    } catch (errors) {
        console.log(errors["message"]);
        const message = errors["message"]
        document.getElementById('PP_search_message').innerHTML = `<p>${message}</p>`
    }
}

async function PP_price_entry() {
    try {
        event.preventDefault();
        const ed = document.getElementById("PP_add_ed").value
        const sp = document.getElementById("PP_add_sp").value
        const cp = document.getElementById("PP_add_cp").value
        const gk = document.getElementById("PP_add_gk").value
        const desc = document.getElementById("PP_add_desc").value
        sp_cp_gk_validation(sp,cp,gk)
        date_validation(ed)
        const prices = { sp: sp, cp: cp, gk: gk, ed: ed, desc: desc};
    
        console.log(prices)
        const response = await axios.post(host + 'personal_purchase_table_add', prices);
        const data = response.data
        fetch_PP_table(data)
        document.getElementById("PP_add_sp").value = ""
        document.getElementById("PP_add_cp").value = ""
        document.getElementById("PP_add_gk").value = ""
        document.getElementById("PP_add_desc").value = ""
        document.getElementById("PP_add_ed").value = date_to_string(new Date())
        document.getElementById('PP_add_message').value=""
        document.getElementById("PP_close_add_modal").click()
    } catch (errors) {
        console.log(errors["message"]);
        const message = errors["message"]
        document.getElementById('PP_add_message').innerHTML = `<p>${message}</p>`
    }

}


function PP_del_load(id, c_date) {
 document.getElementById("PP_delete").innerHTML = `<button type="submit" onclick="PP_delete(${id},'${c_date}')" class="btn btn-default">Yes</button>`
}

async function PP_delete(id, c_date) {
    try {
        event.preventDefault();
        const prices = {id: id,c_date: c_date};
    
        const response = await axios.post(host + 'personal_purchase_table_delete', prices);
        console.log(response)
        const data = response.data
        fetch_PP_table(data)
        document.getElementById("PP_close_delete_modal").click()

    } catch (errors) {
        console.log("errors", errors);
        const message = errors["message"]
        document.getElementById('PP_del_message').innerHTML = `<p>${errors["message"]}</p>`
    }
}


function PP_edit_load(id, sp, cp, gk, profit, desc, c_date) {
    console.log("hello", id, sp, cp, gk, profit, c_date,desc)
    document.getElementById("PP_update_sp").value = sp
    document.getElementById("PP_update_cp").value = cp
    document.getElementById("PP_update_gk").value = gk
    document.getElementById("PP_update_desc").value = desc
    document.getElementById("PP_update").innerHTML = `<button type="submit" onclick="PP_update(${id},'${c_date}')" class="btn btn-default">Submit</button>`

}

async function PP_update(id, c_date) {
    try {
        event.preventDefault();
        console.log(c_date)
        const sp = document.getElementById("PP_update_sp").value
        const cp = document.getElementById("PP_update_cp").value
        const gk = document.getElementById("PP_update_gk").value
        const desc = document.getElementById("PP_update_desc").value
        sp_cp_gk_validation(sp,cp,gk)
        const prices = {sp: sp,cp: cp,gk: gk,id: id,ed: c_date,desc: desc};

    
        const response = await axios.post(host + 'personal_purchase_table_edit', prices);
        const data = response.data
        fetch_PP_table(data)
        document.getElementById("PP_close_update_modal").click()

    } catch (errors) {
        console.log(errors["message"]);
        document.getElementById('PP_update_message').innerHTML = `<p>${errors["message"]}</p>`
    }

}

async function PP_result() {
    try {
        event.preventDefault();
        const s_date = document.getElementById("PP_s_date").value
        const e_date = document.getElementById("PP_e_date").value
        date_compare(s_date, e_date)
        const r_data = { s_date: s_date,e_date: e_date};

        const response = await axios.post(host + 'personal_purchase_table_results', r_data);
        const data = response.data
        document.getElementById("PP_s_date").value = s_date
        document.getElementById("PP_e_date").value = e_date

        document.getElementById("PP_res_head").innerHTML = `<h3>${data['month']}</h3>`
        document.getElementById("PP_res_sp").innerHTML = `<span class="info-box-number">${data['sum_sp']}</span>`
        document.getElementById("PP_res_cp").innerHTML =`<span class="info-box-number">${data['sum_cp']}</span>`
        document.getElementById("PP_res_gk").innerHTML = `<span class="info-box-number">${data['sum_gk']}</span>`
        document.getElementById("PP_res_profit").innerHTML = `<span class="info-box-number">${data['profit']}</span>`
        document.getElementById("PP_res_balance").innerHTML = `<span class="info-box-number">${data['balance']}</span>`
        document.getElementById('PP_res_message').value = ''

    } catch (errors) {
        console.log("errors", errors);
        const message = errors["message"]
        document.getElementById('PP_res_message').innerHTML = `<p>${errors["message"]}</p>`
    }
}







