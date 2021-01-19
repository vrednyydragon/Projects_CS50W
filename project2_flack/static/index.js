//C:\Alex\projects\CS50's_Web_with_Py_and_JS\projects\project2\static\index.js
var temp_buffer;
document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {
    //registration window of user
        console.log("start");
        if (!localStorage.getItem("user_name")){ 
            $("#allinterface").hide()
        }
        else{
            document.getElementById("username_in_head").innerHTML = localStorage.getItem('user_name');
        }

        $("#register_btn").on('click',()=>{
            var user_name_input = btn_inputFunction()
            localStorage.setItem('tmp_user_name', user_name_input)
            // console.log(user_name_input)
            if(user_name_input == "" ){
                alert("empty string");
            }
            else {
                socket.emit('new user is login', {'new_user': user_name_input});
            }
        }) 

        // logout user
        $('#btn_logout').on("click",()=> {
            var logout_btn_res = confirm("Do you realy want leave?")
            if (logout_btn_res == true){
                // alert("you leaved chat")
                socket.emit('delete user from users list',{'logout_user': localStorage.getItem("user_name")});
                // localStorage.removeItem("user_name")
                localStorage.clear()
                $("#allinterface").hide()
                $("#input_window").show();
            }
        })


        // write the channel name in the input line
        $('#input_channel').on("keyup", (key) => {
            if (key.keyCode==13 && $('#input_channel').val()!="") {
                socket.emit('submit channel', {
                    'selection': $('#input_channel').val()//selection
                });
            };
        });

        // make one channel active by click and save it in localStorage
        $('#channel_list').on("click","button", function() {
            $('button').removeClass('active');
            this.className += " active";
            // console.log(this)
            var value =  $(this).attr('id')
            // console.log(value)
            var active_channel = localStorage.setItem("active_channel", value)
            clear_messages_block()
            socket.emit('one channel data', {'active_channel': localStorage.getItem("active_channel")
            });
        });

        // messages block
        $('#input_message').on("keyup", (key) => {
            if (key.keyCode==13 && $('#input_message').val()!="") {
                const user_name = localStorage.getItem("user_name")
                const data_time = new Date().toLocaleString()
                const fix_active_channel = localStorage.getItem("active_channel")
                socket.emit('submit message', {
                    'print_name': user_name, 
                    'print_date':data_time, 
                    'print_message': $('#input_message').val(),
                    'message_type': "text",
                    'fix_active_channel': fix_active_channel});
            };
        });

        // loading file by user to the chat 
        $('#send_file').on("change", function() {
            if($("#send_file").val() != ""){
                var file = $("#send_file").get(0).files[0];
                    const user_name = localStorage.getItem("user_name")
                    const data_time = new Date().toLocaleString()
                    const fix_active_channel = localStorage.getItem("active_channel")
                    socket.emit('try_upload_file', { 
                                'file_name': file["name"],
                                'file_size': file["size"],
                                'file_type': file["type"],
                                'file_data': file,//arrayBuffer,
                                'fix_active_channel': fix_active_channel,
                                'print_name': user_name,
                                'print_date': data_time,
                                'message_type': "file"
                    });
            }
            else{
                console.log("no file") 
            }
        });

        $('#displayed_messages').on("click", "button", function(){
            var name_file = this.id 
            // console.log(this)
            var download_window = confirm("Do you realy want download this file " + 
                name_file +"?");
            if(download_window){
                socket.emit("I need file", {"name_file":name_file, 
                                            'fix_active_channel': localStorage.getItem("active_channel")})
            }
        });

        $("#displayed_messages").on("click", "img", function(){    // Событие клика на маленькое изображение
            console.log("нажали на картинку")
            var img = $(this);    // Получаем изображение, на которое кликнули
            var src = img.attr('src'); // Достаем из этого изображения путь до картинки
            $("body").append("<div class='popup'>"+ //Добавляем в тело документа разметку всплывающего окна
                            "<div class='popup_bg'></div>"+ // Блок, который будет служить фоном затемненным
                            "<img src='"+src+"' class='popup_img' />"+ // Само увеличенное фото
                            "</div>");
            $(".popup").fadeIn(800); // Медленно выводим изображение
            $(".popup_bg").click(function(){    // Событие клика на затемненный фон      
                $(".popup").fadeOut(800);    // Медленно убираем всплывающее окно
                setTimeout(function() {    // Выставляем таймер
                    $(".popup").remove(); // Удаляем разметку всплывающего окна
                    }, 800);
            });
        });
    });

    //существует ли имя пользователя в списке
    socket.on('user exists alert', data=> {
        // console.log(data);
        if (!data){
            alert("User with this name exists!");
        }
        else{
            $("#input_window").hide();
            $("#allinterface").show();
            localStorage.setItem('user_name', localStorage.getItem('tmp_user_name'));
            document.getElementById("username_in_head").innerHTML = localStorage.getItem('user_name');
            localStorage.setItem('tmp_user_name', null);
        }
    })

    // for one channel messages
    socket.on('load one channel', data=> {
        // console.log(data);
        console.log(data["one_channel_data"]);
        clear_messages_block()
        for (n in data["one_channel_data"]){
            console.log(data["one_channel_data"][n])
            console.log(data["one_channel_data"][n]['file']);
            if (data["one_channel_data"][n]['message_type'] == 'file'){
               load_existing_messages(data["one_channel_data"][n], data["one_channel_data"][n]['file'])
            }
            else{
                load_existing_messages(data["one_channel_data"][n])
            }
        }
    });

    //load existing channels & messages after reloading page
    socket.on('load existing channels', data=> {
        // console.log(data['existing_channels'])
        if (!localStorage.getItem("user_name")){ 
            $("#allinterface").hide()
        }
        else{
            $("#input_window").hide()
        }
        //load existing channels
        $('#channel_list button').remove();
        for (channel in data['existing_channels']){
            btn_for_channel(channel)
        }
        //show active channel after reload
        $('#'+localStorage.getItem("active_channel")).click()
        clear_messages_block()
        var active_channel = localStorage.getItem("active_channel")
        for (channel in data['existing_channels']){
            if (data['existing_channels'][channel] == active_channel){ 
                console.log(data['existing_channels'][channel])
                load_existing_messages(data['existing_channels'][channel])     
            }
        }
    });
    // add channel into channel list 
    socket.on('announce channel', data => {
         $('#input_channel').val("")
        btn_for_channel(`${data.selection}`) 
    });
     // When a new message is announced, add to the displayed_messages
    socket.on('announce message', data => {
        $('#input_message').val("")
        const message_p = data['print_message'];
        const name_p = data['print_name'];
        const time_p = data['print_date'];
        const channel_p = data['fix_active_channel'];
        const message_type = data['message_type']
        if (channel_p == localStorage.getItem("active_channel")){
            messages_style(name_p,time_p,message_p,message_type)
        }
        else{
            console.log("message for NOT active channel")
        }
    });

    socket.on('channel exists alert', () => {
        alert("Channel with this name exists!")
    });
    
    //when new message appear in nonactive chat this chat is blincking
    socket.on('channel blincking', data => {
        console.log(data)
        if (data != localStorage.getItem("active_channel")){
            document.getElementById(data).className += " blink_channel";
        }

        $('#channel_list').on("click","button", function() {
            $(this).removeClass('blink_channel');
        });
    });

    //show file in message window
    socket.on('load file', data => {
        if (data["active_channel"] == localStorage.getItem("active_channel")){
            messages_style(data["print_name"], data["print_date"], 
                    data["file_name"], data['message_type'], data["file_type"], data["file"] )
        }
    });
    socket.on('send file from server', data => {
        console.log("file")
        var array = new Uint8Array(data["file"]);
        console.log("array" + array.length)
        var blob = new Blob([array], {type: data["file_type"]});
        var filename = data["file_name"];
        var file = new File([blob], filename, {type: data["file_type"]})
        var a = document.createElement("a");
        var url = URL.createObjectURL(blob);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);  
        }, 0);
    });
});

//channels style
function btn_for_channel(data){
    const button=document.createElement('button');
    button.className='btn btn-block text-center button1';
    button.id = data
    button.innerHTML= data;
    $('#channel_list').append(button);

}

//style for message that sent by me
function my_message(name_p,time_p,message_p,message_type, file_type = null, file = null){
    // show user name in message
    const div0 = document.createElement('div');
    div0.className='ml-auto';
    div0.setAttribute("style", "width: 60%;");
    const head_user=document.createElement('h6');
    head_user.className='text-right';
    head_user.setAttribute("style", "color: #4682B4; font-weight: bold;"); 
    head_user.id = name_p
    head_user.innerHTML = name_p
    // message
    const table1=document.createElement('table');
    table1.className='table';
    table1.setAttribute("style", "font-size: small; min-height: 10px "); 
    const tr1=document.createElement('tr');
    const td1=document.createElement('td');
    td1.bgColor = "#D9E0EB"
    td1.setAttribute("style","width: 80%")
    different_mess_view(message_type, td1, message_p, file_type, file)
    
    const td2=document.createElement('td');
    td2.className='align-text-top'
    td2.setAttribute("style", "color: gray; font-size:  x-small"); 
    td2.innerHTML = time_p

    tr1.appendChild(td1)
    tr1.appendChild(td2);
    table1.appendChild(tr1);
    div0.appendChild(head_user)
    div0.appendChild(table1)
    $('#displayed_messages').append(div0);
    $('#displayed_messages').scrollTop(500000);
}

//view of message by other users
function others_message(name_p,time_p,message_p,message_type, file_type = null, file = null){
    // show user name in message
    const div0 = document.createElement('div');
    div0.setAttribute("style", "width: 60%;");
    const head_user=document.createElement('h6');
    head_user.setAttribute("style", "color: #4682B4; font-weight: bold;"); 
    head_user.id = name_p
    head_user.innerHTML = name_p
     //time 
    const td2=document.createElement('td');
    td2.className='align-text-top'
    td2.setAttribute("style", "color: gray; font-size:  x-small"); 
    td2.innerHTML = time_p
    // message
    const table1=document.createElement('table');
    table1.className='table';
    table1.setAttribute("style", "font-size: small; min-height: 10px "); 
    const tr1=document.createElement('tr');
    const td1=document.createElement('td');
    td1.bgColor = "#D9E0EB"
    td1.setAttribute("style","width: 80%")
    different_mess_view(message_type, td1, message_p, file_type, file)
    
    tr1.appendChild(td2)
    tr1.appendChild(td1);
    table1.appendChild(tr1);
    div0.appendChild(head_user)
    div0.appendChild(table1)
    $('#displayed_messages').append(div0);
    $('#displayed_messages').scrollTop(500000);
}

//load existing messages
function load_existing_messages(data, file=null){
    console.log(data)
    console.log(file)
    var i=0;
    console.log("message <" +data['message'] + ">");
    if (data.length !=0){
        const name_p = data['user']
        const time_p = data['data']
        const message_p = data['message']
        const message_type = data['message_type']
        var file_size =null
        var file_type =null
        if(message_type == "file"){
                file_size = data['file_info']['file_size']
                file_type = data['file_info']['file_type']
        }
        messages_style(name_p, time_p, message_p, message_type, file_type, file)
    }
}

function messages_style(name_p,time_p,message_p,message_type, file_type = null, file = null){
    console.log(name_p,time_p,message_p,message_type, file_type, file)
    if (name_p != localStorage.getItem("user_name")){
        others_message(name_p,time_p,message_p,message_type, file_type, file)
    }
    else{
        my_message(name_p,time_p,message_p,message_type, file_type, file)
    }
}

function clear_messages_block(){
    var container = document.getElementById('displayed_messages');
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
}

function login_form(){
    const div_cont = document.createElement('div');
    div_cont.id = "input_window"
    div_cont.className='container border rounded m-auto shadow';
    const paragraph = document.createElement('p');
    paragraph.innerHTML = "Please fill in this form to login or enter to Flack"
    const input_form = document.createElement('input');
    input_form.id = "input_form"
    input_form.setAttribute("type", "text;");
    input_form.setAttribute("placeholder", "Enter your name");
    input_form.setAttribute("name", "name");
    const button = document.createElement('button');
    button.id = "register_btn"
    button.setAttribute("type", "button");
    button.className='btn btn-secondary'
    // button.setAttribute("class", "btn btn-secondary");
    button.innerHTML = "Login"
    div_cont.appendChild(paragraph)
    div_cont.appendChild(input_form)
    div_cont.appendChild(button)
    document.body.prepend(div_cont); 
}

function btn_inputFunction(){
    var input_name = document.getElementById("input_form").value;
    return input_name
}

function download_file_view(tag, filename){
    // console.log("filename" + filename)
    const div1 = document.createElement('div');
    div1.className='div1'
    const div2 = document.createElement('div');
    const button=document.createElement('button');
    button.className='btn-sm btn-light btn_show_file';
    button.id =  filename;
    const div3 = document.createElement('div');
    div3.className='div1'
    const p = document.createElement('p');
    p.innerHTML = filename

    div2.appendChild(button)
    div3.appendChild(p)
    div1.appendChild(div2)
    div1.appendChild(div3)
    tag.appendChild(div1)
}
// view message if it is a picture
function img_message_view(tag, filename, file_type, file){
    console.log(file)
    const div1 = document.createElement('div');
    const img = new Image();
    img.id =  filename;
    var blob = new Blob( [ file ], { type: file_type } );
    var urlCreator = window.URL || window.webkitURL;
    var imageUrl = urlCreator.createObjectURL( blob );
    img.src = imageUrl;
    img.setAttribute("style", "width: 100%");
    div1.appendChild(img)
    tag.appendChild(div1)
}
// for different type of messages function
function different_mess_view(message_type, td1, message_p, file_type, file){
    if (message_type == "text"){
        td1.innerHTML = message_p;
    }
    else{
        if (file_type == 'image/png' || file_type == 'image/jpeg'){
            img_message_view(td1, message_p, file_type, file)
        }
        else{
            download_file_view(td1, message_p)
        }
    }
}