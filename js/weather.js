const API_KEY = "9730934379c4806648360d3cc00d8894";

// getCurrentPosition이 성공했을 때 함수
// latitude 위도, longitude 경도
function onGeoOk(position){
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${API_KEY}&units=metric`;
    // fetch함수: 서버에 데이터 요청
    // .then 서버에서 데이터를 가져오는 작업이 완료된 이후 then에 있는 함수 실행 
    // response 객체는 fetch를 통해서 요청했을 때 웹서버가 응답한 결과를 담고있는 객체데이터
    fetch(url)
        .then(response => response.json())
        .then(data =>{
        const name = data.name;
        const temp =  data.main.temp
        const feels_like = data.main.feels_like
        const temp_min = data.main.temp_min
        const temp_max = data.main.temp_max
        const humidity = data.main.humidity
    });
}

// 변수 정리
// 1. data.name: 도시 이름
// 2. data.main.temp: 현재 온도
// 3. data.main.feels_like: 체감 온도
// 4. data.main.temp_min: 최저 온도
// 5. data.main.temp_max: 최고 온도
// 6. data.main.humidity: 습도

// 1체감 온도 2최저 3최고 온도 4강수량 5현재 온도 6도시 이름








// getCurrentPosition이 실패했을 때 함수
function onGeoError(){
    alert("위치를 찾을 수 없어 날씨를 제공할 수 없습니다.")
}

// 유저의 위치를 주는 함수
// 브라우저에서 위치 좌표를 줌
// getCurrentPosition은 성공했을 때 함수, 실패했을 때 함수가 필요
navigator.geolocation.getCurrentPosition(onGeoOk, onGeoError)