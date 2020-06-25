// Esta é a função init, disponibilizada pelo professor, nas aulas teóricas
function init() {
    var scheme
    if (window.location.protocol == 'https:')
        scheme = 'wss:';
    else
        scheme = 'ws:';
    var wsUri = scheme + '//' + window.location.hostname;
    logMsg("Connecting to " + wsUri + "...")
    websocket           = new WebSocket(wsUri);
    websocket.onopen    = function(evt) { onOpen    (evt) };
    websocket.onclose   = function(evt) { onClose   (evt) };
    websocket.onmessage = function(evt) { onMessage (evt) };
    websocket.onerror   = function(evt) { onError   (evt) };
}

// Ligar ao site criado pela ESP32
function onOpen(evt) {
    logMsg("Connected");
}

// Perder a ligação com o site criado pela ESP32
function onClose(evt) {
    logMsg("Connection Lost");
}

// Receber uma mensagem do ficheiro main.py
function onMessage(evt) {
    var str = evt.data
    if (str.startsWith("O"))  // Começando com a letra "O", faz o display da mensagem no log
        logMsg(str);
    else
        drawChart(str);
}

// Desenhar o gráfico, sempre que recebe uma nova lista
function drawChart(evt) {    
    var lista = JSON.parse(evt).lista
    var data = google.visualization.arrayToDataTable(lista);
    var options = {
        title: 'Voltagem captada pelo painel solar em função do tempo',
        curveType: 'function',
        legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
    chart.draw(data, options);
}

function logMsg(s) {
    document.getElementById("log").value += s + '\n';
}
window.addEventListener("load", init, false);