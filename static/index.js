let pm1;
let pm25;
let pm10;
let power_state;


//새로고침 있음
function poweron(){
    $.getJSON('/poweron',
            function(data) {
            //do nothing
        });
        return false;
}
    
  //새로고침 있음
function poweroff(){
    //확인
    //document.form.submit();
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
    
    pm1= Number(data.pm1)
    pm25= Number(data.pm25)
    pm10= Number(data.pm10)
    power_state= Number(data.power_state)
    fan_state= Number(data.fan_state)
    console.log(pm1);
    console.log(pm25);
    console.log(pm10);
    console.log(power_state);
    console.log(fan_state);
    
    $('#dustvalue1').text(pm1);
    $('#dustvalue2').text(pm25);
    $('#dustvalue3').text(pm10);

      //미세먼지 배경 색 변화
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
        console.log("체크됨")
    }
    if (power_state == 0){
        $('#switch2').attr("disabled", true);
        $("#sw2lb").css("background-color", "#bebebe");
    }else{
        $('#switch2').removeAttr("disabled");
        
    }
    if (power_state == 2){
        $("#switch2").prop("checked", true);
        $("#sw2lb").css("background-color", "#0bba82");
    }else if(power_state ==1){
        $("#switch2").prop("checked", false);
        $("#sw2lb").css("background-color", "#ed4956");
    }else{
        $("#switch2").prop("checked", false);
        $("#sw2lb").css("background-color", "#bebebe");
    }
        
    
    });
    
};

function powerctrl(){
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
function autoctrl(){
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