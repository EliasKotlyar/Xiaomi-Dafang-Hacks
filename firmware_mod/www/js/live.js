//Functions for live stream with images
var timeoutJobs = {};

function refreshLiveImage() {
    var ts = new Date().getTime();
    $("#liveview").attr("src", "/cgi-bin/currentpic.cgi?" + ts);
}

function scheduleRefreshLiveImage(interval) {
    if (timeoutJobs['refreshLiveImage'] != undefined) {
        clearTimeout(timeoutJobs['refreshLiveImage']);
    }
    timeoutJobs['refreshLiveImage'] = setTimeout(refreshLiveImage, interval);
}

//Function for PTZ control
function PTZControl(view) {
    if( view == "show") {
        // Show PTZ Buttons
        $("#btn-ptz-left").removeClass("w3-hide");
        $("#btn-ptz-right").removeClass("w3-hide");
        $("#btn-ptz-up").removeClass("w3-hide");
        $("#btn-ptz-down").removeClass("w3-hide");
        
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
        
        //Change onclick function value and change color of button PTZ
        $("#btn-ptz").attr("onclick","PTZControl('show')");
        $("#btn-ptz").removeClass("w3-grey");   
        $("#btn-ptz").addClass("w3-black");
    }
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
    var cmd = "cgi-bin/action.cgi?cmd=motor_" + move;
    $.get(cmd);
    setTimeout(refreshLiveImage, 500);
}

//Function to sync control switch on the left
function syncControlSwitches() {
    $.get("https://192.168.76.105/cgi-bin/state.cgi", {cmd: "all"}, function (result) {
       var switches = result.split("\n");
       for (var i = 0; i < switches.length-1; i++) {
        var switch_info = switches[i].split(":");
        $('#'+switch_info[0]).prop('checked', (switch_info[1] == "ON"));
       }
    });
}

//Function to open sidebar
function w3_open() {
  document.getElementById("cameraSidebar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
  syncControlSwitches();
}

//Function to close side bar
function w3_close() {
  document.getElementById("cameraSidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}





//Function loaded when script load
function onLoad() {
    // Show dpad according camera version
    $.get("cgi-bin/action.cgi", {cmd: "show_HWmodel"}, function(model){      
        if (model != "Xiaomi Dafang\n") 
            $("#btn-ptz").addClass("w3-hide");
    });

    $.get("cgi-bin/state.cgi", {cmd: "hostname"}, function(hostname){
        $("#hostname").html(hostname);
    });

    // Make liveview self refresh
    $("#liveview").attr("onload", "scheduleRefreshLiveImage(1000);");
}

onLoad();