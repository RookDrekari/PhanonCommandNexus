const terminal = new Terminal();
terminal.open(document.getElementById('terminal'));

const socket = new WebSocket('ws://your-linode-ip:8080');

socket.onopen = function(event) {
    terminal.writeln('Connected to the game server');
};

socket.onmessage = function(event) {
    terminal.write('\r\n' + event.data);
};

socket.onclose = function(event) {
    terminal.writeln('Disconnected from server');
};

terminal.onData(e => {
    socket.send(e);
});