// get url -----------------------------
let loc = window.location;
let wsStart = 'ws://';
if (loc.protocol === 'https') {
    wsStart = 'wss://';
}

let endpoint = wsStart + loc.host + "/notification";

let socket = new WebSocket(endpoint)

socket.onopen = function (e) {
    console.log("websocket connect..");
}
socket.onmessage = function (e) {
    document.getElementById('notificatin_bell').classList.remove('d-none')
    document.getElementsByClassName('count_msg')
    console.log("Message recevied..", e);
}

socket.onclose = function (e) {
    console.log("websocket close..");
}