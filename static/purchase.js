// const host = 'https://balanceapp.pythonanywhere.com/'
const host = 'http://127.0.0.1:5002/'


function purchase_validation(purchase){
        if ((purchase === "" & purchase.trim().length == 0)) {
        console.log("purchases can't be empty")
        window.alert("Please enter something")
        document.getElementById("PUR_add_purchase").value = ""
 
    }
}

function fetch_PUR_table(data) {
    document.getElementById("PP_start_search_date").value = data["s_date_2"]
    document.getElementById("PP_end_search_date").value = data["e_date_2"]
    document.getElementById("PUR_add_ed").value = data["curr_date"]
    document.getElementById("PUR_TO_PAY").innerHTML = `<h3>Balance: ${data["balance"]}</h3>`
    document.getElementById("PUR_PAID_EXTRA").innerHTML = `<h3>Balance: ${data["balance"]}</h3>`

    if (data["l1"].length > 0) {
        let d = []
        for (let num = 0; num < data["l1"].length; num++) {
            d += `<tr>
            <td><button type="button" onclick="PUR_edit_load(id=${data['l1'][num]['id']},purchase=${data['l1'][num]['purchase']},desc='${data['l1'][num]['desc']}',sc_date='${data['s_date_2']}',ec_date='${data['e_date_2']}')"  data-toggle="modal" data-target="#modal-xl" ><i class="fa-solid fa-pen"></i></button>
            <button type="button"  onclick="PUR_del_load(${data['l1'][num]['id']},'${data['s_date_2']}','${data['e_date_2']}')" data-toggle="modal" data-target="#modal-sm"><i class="fa-solid fa-trash"></i></button></td>
                <td style="height: 78px; font-size: larger;">${data['l1'][num]['date']}</td>
                <td style="height: 78px; font-size: larger;">${data['l1'][num]['purchase']}</td>
                <td style="height: 78px; font-size: larger;">${data['l1'][num]['to_pay']}</td>
                <td style="height: 78px; font-size: larger;">${data['l1'][num]['desc']}</td>

            </tr>`
        }
     
        document.getElementById("PUR_table_rows").innerHTML = d
    }
    else {
        document.getElementById("PUR_table_rows").innerHTML = ''
        document.getElementById("PUR_search_message").innerHTML = `<h3>No records found </h3>`

    }
}


async function PUR_tables() {
    try {
        event.preventDefault();
        console.log("hello")
        let PP_start_search_date = document.getElementById("PP_start_search_date").value
        let PP_end_search_date = document.getElementById("PP_end_search_date").value

        date_compare(PP_start_search_date, PP_end_search_date)
        const all_data = {
            sc_date: PP_start_search_date,
            ec_date: PP_end_search_date
        };
    
        const response = await axios.post(host, all_data);
        console.log(response)
        const data = response.data
        fetch_PUR_table(data)
    } catch (errors) {
        console.log(errors["message"]);
        const message = errors["message"]
        document.getElementById('PUR_search_message').innerHTML = `<p>${message}</p>`
    }
}

async function PUR_purchase_entry() {
    try {
        event.preventDefault();
        const ed = document.getElementById("PUR_add_ed").value
        const purchase = document.getElementById("PUR_add_purchase").value
        const desc = document.getElementById("PUR_add_desc").value
        purchase_validation(purchase)
        date_validation(ed)
        const prices = { purchase: purchase, ed: ed, desc: desc};
        console.log(prices)
        const response = await axios.post(host + 'personal_purchase_table_add', prices);
        const data = response.data
        fetch_PP_table(data)
        document.getElementById("PUR_add_purchase").value = ""
        document.getElementById("PUR_add_desc").value = ""
        document.getElementById("PUR_add_ed").value = date_to_string(new Date())
        document.getElementById('PUR_add_message').value=""
        document.getElementById("PUR_close_add_modal").click()
    } catch (errors) {
        console.log(errors["message"]);
        const message = errors["message"]
        document.getElementById('PUR_add_message').innerHTML = `<p>${message}</p>`
    }

}


function PUR_del_load(id, sc_date, ec_date) {
 document.getElementById("PP_delete").innerHTML = `<button id="button_delete" type="submit" onclick="PP_delete(${id},'${sc_date}','${ec_date}')" class="btn btn-default">Yes</button>`
}

async function PUR_delete(id, sc_date, ec_date) {
    try {
        event.preventDefault();
        const prices = {id: id,sc_date: sc_date,ec_date: ec_date};
    
        const response = await axios.post(host + 'personal_purchase_table_delete', prices);
        console.log(response)
        const data = response.data
        fetch_PUR_table(data)
        document.getElementById("PUR_close_delete_modal").click()

    } catch (errors) {
        console.log("errors", errors);
        const message = errors["message"]
        document.getElementById('PUR_del_message').innerHTML = `<p>${errors["message"]}</p>`
    }
}


function PUR_edit_load(id,purchase, desc, sc_date, ec_date) {
    document.getElementById("PUR_update_purchase").value = purchase
    document.getElementById("PUR_update_desc").value = desc
    document.getElementById("PUR_update").innerHTML = `<button type="submit" onclick="PUR_update(${id},'${sc_date}','${ec_date}')" class="btn btn-default">Submit</button>`

}

async function PUR_update(id, sc_date, ec_date) {
    try {
        event.preventDefault();
        const purchase = document.getElementById("PUR_update_purchase").value
        const desc = document.getElementById("PUR_update_desc").value
        purchase_validation(purchase)
        const prices = {purchase: purchase,id: id,desc: desc,sc_date: sc_date,ec_date: ec_date};

    
        const response = await axios.post(host + 'personal_purchase_table_edit', prices);
        const data = response.data
        fetch_PUR_table(data)
        document.getElementById("PUR_close_update_modal").click()

    } catch (errors) {
        console.log(errors["message"]);
        document.getElementById('PUR_update_message').innerHTML = `<p>${errors["message"]}</p>`
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









