
async function PriceEntry () {
    event.preventDefault();
    const sp = document.getElementById("sp").value
    const cp = document.getElementById("cp").value
    const gk = document.getElementById("gk").value
    const ed = document.getElementById("entry_date").value
    console.log(typeof sp,sp)
    console.log(typeof cp,cp)
    console.log(typeof gk,gk)
    console.log(typeof ed,ed)
    ed_date = new Date(ed.split("/")[2],ed.split("/")[1]-1,ed.split("/")[0])
    td_date= new Date()
       if((sp==="") & (cp==="") & (gk==="")){
        console.log("all are empty")
        alert("Please enter something")
        document.getElementById("sp").value = ""
        document.getElementById("cp").value=""
        document.getElementById("gk").value=""
    }

    else if(ed_date > td_date){
    window.alert("please don't enter future dates")
    }
    else if(ed===""){
            console.log("please enter date")
        alert("Please enter date")
    }

    else{
    const prices = {
    sp: sp,
    cp: cp,
    gk: gk,
    ed:ed
    };
    console.log(prices)
    try {
        const response = await axios.post('https://dailybalanceapp.herokuapp.com/', prices);
        const data  = response.data
        console.log(`Added a new Todo!`,data['message']);
        document.getElementById('entry_result').innerHTML = data['message']
        document.getElementById("sp").value = ""
        document.getElementById("cp").value=""
        document.getElementById("gk").value=""
        document.getElementById("entry_date").value=data['date']
    } catch (errors) {
        console.log(errors);
        message = errors["message"]
        document.getElementById('entry_result').value = message
    }
    }
}


async function tables () {
    event.preventDefault();
    let c_date = document.getElementById("c_date").value

    console.log(c_date)
    cd_date = new Date(c_date.split("/")[2],c_date.split("/")[1]-1,c_date.split("/")[0])
    td_date= new Date()
    if(c_date===""){
        console.log("please enter something")
        alert("Please enter something")
    }
    else if(cd_date > td_date){
    window.alert("please don't enter future dates")

    }
    else{
        const all_data = {
    c_date: c_date,
    };
    console.log(all_data)

    try {
        const response = await axios.post('https://dailybalanceapp.herokuapp.com/table', all_data);
        const data = response.data
        console.log('Added a new Todo!', data);
        console.log(data["date_2"])
        document.getElementById("c_date").value = data["date_2"]
        if(data["l1"].length > 0){
                document.getElementById("balance").innerHTML =`<h4 >Balance:${data["balance"]}</h4>`
                document.getElementById("head").innerHTML=`<tr style="background-color: black;">
                        <th>SP</th>
                        <th>CP</th>
                        <th>GK</th>
                        <th>PR</th>
                        <th>Edit/Delete</th>
                    </tr>`
                let d =[]
                 for (let num = 0; num < data["l1"].length; num++)
                 {
                    d+=`<tr>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['selling_price'] }</td>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['cost_price'] }</td>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['profit'] }</td>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['ghar_kharch'] }</td>

                                <td><button type="button" onclick="edit(id=${ data['l1'][num]['id']},sp=${ data['l1'][num]['selling_price'] },cp=${ data['l1'][num]['cost_price'] },gk=${ data['l1'][num]['ghar_kharch'] },profit=${ data['l1'][num]['profit'] },c_date='${all_data['c_date']}')"  data-toggle="modal" data-target="#modal-xl" ><i class="fa-solid fa-pen"></i></button>
                        <button type="button"  onclick="del(${ data['l1'][num]['id']},'${data['date_2']}')" data-toggle="modal" data-target="#modal-sm"><i class="fa-solid fa-trash"></i></button></td>
                    </tr>`
                }
                document.getElementById("table").innerHTML=d
                   console.log(data['date_2'])
                }
        else{
        document.getElementById("balance").innerHTML =`<h4 >No record found</h4>`
        document.getElementById("head").innerHTML=``
        document.getElementById("table").innerHTML=``
        }



    } catch (errors) {
        console.error(errors);
    }
    }

}

async function result() {
    event.preventDefault();
    const s_date = document.getElementById("s_date").value
    const e_date = document.getElementById("e_date").value
    const td = new Date
    start_date = new Date(s_date.split("/")[2],s_date.split("/")[1]-1,s_date.split("/")[0])
    end_date= new Date(e_date.split("/")[2],e_date.split("/")[1]-1,e_date.split("/")[0])
    console.log(start_date,end_date)
    if((end_date<=start_date) | (s_date==="") | (e_date ==="")){
        console.log("start date is greater than end date")
        window.alert("please enter proper inputs, either field is empty or start date is greater than end_date")
        document.getElementById("s_date").value=""
        document.getElementById("e_date").value=""
    }
    else if(start_date>td){
        window.alert("please don't enter future dates")

    }
    else if(end_date>td){
        window.alert("please don't enter future dates")

    }
    else{

    console.log(s_date)
    console.log(e_date)
    const r_data = {
    s_date:s_date,
    e_date:e_date
    };
    console.log(r_data)
    try {
        const response = await axios.post('https://dailybalanceapp.herokuapp.com/result', r_data);
        const data = response.data
        console.log(`Added a new Todo!`, data);
        document.getElementById("s_date").value=s_date
        document.getElementById("e_date").value=e_date
        document.getElementById("res").innerHTML=`
              <h3>${data['month']}</h3>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3 col-sm-6 col-12">
                      <div class="info-box">
                        <span class="info-box-icon bg-info"><i class="far fa-envelope"></i></span>

                        <div class="info-box-content">
                          <span class="info-box-text">Selling price</span>
                          <span class="info-box-number">${data['sum_sp']}</span>
                        </div>
                        <!-- /.info-box-content -->
                      </div>
                      <!-- /.info-box -->
                    </div>
                    <!-- /.col -->
                    <div class="col-md-3 col-sm-6 col-12">
                      <div class="info-box">
                        <span class="info-box-icon bg-success"><i class="far fa-flag"></i></span>

                        <div class="info-box-content">
                          <span class="info-box-text">Cost Price</span>
                          <span class="info-box-number">${data['sum_cp']}</span>
                        </div>
                        <!-- /.info-box-content -->
                      </div>
                      <!-- /.info-box -->
                    </div>
                    <!-- /.col -->
                    <div class="col-md-3 col-sm-6 col-12">
                      <div class="info-box">
                        <span class="info-box-icon bg-warning"><i class="far fa-copy"></i></span>

                        <div class="info-box-content">
                          <span class="info-box-text">Ghar Kharch</span>
                          <span class="info-box-number">${data['sum_gk']}</span>
                        </div>
                        <!-- /.info-box-content -->
                      </div>
                      <!-- /.info-box -->
                    </div>
                    <!-- /.col -->
                    <div class="col-md-3 col-sm-6 col-12">
                      <div class="info-box">
                        <span class="info-box-icon bg-danger"><i class="far fa-star"></i></span>

                        <div class="info-box-content">
                          <span class="info-box-text">Profit</span>
                          <span class="info-box-number">${data['profit']}</span>
                        </div>
                        <!-- /.info-box-content -->
                      </div>
                      <!-- /.info-box -->
                    </div>
                    <!-- /.col -->
                     <div class="col-md-3 col-sm-6 col-12">
                      <div class="info-box">
                        <span class="info-box-icon bg-danger"><i class="far fa-star"></i></span>

                        <div class="info-box-content">
                          <span class="info-box-text">Balance</span>
                          <span class="info-box-number">${data['balance']}</span>
                        </div>
                        <!-- /.info-box-content -->
                      </div>
                      <!-- /.info-box -->
                    </div>
                  </div>

            </div>
         `

    } catch (errors) {
        console.error(errors);
    }
    }
}



function edit(id,sp,cp,gk,profit,c_date){
    console.log("hello",id,sp,cp,gk,profit,c_date)
            document.getElementById("sp").value = sp
        document.getElementById("cp").value=cp
        document.getElementById("gk").value=gk
        document.getElementById("update").innerHTML =`<button id="button_update" type="submit" onclick="update(${id},'${c_date}')" class="btn btn-default">Submit</button>`


}

function del(id,c_date){
    console.log("hello",id,c_date)
    document.getElementById("delete").innerHTML =`<button id="button_delete" type="submit" onclick="rem(${id},'${c_date}')" class="btn btn-default">Yes</button>`

}


async function rem(id,c_date){
    event.preventDefault();
    const prices = {
    id:id,
    c_date:c_date
    };
    console.log(prices)
    try {
        const response = await axios.post('https://dailybalanceapp.herokuapp.com/delete', prices);
        const data  = response.data
        console.log(`Added a new Todo!`,data);
         document.getElementById("balance").innerHTML =`<h4 >Balance:${data["balance"]}</h4>`
                document.getElementById("head").innerHTML=`<tr style="background-color: black;">
                        <th>SP</th>
                        <th>CP</th>
                        <th>GK</th>
                        <th>PR</th>
                        <th>Edit/Delete</th>
                    </tr>`
                let d =[]
                 for (let num = 0; num < data["l1"].length; num++)
                 {
                    d+=`<tr>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['selling_price'] }</td>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['cost_price'] }</td>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['profit'] }</td>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['ghar_kharch'] }</td>

                                <td><button type="button" onclick="edit(${ data['l1'][num]['id']},${ data['l1'][num]['selling_price'] },${ data['l1'][num]['cost_price'] },${ data['l1'][num]['ghar_kharch'] },${ data['l1'][num]['profit'] },'${c_date}')"  data-toggle="modal" data-target="#modal-xl" ><i class="fa-solid fa-pen"></i></button>
                        <button onclick="del(${ data['l1'][num]['id']},'${c_date}')" type="button" data-toggle="modal" data-target="#modal-sm"><i class="fa-solid fa-trash"></i></button></td>
                    </tr>`
                }
                document.getElementById("table").innerHTML=d
                document.getElementById("delete_no").click()

    } catch (errors) {
        console.log("errors",errors);
        message = errors["message"]
        document.getElementById('del_result').innerHTML = `<p>${errors["message"]}</p>`
    }
    }


async function update(id,c_date){
    event.preventDefault();
    const sp = document.getElementById("sp").value
    const cp = document.getElementById("cp").value
    const gk = document.getElementById("gk").value
    console.log(typeof sp,sp)
    console.log(typeof cp,cp)
    console.log(typeof gk,gk)
       if((sp==="0" | sp==="") & (cp==="0" | cp==="") & (gk==="0" | gk==="")){
        console.log("all are zero")
        alert("Please enter something")
        document.getElementById("sp").value = 0
        document.getElementById("cp").value=0
        document.getElementById("gk").value=0
    }

    else{
    const prices = {
    sp: sp,
    cp: cp,
    gk: gk,
    id:id,
    c_date:c_date
    };
    console.log(prices)
    try {
        const response = await axios.post('https://dailybalanceapp.herokuapp.com/edit', prices);
        const data  = response.data
        console.log(`Added a new Todo!`,data);
         document.getElementById("balance").innerHTML =`<h4 >Balance:${data["balance"]}</h4>`
                document.getElementById("head").innerHTML=`<tr style="background-color: black;">
                        <th>SP</th>
                        <th>CP</th>
                        <th>GK</th>
                        <th>PR</th>
                        <th>Edit/Delete</th>
                    </tr>`
                let d =[]
                 for (let num = 0; num < data["l1"].length; num++)
                 {
                    d+=`<tr>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['selling_price'] }</td>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['cost_price'] }</td>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['profit'] }</td>
                      <td style="height: 78px; font-size: larger;">${ data['l1'][num]['ghar_kharch'] }</td>

                                <td><button type="button" onclick="edit(${ data['l1'][num]['id']},${ data['l1'][num]['selling_price'] },${ data['l1'][num]['cost_price'] },${ data['l1'][num]['ghar_kharch'] },${ data['l1'][num]['profit'] },'${c_date}')"  data-toggle="modal" data-target="#modal-xl" ><i class="fa-solid fa-pen"></i></button>
                        <button onclick="delete(${ data['l1'][num]['id']},'${c_date}')" type="button" data-toggle="modal" data-target="#modal-sm"><i class="fa-solid fa-trash"></i></button></td>
                    </tr>`
                }
                document.getElementById("table").innerHTML=d
                document.getElementById("update_no").click()



    } catch (errors) {
        console.log(errors["message"]);
        document.getElementById('upd_result').innerHTML = `<p>${errors["message"]}</p>`
    }
    }

}
