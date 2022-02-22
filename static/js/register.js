function check_All(){
    //html id, pw 가져오기
    let user_id = document.getElementById("id")
    let user_pw = document.getElementById("pw")
    let nickname = document.getElementById("nickname")

    // 비어있는 경우 예외처리
    if (user_id.value === ""){
        alert("아이디를 입력해주세요")
        user_id.focus(); // focus() : 커서가 깜빡이게 설정
        return false; // 비어있으면 아래 함수들 작동 x
    };

    if (nickname.value === ""){
        alert("비밀번호를 입력해주세요");
        nickname.focus();
        return false;
    };

    if (user_pw.value === ""){
        alert("비밀번호를 입력해주세요");
        user_pw.focus();
        return false;
    };


    // 비밀번호 영문자+숫자+특수조합(8~20자리 입력)
    let pwdCheck = /^(?=.*[a-zA-Z])(?=.*[!@.#$%^&*+=-])(?=.*[0-9]).{8,20}$/;

    if(!pwdCheck.test(user_pw.value)){
        alert("비밀번호는 영문자+숫자+특수문자 조합으로 8~20자리 사용해야 합니다.")
        user_pw.focus();
        return false

    };
    // 비밀번호 특수 문자 및 8~20자리 체크
    let num = user_pw.(/[0-9]/g);
    let eng = user_pw.(/[a-z]ig);
    let spe = pw.search(/[`~!@@#$%^&*|₩₩₩'₩";:₩/?]/gi);
    let check_Text = document.getElementsByClassName(check-text);

    if(user_pw.length < 8 || user_pw.length > 20){
        check_Text.innerText = "8자리~ 20자리 이내로 입력해주세요"
    } else if(user_pw.search(/\s/) != -1)){
        check_Text.innerText = "비밀번호는 공백 없이 입력해주세요"
    } else if(num < 0 || eng < 0 || spe < 0){
        check_Text.innerText = "영문, 숫자, 특수문자를 혼합하여 입력해주세요"
    }





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
       register();
}