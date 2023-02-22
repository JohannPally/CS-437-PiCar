document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "192.168.50.217";   // the IP address of your Raspberry PI

function client(input){
    
    const net = require('net');
    // var input = document.getElementById("message").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        let receivedData = data.toString();
        console.log(receivedData)
        let [orientation, distanceTravelled] = receivedData.split(",") 
        document.getElementById("direction").innerHTML = orientation
        document.getElementById("distance").innerHTML = Number(distanceTravelled).toFixed(2) + " cm"
        console.log(receivedData);
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        // send_data("87");
        client("w");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        // send_data("83");
        client("s");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        // send_data("65");
        client("a");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        // send_data("68");
        client("d");
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
}

window.onload = () => {
    // document.getElementById("direction")
}

// update data for every 50ms
function update_data(event){
    console.log(event)
    client(event.target.value);
}
