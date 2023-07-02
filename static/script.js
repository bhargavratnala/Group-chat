let msgbox = document.getElementById("msgbox");
let msgarea = document.getElementById("msgarea");
let disname = document.getElementById("name");
let count = document.getElementById("count");

let name = prompt("enter your name");
$.get(`/sendmsg/{{count}}/${name}`);
disname.innerHTML = name;

function sendmsg(){
    if(msgarea.value != ""){
        $.get(`/sendmsg/${count.value}/${msgarea.value}`);
        let send = document.createElement("div");
        send.innerHTML = `${msgarea.value}`;
        send.className = "msg sendmsg";
        msgbox.appendChild(send);
        msgarea.value = "";
    }
}

let recivecall = ()=>{
    fetch(`/msg/${count.value}`).then(response =>{
        response.json().then((data)=>{
            let recive = document.createElement("div");
            if(data.msg != ""){
                recive.innerHTML = data.msg;
                recive.className = "msg recivemsg";
                msgbox.appendChild(recive);
            }
            setTimeout(recivecall(), 500);
        })
    })
};

setTimeout(recivecall(), 500);

window.addEventListener("beforeunload",()=>{
    $.get(`/sendmsg/{{count}}/exit`);
})