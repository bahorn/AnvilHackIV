var mode = "INSERT"

function event_handler(event) {
    var data = JSON.parse(event.data);
    console.log(data);
    mode = data['mode'];
    if (mode == "PREDICT") {
        // display the predictions
    } else if (mode == "INSERT") {
        
    }
    document.getElementById("mode").innerHTML = mode;
    var highlighted = data['line_text'][data['pos']-1];
    document.getElementById("commandPage").innerHTML = data['line'];
    document.getElementById("partCommand").innerHTML = data['progress'];
    var k = data['line_text'].substr(0, data['pos']-1);
    var l = data['line_text'].substr(data['pos'],data['line_text'].length);
    if (k == "undefined") {
        k = "";
    }
    if (l == "undefined") {
        l = "";
    }
    document.getElementById("command").innerHTML = k+"<mark>"+highlighted+"</mark>"+l;
    document.getElementById("output").innerHTML = data['last_output'];
}

function setup() {
    var ws = new WebSocket("ws://127.0.0.1:5678/");
    ws.onmessage = function (event) {
        event_handler(event);
    };
}


setup();
