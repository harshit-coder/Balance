// const host = 'https://balanceapp.pythonanywhere.com/'
// const host = 'http://127.0.0.1:5002/'


function fetch_PA_table(data) {
document.getElementById("PA_start_search_date").value = data["s_date"]
document.getElementById("PA_end_search_date").value = data["e_date"]
document.getElementById("PA_add_ed").value = data["curr_date"]

if (data["l1"].length > 0) {
    let d = []
    for (let num = 0; num < data["l1"].length; num++) {
        d += `<tr>
        <td><button type="button" onclick="PA_edit_load(id=${data['l1'][num]['id']},paid=${data['l1'][num]['paid']},desc='${data['l1'][num]['desc']}',sc_date='${data['s_date']}',ec_date='${data['e_date']}')"  data-toggle="modal" data-target="#modal-xl" ><i class="fa-solid fa-pen"></i></button>
        <button type="button"  onclick="PA_del_load(${data['l1'][num]['id']},'${data['s_date']}','${data['e_date']}')" data-toggle="modal" data-target="#modal-sm"><i class="fa-solid fa-trash"></i></button></td>
            <td style="height: 78px; font-size: larger;">${data['l1'][num]['date']}</td>
            <td style="height: 78px; font-size: larger;">${data['l1'][num]['paid']}</td>
            <td style="height: 78px; font-size: larger;">${data['l1'][num]['desc']}</td>

        </tr>`
    }
 
    document.getElementById("PA_table_rows").innerHTML = d
}
else {
    document.getElementById("PA_table_rows").innerHTML = ''
    document.getElementById("PA_search_message").innerHTML = `<h3>No records found </h3>`

}
}


async function PA_tables() {
try {
    event.preventDefault();
    console.log("hello")
    const PA_start_search_date = document.getElementById("PA_start_search_date").value
    const PA_end_search_date = document.getElementById("PA_end_search_date").value

    date_compare(PA_start_search_date, PA_end_search_date)
    const all_data = {
        sc_date: PA_start_search_date,
        ec_date: PA_end_search_date
    };

    const response = await axios.post(host +"paid", all_data);
    console.log(response)
    const data = response.data
    fetch_PA_table(data)
} catch (errors) {
    console.log(errors["message"]);
    const message = errors["message"]
    document.getElementById('PA_search_message').innerHTML = `<p>${message}</p>`
}
}

async function PA_paid_entry() {
try {
    event.preventDefault();
    const ed = document.getElementById("PA_add_ed").value
    const paid = document.getElementById("PA_add_paid").value
    const desc = document.getElementById("PA_add_desc").value
    purchase_validation(paid)
    date_validation(ed)
    const all_data = { paid: paid, ed: ed, desc: desc};
    console.log(all_data)
    const response = await axios.post(host + 'paid_table_add', all_data);
    const data = response.data
    fetch_PA_table(data)
    document.getElementById("PA_add_paid").value = ""
    document.getElementById("PA_add_desc").value = ""
    document.getElementById("PA_add_ed").value = date_to_string(new Date())
    document.getElementById('PA_add_message').value=""
    document.getElementById("PA_close_add_modal").click()
} catch (errors) {
    console.log(errors["message"]);
    const message = errors["message"]
    document.getElementById('PA_add_message').innerHTML = `<p>${message}</p>`
}

}


function PA_del_load(id, sc_date, ec_date) {
document.getElementById("PA_delete").innerHTML = `<button type="submit" onclick="PA_delete(${id},'${sc_date}','${ec_date}')" class="btn btn-default">Yes</button>`
}

async function PA_delete(id, sc_date, ec_date) {
try {
    event.preventDefault();
    const all_data = {id: id,sc_date: sc_date,ec_date: ec_date};

    const response = await axios.post(host + 'paid_table_delete', all_data);
    console.log(response)
    const data = response.data
    fetch_PA_table(data)
    document.getElementById("PA_close_delete_modal").click()

} catch (errors) {
    console.log("errors", errors);
    const message = errors["message"]
    document.getElementById('PA_del_message').innerHTML = `<p>${errors["message"]}</p>`
}
}


function PA_edit_load(id,paid, desc, sc_date, ec_date) {
document.getElementById("PA_update_paid").value = paid
document.getElementById("PA_update_desc").value = desc
document.getElementById("PA_update").innerHTML = `<button type="submit" onclick="PA_update(${id},'${sc_date}','${ec_date}')" class="btn btn-default">Submit</button>`

}

async function PA_update(id, sc_date, ec_date) {
try {
    event.preventDefault();
    const paid = document.getElementById("PA_update_paid").value
    const desc = document.getElementById("PA_update_desc").value
    purchase_validation(paid)
    const all_data = {paid: paid,id: id,desc: desc,sc_date: sc_date,ec_date: ec_date};


    const response = await axios.post(host + 'paid_table_edit', all_data);
    const data = response.data
    fetch_PA_table(data)
    document.getElementById("PA_close_update_modal").click()

} catch (errors) {
    console.log(errors["message"]);
    document.getElementById('PA_update_message').innerHTML = `<p>${errors["message"]}</p>`
}

}











