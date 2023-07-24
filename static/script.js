
now = Math.floor(Date.now() / 1000)
var ws = new WebSocket("ws://127.0.0.1:8000/ws/" + "${now}");
//const ws = new WebSocket("ws://" + window.location.host + "/ws/1");

ws.onmessage = function (event) {
    console.log(event.data)
    const data = JSON.parse(event.data);
    const message = data.server;
    const notificationContainer = document.getElementById("notification-container");
    const notificationItem = document.createElement("div");
    notificationItem.innerText = message;
    notificationContainer.appendChild(notificationItem);
};
