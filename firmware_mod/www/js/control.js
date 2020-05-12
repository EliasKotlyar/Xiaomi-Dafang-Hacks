function timedRefresh(timeoutPeriod) {
    timeoutPeriod -= 1;
    $('#message').text("Rebooting ... wait..." + timeoutPeriod);

    if (timeoutPeriod == 0) {
        window.location.href = window.location.href;
    } else {
        setTimeout(function() {
            timedRefresh(timeoutPeriod)
        }, 1000);
    }
};

function update(onStart) {
    $.ajax({
        'url': 'cgi-bin/action.cgi?cmd=show_updateProgress'
    }).done(function(log) {   
        if (log < 0) {
            if (onStart != true)
            {
                $('#message').text("Error starting update progress");
                $('#message').text("Error starting update process");
            }
        } else {
            $('#message').text("Update in progress");
            $('#progress').removeAttr('style');
            $('#progress').attr('style','width:'+log+'%');
            $('#progressValue').html(log+'%');
            // This is the end, start the reboot count down
            if (log >= 100) {
                timedRefresh(45);
            } else {
                setTimeout(update, 500);
            }
        }
    });

}
function showupdatepage(result) {
    $.ajax({
        'url': 'cgi-bin/action.cgi?cmd=check_update'
    }).done(function(result){
        
        var update = result.split(":")
        var update_status = parseInt(update[1],10);

        if (update_status == 0) {
            $('#updatemsg').html("You have already the lastest version from branch " + update[0])
            if (update[0] == "master") {
                $('#switchBeta').removeAttr('style');
                $('#fullStable').removeAttr('style');
            }
            else {
                $('#switchStable').removeAttr('style');
                $('#fullBeta').removeAttr('style');
            }
        } 
        else if (update_status == -1) {
            $('#updatemsg').html("No version file found. <br /> You can update the running firmware on this camera by the latest available from its <a target='_blank' href='https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks'>Github repository</a>. <br />Settings will be retained after update.")
            $('#updateStable').removeAttr('style');
            $('#updateBeta').removeAttr('style');
        }
        else if (update_status > 0) {
            $('#updatemsg').html("You are "+ update_status +" commits behind "+ update[0] + " branch");
            if (update[0] == "master") {
                $('#updateStable').removeAttr('style');
                $('#switchBeta').removeAttr('style');
                $('#fullStable').removeAttr('style');
            }
            else {
                $('#updateBeta').removeAttr('style');
                $('#switchStable').removeAttr('style');
                $('#fullBeta').removeAttr('style');
            }
        }
        else {
            $('#updatemsg').text("Problem with your VERSION file. Need a full update to get a correct VERSION file.");
            $('#fullStable').removeAttr('style');
            $('#fullBeta').removeAttr('style');
        }
    });
}

function start(branch,mode) {
    var login = "";   
    // if ($('#login').val().length > 0) {
    //     login = "login=" + $('#login').val() + ":" + $('#password').val();
    // }
    //Open modal window
    document.getElementById('confirm_box').style.display='block'
    $('#confirm_title').html('Update in progress');
    $('#confirm_content').html('<h4>Please note: at the end of this process the camera will reboot without notice</h4> \
    <div class="w3-light-grey"><div id="progress" class="w3-container w3-theme" style="width:0%"><span id="progressValue">0%</span></div></div><br><h4 id=message></h4>');

    var url = 'cgi-bin/action.cgi?cmd=update&release='+branch+'&mode='+mode;
    $.ajax({
        'url': url,
        'type': 'POST',
        'data': login
    }).done(function(result) {

        if (result.length > 0) {
            update(false);
        } else {
            $('#confrim_content').text("Error starting update progress");
        }
    });
}

//Function control service (stop/start)
function controlService(action,serviceName) {
    $.get("cgi-bin/control.cgi", {cmd: "services",service: serviceName, action: action}, function(result){
        if (action == 'on') {
            $('#start_'+serviceName).removeAttr('onclick');
            $('#stop_'+serviceName).attr('onclick','controlService("off","'+serviceName+'")');
            $('#start_'+serviceName).removeClass('w3-text-green');
            $('#start_'+serviceName).addClass('w3-text-grey');
            $('#stop_'+serviceName).removeClass('w3-text-grey');
            $('#stop_'+serviceName).addClass('w3-text-red');
        }
        else {
            $('#stop_'+serviceName).removeAttr('onclick');
            $('#start_'+serviceName).attr('onclick','controlService("on","'+serviceName+'")');
            $('#start_'+serviceName).removeClass('w3-text-grey');
            $('#start_'+serviceName).addClass('w3-text-green');
            $('#stop_'+serviceName).removeClass('w3-text-red');
            $('#stop_'+serviceName).addClass('w3-text-grey');
        }
        $('#start').append("<tr><td>"+config_info[0]+"</td><td><i class='fa fa-play-circle w3-xxlarge "+color_start+"</i> <i class='fa fa-stop-circle w3-xxlarge "+color_stop+"</i></td><td><input class='w3-check' type='checkbox' "+checked+"></td></tr>");
    });
}

//Function to control autostart
function autoStartService(action,serviceName) {
    $.get("cgi-bin/control.cgi", {cmd: "autoStartService",service: serviceName, action: action});
    $('#autoStart_'+serviceName).removeAttr('onclick');
    if(action == "true") {
        $('#autoStart_'+serviceName).attr('onclick','autoStartService("false","'+serviceName+'")');
    }
    else {
        $('#autoStart_'+serviceName).attr('onclick','autoStartService("true","'+serviceName+'")');
    }
}

//Function get config
function getServices() {
    // get config and put to hmtl elements
    $.get("cgi-bin/control.cgi", {cmd: "get_services"}, function(config){             
        var config_all = config.split("\n");
        for (var i = 0; i < config_all.length-1; i++) {
         var config_info = config_all[i].split("#:#");       
         // Select button color accrding status
         if (config_info[1] == "ON") {
             var color_start = "w3-text-grey' id='start_"+config_info[0]+"'>";
             var color_stop = "w3-text-red'onclick='controlService(\"off\",\""+config_info[0]+"\")' id='stop_"+config_info[0]+"'>";
         }
         else {
            var color_start = "w3-text-green' onclick='controlService(\"on\",\""+config_info[0]+"\")' id='start_"+config_info[0]+"'>";
            var color_stop = "w3-text-grey' id='stop_"+config_info[0]+"'>";
         }
         var checked = "onclick='autoStartService(\"true\",\""+config_info[0]+"\")')";
         if(config_info[2] == "true")
            checked = "checked onclick='autoStartService(\"false\",\""+config_info[0]+"\")')";
         $('#tabServices').append("<tr><td>"+config_info[0]+"</td><td><i class='fa fa-play-circle w3-xxlarge "+color_start+"</i> <i class='fa fa-stop-circle w3-xxlarge "+color_stop+"</i></td><td><input id='autoStart_"+config_info[0]+"' class='w3-check' type='checkbox' "+checked+"></td></tr>");
        }
    });

}

function system(command) {
    //Open modal window
    document.getElementById('confirm_box').style.display='block'
    $('#confirm_title').html(command);
    if (command == "reboot") {
        $('#confirm_content').html("Waiting for camera to reboot...");
        $.get("cgi-bin/action.cgi?cmd=reboot");
    }
    else {
        $('#confirm_content').html("Camera shutting down...");
        $.get("cgi-bin/action.cgi?cmd=shutdown");
    }
}

//Function loaded when script load
function onLoad() {
    //Activate accordion
    accordion();
    //Get configuration
    getServices();
}

onLoad();


