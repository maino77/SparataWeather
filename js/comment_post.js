<!-- Optional JavaScript -->
<!-- jQuery first, then Popper.js, then Bootstrap JS -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
        integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
        crossorigin="anonymous"></script>

function postComment() {
        if ($('#post-local').val() == '') {
            alert('지역을 입력하세요!');
            return false;
        }
        if ($('#post-talk').val() == '') {
            alert('날씨 이야기를 입력하세요!');
            return false;
        } else {
            let local = $("#post-local").val();
            let talk = $("#post-talk").val();

            function getToday() {
                var date = new Date();
                return date.getFullYear() + "." + ("0" + (date.getMonth() + 1)).slice(-2) + "." + ("0" + date.getDate()).slice(-2) + " " + ("0" + date.getHours()).slice(-2) + ":" + ("0" + date.getMinutes()).slice(-2);
            }
            //날짜 부분 수정 작업 예정

            let date = getToday();

            $.ajax({
                type: "POST",
                url: "/album/talk",
                data: {local_give: local, talk_give: talk, date_give: date},
                success: function (response) {
                    alert(response["msg"]);
                    window.location.reload();
                }
            })
        }
    }