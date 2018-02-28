
$(function(){
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chat_socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);

    $('#chatform').on('submit', function(event) {
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
        chat_socket.send(JSON.stringify(message));
        return false;
    });

    chat_socket.onmessage = function(message) {
        var data = JSON.parse(message.data);
        $('#chat').append('<tr>' 
            + '<td>' + data.timestamp + '</td>' 
            + '<td>' + data.handle + '</td>'
            + '<td>' + data.message + ' </td>'
        + '</tr>');
    }
    //   no longer to be used
    // $('#friends').on('click', 'button', function(){
    //     $friend_id=$(this).attr('value')
    //     $.ajax({
    //         type: "POST",
    //         data: {action:"chat_room", friend_id: $friend_id},
    //         success: function(data){
    //             // print(data);
    //             $("#chat tbody").html("");
    //             for (var message in data.messages) {
    //                 chat_socket.send(JSON.stringify(message))
    //             }
    //         },
    //     })
    // })
})