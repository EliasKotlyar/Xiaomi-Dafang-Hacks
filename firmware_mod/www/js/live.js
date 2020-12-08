//Array for timeouts
var timeoutJobs = {};
var stateSideBar = false;

//Function for flip image
function flip() {
    $.get("/cgi-bin/ui_live.cgi", {cmd: "flip"});
}

//Functions for live stream with images
function refreshLiveImage() {
    var ts = new Date().getTime();
    $("#liveview").attr("src", "/cgi-bin/currentpic.cgi?" + ts);
}

//Function to download a screenshot
function downloadScreenshot() {
    var ts = new Date().getTime();
    window.location.href = "/cgi-bin/downloadpic.cgi?" + ts;
}

//Function to refresh side bar buttons
function refreshSideBar() {
    $.get("/cgi-bin/ui_live.cgi", {cmd: "status_all"}, function (result) {
       var switches = result.split("\n");
       for (var i = 0; i < switches.length-1; i++) {
        var switch_info = switches[i].split(":");
        $('#'+switch_info[0]).prop('checked', (switch_info[1] == "ON"));
       }
       if(stateSideBar)
        setTimeout(refreshSideBar, 2000);
    });
}

//Function manage refresh jobs
function scheduleRefreshJob(job,func,interval) {
    if (timeoutJobs[job] != undefined) {
        clearTimeout(timeoutJobs[job]);
    }
    timeoutJobs[job] = setTimeout(func, interval);
}

//Function for PTZ control
function PTZControl(view) {
    if( view == "show") {
        // Show PTZ Buttons
        $("#btn-ptz-left").removeClass("w3-hide");
        $("#btn-ptz-right").removeClass("w3-hide");
        $("#btn-ptz-up").removeClass("w3-hide");
        $("#btn-ptz-down").removeClass("w3-hide");
        $('#btn-ptz-calibrate').removeClass("w3-hide");
        
        //Change onclik function value and change color of button PTZ
        $("#btn-ptz").attr("onclick","PTZControl('hide')");
        $("#btn-ptz").removeClass("w3-black");   
        $("#btn-ptz").addClass("w3-grey");
    }
    else {
        // Hide PTZ Buttons
        $("#btn-ptz-left").addClass("w3-hide");
        $("#btn-ptz-right").addClass("w3-hide");
        $("#btn-ptz-up").addClass("w3-hide");
        $("#btn-ptz-down").addClass("w3-hide");
        $('#btn-ptz-calibrate').addClass("w3-hide");

        //Change onclick function value and change color of button PTZ
        $("#btn-ptz").attr("onclick","PTZControl('show')");
        $("#btn-ptz").removeClass("w3-grey");   
        $("#btn-ptz").addClass("w3-black");
    }
}

function record(action) {
    $.get("cgi-bin/ui_live.cgi",{cmd: "recording", action: action},function (result) {
        if (action == "on" || result == "ON\n") {
            $("#btn-record span").attr("style","color:red");
            $("#btn-record").attr("onclick","record('off')");
        }
        else {
            $("#btn-record span").removeAttr("style");
            $("#btn-record").attr("onclick","record('on')");
        }
    });
}

//Function to show control buttons
function camControl(view) {
    if( view == "show") {
        // Show PTZ and Settings button
        $("#cam-control").removeClass("w3-hide");
    }
    else {
        // Hide all buttons on the picture
        $("#cam-control").addClass("w3-hide");
    }
}

//Function to move the camra
function moveCamera(move) {
    var cmd = "cgi-bin/ui_live.cgi?cmd=motor&move=" + move;
    $.get(cmd);
    setTimeout(refreshLiveImage, 500);
}


//Function to open sidebar
function w3_open() {
  document.getElementById("sideBar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
  // refresh switches when control menu open
  stateSideBar = true;
  refreshSideBar();
  //Activate listen toggler switch when side bar open
  toggleSideBar();
}

//Function to close side bar
function w3_close() {
  document.getElementById("sideBar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
  stateSideBar = false;
}

//Function toggle action on side bar button
function toggleSideBar() {
    $('input').click(function(){
        var action="off";
        if (this.checked)
            action="on"
        var cmd = "cgi-bin/ui_live.cgi?cmd="+ this.id +"&action=" + action;
        $.get(cmd);      
    });

}

//Function loaded when script load
function onLoad() {
    // Show dpad according camera version
    $.get("cgi-bin/ui_live.cgi", {cmd: "show_HWmodel"}, function(model){      
        if (model != "Xiaomi Dafang\n") 
            $("#btn-ptz").addClass("w3-hide");
    });

    $.get("cgi-bin/ui_live.cgi", {cmd: "hostname"}, function(hostname){
        $("#hostname").html(hostname);
    });

    //Get record status 
    record("status");
    // Make liveview self refresh
    $("#liveview").attr("onload", "scheduleRefreshJob('live','refreshLiveImage()',1000);");
}

//Main program
onLoad();

