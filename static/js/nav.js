function add_btn(){
    document.querySelector('#add_div').style.display = 'block';
    document.querySelector('#task_div').style.display = 'none';
}

function close_modal(){
    document.querySelector('#add_div').style.display = 'none'
    document.querySelector('#task_div').style.display = 'block';
}