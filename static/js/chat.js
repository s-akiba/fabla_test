function readMessage() {
    $.ajax({
        type: 'post',
        url: './php/message.txt'
        })
    .then(
        function (data) {
            log = data.replace(/[\n\r]/g, "<br />");
            $('#messageTextBox').html(log);
        },
        function () {
            alert("読み込み失敗");
        }
    );
}


function writeMessage() {
    $.ajax({
        type: 'post',
        url: './php/chat.php',
        data: {
            'message' : $("#message").val()
        }
    })
    .then(
        function (data) {
            readMessage();
            $("#message").val('');
        },
        function () {
            alert("書き込み失敗");
        }
    );
}


$(document).ready(function() {
    readMessage();
    setInterval('readMessage()', 3000);
});