
function date_validation(input_date) {
    let cd_date = new Date(input_date.split("/")[2], input_date.split("/")[1] - 1, input_date.split("/")[0])
    let td_date = new Date()
    if (input_date === "" & input_date.trim().length == 0) {
        window.alert("Please enter  a date")
        window.location.reload();
    }
    else if (cd_date > td_date) {
        window.alert("please don't enter future dates")
        window.location.reload();
    }
}


function date_compare(start_date, end_date){
    date_validation(start_date)
    date_validation(end_date)
    let s_date = new Date(start_date.split("/")[2], start_date.split("/")[1] - 1, start_date.split("/")[0])
    let e_date = new Date(end_date.split("/")[2], end_date.split("/")[1] - 1, end_date.split("/")[0])
    if(s_date > e_date){
        window.alert("Please enter proper dates")
        window.location.reload();
    }
}


function date_to_string(date) {
    return [date.getDate(), date.getMonth() + 1, date.getFullYear()].join('/')
}
