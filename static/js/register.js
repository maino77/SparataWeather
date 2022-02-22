function register() {
    let id = $('#id').val();
    let pw = $('#pw').val();
    let nickname = $('#nickname').val();

    $.ajax({
        type: "POST",
        url: "/api/register",
        data: {id_give: id, pw_give: pw, nickname_give: nickname},
        success: function (response) { // 성공하면
            alert(response["msg"]);
            window.location.replace('login')
        }
    })
}