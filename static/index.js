let pm1;
let pm25;
let pm10;
let power_state;
let fan_speed;

// 전원 켜기
function poweron(){
    $.getJSON('/poweron',
            function(data) {
            //do nothing
        });
        return false;
}
function poweroff(){
    $.getJSON('/poweroff',
            function(data) {
            //do nothing
        });
        return false;
}
function modeauto(){
    $.getJSON('/modeauto',
            function(data) {
            //do nothing
        });
        return false;
}


//ajax 미세먼지값 수신
let intervalID= setInterval(update_dust, 1000);
function update_dust() {
    $.getJSON('/stuff',
    function (data) {
    console.log(data);
    
    pm1= Number(data.pm1);
    pm25= Number(data.pm25);
    pm10= Number(data.pm10);
    power_state= Number(data.power_state);
    fan_speed= data.fan_speed;
    console.log(pm1);
    console.log(pm25);
    console.log(pm10);
    console.log(power_state);
    console.log(fan_speed);
    
    $('#dustvalue1').text(pm1);
    $('#dustvalue2').text(pm25);
    $('#dustvalue3').text(pm10);

    if (fan_speed=="SLOW"){
        $('#fan_speed').text("1단계");
    }
    else if(fan_speed == "MID"){
        $('#fan_speed').text("2단계");
    }
    else if(fan_speed == "FULL"){
        $('#fan_speed').text("3단계");
    }
    else{
        $('#fan_speed').text("Error");
        console.log("풍량표시 오류")
    }

    //미세먼지 이모티콘 및 색 변화
    if((pm1 <= 30) && ((pm25 + pm10) <= 15)){
        $("#duststate").css("color", "#a3e7d6");
        $('#duststate').text("좋음");
        $("#good").css("display", "block");
        $("#normal").css("display", "none");
        $("#bad").css("display", "none");
        $("#verybad").css("display", "none");
        console.log("좋음")
    }else if((pm1 <= 80) && ((pm25 + pm10) <= 35)){
        $("#duststate").css("color", "#77dd77");
        $('#duststate').text("보통");
        $("#good").css("display", "none");
        $("#normal").css("display", "block");
        $("#bad").css("display", "none");
        $("#verybad").css("display", "none");
        console.log("보통")
    }else if((pm1 <= 150) && ((pm25 + pm10) <= 75)){
        $("#duststate").css("color", "#fd9a18");
        $('#duststate').text("나쁨");
        $("#good").css("display", "none");
        $("#normal").css("display", "none");
        $("#bad").css("display", "block");
        $("#verybad").css("display", "none");

    }else if((pm1 >150) || ((pm25 + pm10) > 75)){
        $("#duststate").css("color", "red");
        $('#duststate').text("매우나쁨");
        $("#good").css("display", "none");
        $("#normal").css("display", "none");
        $("#bad").css("display", "none");
        $("#verybad").css("display", "block");
    }else{
        console.log("미세먼지 상태 표시 오류")
        $('#duststate').text("Error!");
    }
    if (power_state == 0){
        $("#switch1").prop("checked", false);
        console.log("체크안됨")
    }else{
        $("#switch1").prop("checked", true);
        console.log("체크됨") //스위치를 전원이 꺼져있을때 off로 변경
    }
    if (power_state == 0){
        $('#switch2').attr("disabled", true);
        $("#sw2lb").css("background-color", "#bebebe");
    }else{
        $('#switch2').removeAttr("disabled");
    }//자동모드 스위치를 전원이 꺼져있을때 비활성화
    if (power_state == 2){
        $("#switch2").prop("checked", true);
        $("#sw2lb").css("background-color", "#0bba82");
    }else if(power_state ==1){
        $("#switch2").prop("checked", false);
        $("#sw2lb").css("background-color", "#ed4956");
    }else{
        $("#switch2").prop("checked", false);
        $("#sw2lb").css("background-color", "#bebebe");
    }//자동모드 일때 스위치 on으로 변경
    });
    
};

function powerctrl(){ // 파워스위치 누를시 실행, 파워모드 변경
    console.log("파워조정");
    if (power_state == 0){
        poweron();
    }
    else if (power_state == 1){
        poweroff();
    }
    else if (power_state == 2){
        poweroff();
    }
    else{
        console.log("파워조정 오류")
    }
};
function autoctrl(){ // 자동모드 스위치 누를시 실행, 자동모드 설정 및 해제
    console.log("모드조정");
    if (power_state == 1){
        modeauto();
        console.log("자동모드 켜기")
    }
    else if (power_state == 2){
        poweron();
    }
    else{
        console.log("자동모드 불가");
    }
};


function fanslow(){
    $.getJSON('/fanslow',
            function(data) {
            //do nothing
        });
        history.back();
        return false;
}
function fanmid(){
    $.getJSON('/fanmid',
            function(data) {
            //do nothing
        });
    history.back();
    return false;
}
function fanfull(){
    $.getJSON('/fanfull',
            function(data) {
            //do nothing
        });
        history.back();
    return false;
}





  // ajax로 전원 끄기(비동기)
  // function poweroff(){
  //     console.log("전원 끔");
  //     alert("전원 끔");
  // }
  // //

//   $(function() {
//     $('a#off').bind('click', function() {
//       $.getJSON('/poweroff',
//           function(data) {
//         //do nothing
//       });
//       return false;
//     });
//   });