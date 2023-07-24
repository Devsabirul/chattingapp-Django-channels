const message_form = $("#message_form");
const input_message = $("#message_input");
let message_body = $('#message_body');
const sender_id = JSON.parse(document.getElementById('json-sender-id').textContent);
const receiver_username = JSON.parse(document.getElementById('json-receiver-username').textContent);
const sender_avatar = JSON.parse(document.getElementById('json-sender-avatar').textContent);
const receiver_avatar = JSON.parse(document.getElementById('json-receiver-avatar').textContent);

// get url -----------------------------
let loc = window.location;
let wsStart = 'ws://';
if (loc.protocol === 'https') {
    wsStart = 'wss://';
}

let endpoint = wsStart + loc.host + loc.pathname;


let socket = new WebSocket(endpoint)
socket.onopen = function (e) {
    console.log("webSocket connected...", e)
}

socket.onmessage = function (e) {
    console.log("webSocket received...", e)
    let data = JSON.parse(e.data)
    let message = data.message;
    let sender_id = data.sender_id;
    newMessage(message, sender_id)
}


socket.onerror = function (e) {
    console.log("webSocket errors...", e)
}

socket.onclose = function (e) {
    console.log("webSocket close...")
}



message_form.on('submit', function (e) {
    e.preventDefault();

    let message = input_message.val();

    if (message.trim() !== '') { // Check if message is not empty or only whitespace
        let data = {
            'message': message,
            'sender_id': sender_id,
            'receiver_username': receiver_username
        };

        data = JSON.stringify(data);
        socket.send(data);
        $(this)[0].reset();
    }
});



// msg added function  --------------------
function newMessage(message, sent_by_id) {
    if ($.trim(message) === '') {
        return false;
    }
    if (sent_by_id == sender_id) {
        message_element = `
                <div class="d-flex align-items-baseline pt-1 text-end justify-content-end">
                <div class="pe-2" style="margin-right: 0.5rem !important;">
                    <div>
                        <div class="card card-text d-inline-block p-2 px-3 m-1"
                            style="text-align: justify;line-height: 20px;background: #4FBC87;color: white;">
                            ${message}
                        </div>
                    </div>
                    <div>
                        <div class="small" style="font-size: 10px;">
                            01:20PM</div>
                    </div>
                </div>
                <div class="position-relative avatar_">
                    <img src="${sender_avatar}"
                        class="img-fluid" alt="">
                    <span
                        class="position-absolute bottom-0 start-100 translate-middle p-1 bg-success border border-light rounded-circle">
                        <span class="visually-hidden">New alerts</span>
                    </span>
                </div>
            </div>   
        `
    } else {
        message_element = `
            <div class="d-flex align-items-baseline">
            <div class="position-relative avatar_">
                <img src="${receiver_avatar}"
                    class="img-fluid " alt="">
                <span
                    class="position-absolute bottom-0 start-100 translate-middle p-1 bg-success border border-light rounded-circle">
                    <span class="visually-hidden">New alerts</span>
                </span>
            </div>
            <div class="pe-2" style="margin-right: 0.5rem !important;">
                <div style="margin-left: 5px;">
                    <div class="card card-text d-inline-block p-2 px-3 m-1"
                        style="text-align: justify;line-height: 18px;background: #EFEEF4;color: #5e5e5e;">
                        ${message}
                    </div>
                </div>
                <div>
                    <div class="small" style="font-size: 10px;margin-left: 5px;">01:10PM</div>
                </div>
            </div>
        </div>
        `
    }

    message_body.append($(message_element))

    // Animate scrolling to the bottom
    message_body.animate({
        scrollTop: message_body[0].scrollHeight
    }, 1000);

    input_message.val(null);
}