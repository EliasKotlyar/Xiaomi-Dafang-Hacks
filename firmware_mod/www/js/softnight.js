var cur_exposure=-1;
var cur_iridix=-1;
var cur_wb=-1;
var cur_day=true;
var eq2_count = 0;
var eq3_count = 0;



var exposure = new TimeSeries();
var wb = new TimeSeries();
var wb_rg = new TimeSeries();
var wb_bg = new TimeSeries();
var iridix = new TimeSeries();
var gain = new TimeSeries();

function readIspInfo(){
      $.get("/cgi-bin/ui_softnight.cgi", function(data, status)
      {
      parseIspInfo(data);
      });
}
function parseIspInfo(data){
  var lines = data.split('\n');
  var d = new Date().getTime();
  for(var i = 0;i < lines.length;i++){
      for(var k=0; k<keys.length; k++){
          if(lines[i].startsWith(String(keys[k]))){
              var val = lines[i].split(":");
              serieses[k].append(d, val[1]);
              if(String(keys[k]).search('exposure') >= 0){
                  cur_exposure = val[1];
              }else if(String(keys[k]).search('WB Temperature') >= 0){
                  cur_wb = val[1];
              }else if(String(keys[k]).search('Iridix') >= 0){
                  cur_iridix = val[1];
              }
          }
      }
  }
  update_values();
}
timeFormatter = function (date) {
  return date.getMinutes() * 60 + date.getSeconds();
};

var serieses = [];
var keys = [];
var ids= [];
var charts = [];

var timer;
var running;

function getParams(){
  var canvases = $('#canvas_table canvas');
  var divs = $('#canvas_table div');
  var tds = $('#canvas_table td');
  for(var i=0; i<canvases.length; i++){
      var id = canvases[i].id;
      var key = divs[i].innerText;
      var width = tds[i*2+1].clientWidth;
      canvases[i].width = width; 
      serieses[i] = new TimeSeries();
      keys[i] = key;
      ids[i] = id;
  }
}

function startGraph(){
  for(var i=0; i<ids.length; i++){
      //charts[i] = new SmoothieChart({timestampFormatter: timeFormatter,nonRealtimeData: false,millisPerPixel:32,interpolation:'step',labels:{fontSize:10},limitFPS:15});
      var opt = {millisPerPixel:32,interpolation:'step',scaleSmoothing:1,labels:{fontSize:13},tooltip:true,limitFPS:15,horizontalLines:[{color:'#ffffff',lineWidth:1,value:0},{color:'#880000',lineWidth:2,value:3333},{color:'#880000',lineWidth:2,value:-3333}]};
      charts[i] = new SmoothieChart(opt);
      charts[i].addTimeSeries(serieses[i], { strokeStyle: 'rgba(0, 255, 0, 1)', fillStyle: 'rgba(0, 255, 0, 0.2)', lineWidth: 2 });
      charts[i].streamTo(document.getElementById(String(ids[i])));
  }
}

$(document).ready(function () {
  $.get("/cgi-bin/action.cgi?cmd=get_sw_night_config", function(data, status)
      {
          var list = data.split('-');
          var valid=false;
          var j = $("#jitter_percent").val();
          var w = $("#sec_wait").val();
          var e11 = $("#eq1_user_exposure").val();
          var e21 = $("#eq2_user_exposure").val();
          var e22 = $("#eq2_user_iridix").val();
          var e23 = $("#eq2_count").val();
          var e31 = $("#eq3_user_wb").val();
          var e32 = $("#eq3_user_iridix").val();
          var e33 = $("#eq3_count").val();;
          
          for(var i=0; i<list.length; i++){
              switch (list[i][0]){
                  case 'S':
                      valid = true;
                      break;
                  case 'j':
                      j = parseInt(list[i].substring(1)) || j;
                      break;
                  case 'w':
                      w = parseInt(list[i].substring(1)) || w;
                      break;
                  case '1':
                      e11 = parseInt(list[i].substring(1)) || e11;
                      break;
                  case '2':
                      var p = list[i].split(' ');
                      var p2 = p[1].split(',');
                      e21 = parseInt(p2[0]) || e21;
                      e22 = parseInt(p2[1]) || e22;
                      e23 = parseInt(p2[2]) || e23;
                      break;
                  case '3':
                      var p = list[i].split(' ');
                      var p2 = p[1].split(',');
                      e31 = parseInt(p2[0]) || e31;
                      e32 = parseInt(p2[1]) || e32;
                      e33 = parseInt(p2[2]) || e33;
                      break;
              }
          }
          $("#jitter_percent").val(j);
          $("#sec_wait").val(w);
          $("#eq1_user_exposure").val(e11);
          if(e21 == 0){
              $('#eq2').prop('checked', false);
          }else{
              $("#eq2_user_exposure").val(e21);
              $("#eq2_user_iridix").val(e22);
              $("#eq2_count").val(e23);
          }
          if(e31 == 0){
              $('#eq3').prop('checked', false);
          }else{
              $("#eq3_user_wb").val(e31);
              $("#eq3_user_iridix").val(e32);
              $("#eq3_count").val(e33);
          }
          night_mode(false);
          getParams();
          startGraph();
          readIspInfo();
          timer = setInterval(readIspInfo, 1000);
          running = true;
      });
});
  function sw_night_config_pageDone()
  {
      clearInterval(timer);
  }


  $('#play').click(function (event) {
  /*if(running){
      clearInterval(timer);
      running = false;
      $('#play').html("Play");
      for(var i=0; i<charts.length; i++){
          charts[i].stop();
      }
  }else{
      timer = setInterval(readIspInfo, 1000);
      running = true;
      $('#play').html("Pause");
      for(var i=0; i<charts.length; i++){
          charts[i].start();
      }
  }*/
});
function ir_led(val){
  var cmd = (val) ? "cgi-bin/action.cgi?cmd=ir_led_on" : "cgi-bin/action.cgi?cmd=ir_led_off";
  $.get(cmd, function(data, status){});
}
function ir_cut(val){
  var cmd = (val) ? "cgi-bin/action.cgi?cmd=ir_cut_on" : "cgi-bin/action.cgi?cmd=ir_cut_off";
  $.get(cmd, function(data, status){});
}

function night_mode(val){
  var cmd = 'cgi-bin/action.cgi?cmd=toggle-rtsp-nightvision-' + ((val) ? "on" : "off");
  ir_led(true);
  if(val){
      $.get(cmd, function(data, status){});
      ir_cut(!val);
  }else{
      ir_cut(!val);
      $.get(cmd, function(data, status){});
  }
  cur_day = !val;
  $('#cur_mode')[0].innerText = (cur_day) ? "Day mode" : "Night mode";
  $('#cur_mode').css( "color", (cur_day) ? "black" : "white" );
  $('#cur_mode').css( "background-color", (cur_day) ? "white" : "black" );
  $(".eq2").css( "box-shadow", "" );
  $(".eq3").css( "box-shadow", "" );
  mode_switch_wait_count = parseInt($("#sec_wait")[0].value);
}

function update_commandline()
{
  var cmdline = "-S -j " + $("#jitter_percent")[0].value + " -w " + $("#sec_wait")[0].value;
  cmdline += " -1 " + $("#eq1_user_exposure")[0].value;
  cmdline += " -2 ";
  cmdline += $("#eq2")[0].checked ? ($("#eq2_user_exposure")[0].value + "," + ($("#eq2_1")[0].checked ? $("#eq2_user_iridix")[0].value : "9999") + "," + $("#eq2_count")[0].value) : "0,0,1";
  cmdline += " -3 ";
  cmdline += $("#eq3")[0].checked ? ($("#eq3_user_wb")[0].value + "," + ($("#eq3_1")[0].checked ? $("#eq3_user_iridix")[0].value : "0") + "," + $("#eq3_count")[0].value) : "0,0,1";

  $("#command_line")[0].value = cmdline;
}

var last_exposure = 0;
var mode_switch_wait_count=0;
var sec=0;
function update_values(){
  var eq1_pass=false, eq2_pass=false, eq3_pass=false, eq2_1_pass=false, eq3_1_pass=false;
  var jitter_percent;

  try{
      jitter_percent = parseInt($("#jitter_percent")[0].value);
  }catch(e){
      return sw_night_config_pageDone();
  }

  update_commandline();

  $('#exposure_eq1')[0].value = cur_exposure;
  $('#exposure_eq2')[0].value = cur_exposure;
  $('#iridix_eq2')[0].value = cur_iridix;
  $('#iridix_eq3')[0].value = cur_iridix;
  $('#wb_eq3')[0].value = cur_wb;
  sec++;
  sec = sec % 60;
  $('#sec')[0].innerText = sec;

  if( (Math.abs(cur_exposure - last_exposure)/cur_exposure)*100 >= jitter_percent  ){
      last_exposure = cur_exposure;
      $(".jitter").css( "font-weigth", "bold" );
      $(".jitter").css( "background-color", "#ff9292" );
      $(".jitter").css( "box-shadow", "8px 6px 13px #f5194b" );
      eq2_count = 0;
      eq3_count = 0;
      $('#count_eq2')[0].value = eq2_count;
      $('#count_eq3')[0].value = eq3_count;
      return;
  }
  $(".jitter").css( "font-weigth", "normal" );
  $(".jitter").css( "background-color", "#89fcfd" );
  $(".jitter").css( "box-shadow", "" );
  last_exposure = cur_exposure;
  if(cur_exposure > parseInt($("#eq1_user_exposure")[0].value)){
      $("#exposure_eq1").css('color', "green");
      eq1_pass = true;
  }else{
      $("#exposure_eq1").css('color', "red");
  }
  if(cur_exposure < parseInt($("#eq2_user_exposure")[0].value)){
      $("#exposure_eq2").css('color', "green");
      eq2_pass=true;
  }else{
      $("#exposure_eq2").css('color', "red");
  }
  if(cur_iridix < parseInt($("#eq2_user_iridix")[0].value)){
      eq2_1_pass = true;
      $("#iridix_eq2").css('color', "green");
  }else{
      $("#iridix_eq2").css('color', "red");
  }
  if(cur_wb < parseInt($("#eq3_user_wb")[0].value)){
      $("#wb_eq3").css('color', "green");
      eq3_pass=true;
  }else{
      $("#wb_eq3").css('color', "red");
  }
  if(cur_iridix > parseInt($("#eq3_user_iridix")[0].value)){
      eq3_1_pass = true;
      $("#iridix_eq3").css('color', "green");
  }else{
      $("#iridix_eq3").css('color', "red");
  }

  var eq2_enabled     = $("#eq2")[0].checked;
  var eq2_1_enabled   = $("#eq2_1")[0].checked;
  var eq3_enabled     = $("#eq3")[0].checked;
  var eq3_1_enabled   = $("#eq3_1")[0].checked;

  if(mode_switch_wait_count){
      mode_switch_wait_count--;
      $(".wait").css( "box-shadow", "8px 6px 13px #f5194b" );
  }else{
      $(".wait").css( "box-shadow", "" );
      if(cur_day == true){
          if(eq1_pass){
              night_mode(true);
              eq2_count = 0;
              eq3_count = 0;
          }
      }else{
          if(eq2_enabled && eq2_pass && ((eq2_1_enabled && eq2_1_pass) || (eq2_1_enabled == false)) ){
              $(".eq2").css( "box-shadow", "8px 6px 13px #f5194b" );
              eq2_count++;
              if(eq2_count > parseInt($("#eq2_count")[0].value)){
                  night_mode(false);
              }
          }else{
              $(".eq2").css( "box-shadow", "" );
              eq2_count = 0;
          }
          if(eq3_enabled && eq3_pass && ((eq3_1_enabled && eq3_1_pass) || (eq3_1_enabled == false)) ){
              $(".eq3").css( "box-shadow", "8px 6px 13px #f5194b" );
              eq3_count++;
              if(eq3_count > parseInt($("#eq3_count")[0].value )){
                  night_mode(false);
              }
          }else{
              $(".eq3").css( "box-shadow", "" );
              eq3_count = 0;
          }
      }
  }
  $('#count_eq2')[0].value = eq2_count;
  $('#count_eq3')[0].value = eq3_count;

}
function eq_click(name){
  update_commandline();
  if($("#"+name)[0].checked){
      $("."+name).css( "opacity", "1.0" );
      //$("."+name+"_1").css( "opacity", "1.0" );
      $("#"+name+"_1")[0].disabled = false;
      eq_1_click(name);
  }else{
      $("."+name).css( "opacity", "0.7" );
      $("."+name+"_1").css( "opacity", "0.7" );
      $("#"+name+"_1")[0].disabled = true;
  }
}
function eq_1_click(name){
  update_commandline();
  if($("#"+name+"_1")[0].checked){
      $("."+name+"_1").css( "opacity", "1.0" );
  }else{
      $("."+name+"_1").css( "opacity", "0.7" );
  }
}
$('#swNightForm').submit(function (event) {
  debugger;
  var b = $('#sw_night_submit');
      b.toggleClass('is-loading');
      b.prop('disabled', !b.prop('disabled'));

      var formData = {
          'val' :  $("#command_line").val()
      };
      $.ajax({
          type: 'POST',
          url: $('#swNightForm').attr('action'),
          data: formData,
          dataType: 'html',
          encode: true
      }).done(function (res) {
          b.toggleClass('is-loading');
          b.prop('disabled', !b.prop('disabled'));
          showResult(res);
      });
      event.preventDefault();
});