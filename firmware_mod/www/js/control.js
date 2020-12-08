function timedRefresh(timeoutPeriod) {
    timeoutPeriod -= 1;
    $('#message').text("Rebooting ... please wait..." + timeoutPeriod);

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
                timedRefresh(30);
            } else {
                setTimeout(update, 500);
            }
        }
    });

}

//Function show/hide accordion
function accordionUpdate(param) {
    param.classList.toggle("active");
    var panel = param.nextElementSibling;
    if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
    } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
    } 
}

function showupdatepage(result) {
    $.ajax({
        'url': 'cgi-bin/action.cgi?cmd=check_update'
    }).done(function(result){
        
        var update = result.split(":")
        var update_status = parseInt(update[1],10);

        if (update_status == 0) {
            $('#updatemsg').html("You have already the latest version from the " + update[0] + " branch")
            if (update[0] == "master") {
                $('#updatemsg').append('<button class="accordion" type="button" onclick="accordionUpdate(this);">Other Update Options</button> \
                <div class="panel"> <p></p>\
                <input id="switchBeta" class="w3-btn w3-block w3-theme" type="text" value="Switch to BETA firmware" onclick="start(\'beta\',\'full\')"/><br /> \
                <input id="fullStable" class="w3-btn w3-block w3-theme" type="text" value="Force full update to STABLE (remove version file + update)" onclick="start(\'master\',\'full\')"/><br /> \
                </div>');
                
            }
            else {
                $('#updatemsg').append('<button class="accordion" type="button" onclick="accordionUpdate(this);">Other Update Options</button> \
                <div class="panel"> <p></p>\
                <input id="switchStable" class="w3-btn w3-block w3-theme" type="text" value="Switch to STABLE firmware" onclick="start(\'master\',\'full\')"/><br /> \
                <input id="fullBeta" class="w3-btn w3-block w3-theme" type="text" value="Force full update to BETA (remove version file + update)" onclick="start(\'beta\',\'full\')"/><br /> \
                </div>');
            }
        } 
        else if (update_status == -1) {
            $('#updatemsg').html("No version file found. <br /> You can update the firmware on this camera to the latest version from <a target='_blank' href='https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks'>Github repository</a>. <br />Settings will be retained after update.")
            $('#updatemsg').append('\
            <input id="updateStable" class="w3-btn w3-block w3-theme" type="text" value="Update firmware (STABLE)" onclick="start(\'master\',\'cumul\')"/><br /> \
            <input id="updateBeta" class="w3-btn w3-block w3-theme" type="text" value="Update firmware (BETA)" onclick="start(\'beta\',\'cumul\')"/><br />');
        }
        else if (update_status > 0) {
            $('#updatemsg').html("You are "+ update_status +" commits behind "+ update[0] + " branch");
            if (update[0] == "master") {
                $('#updatemsg').append('<input id="updateStable" class="w3-btn w3-block w3-theme" type="text" value="Update firmware (STABLE)" onclick="start(\'master\',\'cumul\')"/><br />');
                $('#updatemsg').append('<button class="accordion" type="button" onclick="accordionUpdate(this);">Other Update Options</button> \
                <div class="panel"><p></p> \
                <input id="switchBeta" class="w3-btn w3-block w3-theme" type="text" value="Switch to BETA firmware" onclick="start(\'beta\',\'full\')"/><br /> \
                <input id="fullStable" class="w3-btn w3-block w3-theme" type="text" value="Force full update to STABLE (remove version file + update)" onclick="start(\'master\',\'full\')"/><br /> \
                </div>');
            }
            else {
                $('#updatemsg').append('<input id="updateBeta" class="w3-btn w3-block w3-theme" type="text" value="Update firmware (BETA)" onclick="start(\'beta\',\'cumul\')"/><br />');
                $('#updatemsg').append('<button class="accordion" type="button" onclick="accordionUpdate(this);">Other Update Options</button> \
                <div class="panel"> <p></p>\
                <input id="switchStable" class="w3-btn w3-block w3-theme" type="text" value="Switch to STABLE firmware" onclick="start(\'master\',\'full\')"/><br /> \
                <input id="fullBeta" class="w3-btn w3-block w3-theme" type="text" value="Force full update to BETA (remove version file + update)" onclick="start(\'beta\',\'full\')"/><br /> \
                </div>');
            }
        }
        else {
            $('#updatemsg').text("There is a problem with your VERSION file. Please do a full update to create a valid VERSION file.");
            $('#updatemsg').append('\
            <input id="updateStable" class="w3-btn w3-block w3-theme" type="text" value="Update firmware (STABLE)" onclick="start(\'master\',\'cumul\')"/><br /> \
            <input id="updateBeta" class="w3-btn w3-block w3-theme" type="text" value="Update firmware (BETA)" onclick="start(\'beta\',\'cumul\')"/><br />');
        }
    });
}

function saveConfig() {
    $.get("cgi-bin/ui_control.cgi",{cmd: "save_config"},function(result) {
        getFiles('config');
    });
    
}

function deleteConfig(fileName,dir) {
    var del = confirm("Confirm delete file: "+fileName);
    if ( del ) { 
        $.get("cgi-bin/ui_control.cgi", {cmd: "del_config",file: fileName});
        getFiles(dir);
    }
}

function restoreConfig(fileName) {
    var restore = confirm("Are you sure to restore config file: "+fileName+"\n Camera will reboot at the end of the process");
    if ( restore ) {
        $.get("cgi-bin/ui_control.cgi",{cmd: "restore_config",file: fileName});  
    }
}

//Function to get video and images files from dir
function getFiles(dir) {
    // Get files from dir
    $('#'+dir).html("<p><button class='w3-btn w3-theme' onclick='saveConfig();'>Take config snapshot</button></p>");
    $.get("cgi-bin/ui_control.cgi", {cmd: "getFiles", dir: dir}, function(config){             
        var config_all = config.split("\n");    
        if ( config_all.length == 1)
            $('#'+dir).append("<h1>No snapshot available.</h1>");
        else {
            $('#'+dir).append("\
            <table class='w3-table-all' id='result_"+dir+"'>\
            <thead>\
              <tr class='w3-theme'>\
                <th>Filename</th>\
                <th>Size</th>\
                <th>Date</th>\
                <th>Actions</th>\
              </tr>\
            </thead>\
            <tbody>");
            for (var i = 0; i < config_all.length-1; i++) {
                var config_info = config_all[i].split("#:#");
                var file_info = config_info[3].split(".");       
                var html_photo = "";
                $('#result_'+dir).append("<tr> \
                <td>"+config_info[0]+"</td> \
                <td>"+config_info[1]+"</td> \
                <td>"+config_info[2]+"</td> \
                <td> \
                <a href=\""+config_info[3]+"\" download><i class='fas fa-download' title='Download file'></i></a> \
                <span onclick=\"deleteConfig('"+config_info[3]+"','"+dir+"')\"><i class='fas fa-trash' title='Delete file'></i></span>\
                <span onclick=\"restoreConfig('"+config_info[3]+"')\" title='Restore config'><i class='fas fa-hdd'></i></span>\
                </td></tr>");
            }
            $('#'+dir).append("</tbody></table><p></p>");
            var table = $('#result_'+dir).DataTable();
            $('#result'+dir).on( 'click', 'tr', function () {
                //$(this).toggleClass('selected');
            } );
            $('#result'+dir).click( function () {
               //alert( table.rows('.selected').data().length +' row(s) selected' );
            } );
        }
    });

}


function start(branch,mode) {
    var login = "";   
    // if ($('#login').val().length > 0) {
    //     login = "login=" + $('#login').val() + ":" + $('#password').val();
    // }
    //Open modal window
    document.getElementById('modal_box').style.display='block'
    $('#modal_title').html('Update in progress');
    $('#modal_content').html('<h4>Please note: at the end of this process the camera will reboot without notice!</h4> \
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
            $('#modal_content').text("Error starting update process!!!");
        }
    });
}

//Function control service (stop/start)
function controlService(action,serviceName) {
    $.get("cgi-bin/ui_control.cgi", {cmd: "services",service: serviceName, action: action}, function(result){
        $('#control_'+serviceName).removeAttr('onclick');
        if (action == 'start') {
            $('#control_'+serviceName).attr('onclick','controlService("stop","'+serviceName+'")')
        }
        else {
            $('#control_'+serviceName).attr('onclick','controlService("start","'+serviceName+'")')
        }
    });
}

//Function to control autostart
function autoStartService(action,serviceName) {
    $.get("cgi-bin/ui_control.cgi", {cmd: "autoStartService",service: serviceName, action: action});
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
    $.get("cgi-bin/ui_control.cgi", {cmd: "get_services"}, function(config){             
        var config_all = config.split("\n");
        for (var i = 0; i < config_all.length-1; i++) {
         var config_info = config_all[i].split("#:#");       
         // Select button color accrding status
         var control_checked = "onclick='controlService(\"start\",\""+config_info[0]+"\")')";
         if (config_info[1] == "started")
            control_checked = "checked onclick='controlService(\"stop\",\""+config_info[0]+"\")')";
         var autostart_checked = "onclick='autoStartService(\"true\",\""+config_info[0]+"\")')";
         if(config_info[2] == "true")
            autostart_checked = "checked onclick='autoStartService(\"false\",\""+config_info[0]+"\")')";
         $('#tabServices').append("<tr><td>"+config_info[0]+"</td>\
         <td>Stop <label class='switch'><input id='control_"+config_info[0]+"' class='w3-check' type='checkbox' "+control_checked+"> <span class='slider round'></span></label> Start</td>\
         <td>Off <label class='switch'><input id='autoStart_"+config_info[0]+"' class='w3-check' type='checkbox' "+autostart_checked+"> <span class='slider round'></span></label> On</td></tr>");
        }
    });

}

function system(command) {
    //Open modal window
    document.getElementById('modal_box').style.display='block'
    $('#modal_title').html(command);
    if (command == "reboot") {
        $('#modal_content').html("<h4 id=message></h4>");
        timedRefresh(45);
        $.get("cgi-bin/action.cgi?cmd=reboot");
    }
    else {
        $('#modal_content').html("The camera is shutting down ...");
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


