$(document).ready(function(){
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chat_socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);
    function updateScroll(){
        var element = document.getElementById("messages");
        element.scrollTop = element.scrollHeight;
        
    }
    updateScroll();
    $('#chatform').on('submit', function(event) {
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
        $('#message').val('');
        if (message.message.length > 0 ){
            chat_socket.send(JSON.stringify(message));
        }
        return false;
    });

    chat_socket.onmessage = function(message) {
        var data = JSON.parse(message.data);
        $('#chat').append('<tr>' 
            + '<td class="time">' + data.created_at + '</td>' 
            + '<td class="name">' + data.handle + ':</td>'
            + '<td>' + data.message + ' </td>'
        + '</tr>');
        updateScroll();
    }
    

})