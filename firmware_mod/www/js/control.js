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
            $('#start').removeAttr('disabled');
            $('#startBeta').removeAttr('disabled');
        } else {
            $('#start').attr("disabled", "disabled");
            $('#startBeta').attr("disabled", "disabled");
            $('#message').text("Update in progress");
            $('#progress').val(log);
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
                $('#btn_switch_beta').removeAttr('style');
                $('#btn_force_update_master').removeAttr('style');
            }
            else {
                $('#btn_switch_master').removeAttr('style');
                $('#btn_force_update_beta').removeAttr('style');
            }
        } 
        else if (update_status == -1) {
            $('#updatemsg').html("No version file found. <br /> You can update the running firmware on this camera by the latest available from its <a target='_blank' href='https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks'>Github repository</a>. <br />Settings will be retained after update.")
            $('#btn_update_master').removeAttr('style');
            $('#btn_update_beta').removeAttr('style');
        }
        else if (update_status > 0) {
            $('#updatemsg').html("You are "+ update_status +" commits behind "+ update[0] + " branch");
            if (update[0] == "master") {
                $('#btn_update_master').removeAttr('style');
                $('#btn_switch_beta').removeAttr('style');
                $('#btn_force_update_master').removeAttr('style');
            }
            else {
                $('#btn_update_beta').removeAttr('style');
                $('#btn_switch_master').removeAttr('style');
                $('#btn_force_update_beta').removeAttr('style');
            }
        }
        else {
            $('#updatemsg').text("Problem with your VERSION file. Need a full update to get a correct VERSION file.");
            $('#btn_force_update_master').removeAttr('style');
            $('#btn_force_update_beta').removeAttr('style');
        }
    });
}

function start(branch,mode) {
    var login = "";   
    // if ($('#login').val().length > 0) {
    //     login = "login=" + $('#login').val() + ":" + $('#password').val();
    // }
    $('#updatebox').removeAttr('style');
    $('#updatebtn').attr('style','display:none;visibility: hidden;');
    $('#updatemsg').html("");
    $('#progressbox').removeAttr('style');
    var url = 'cgi-bin/action.cgi?cmd=update&release='+branch+'&mode='+mode;
    $.ajax({
        'url': url,
        'type': 'POST',
        'data': login
    }).done(function(result) {

        if (result.length > 0) {
             $('#start').attr("disabled", "disabled");
             $('#startBeta').attr("disabled", "disabled");
            update(false);
        } else {
            $('#message').text("Error starting update progress");
            $('#start').removeAttr('disabled');
            $('#startBeta').removeAttr('disabled');
        }
    });
}

//Function save config
function saveConfig() {
    //Open modal window
    document.getElementById('save_confirm').style.display='block'
    var postData = { cmd: "save_config" }
    $("#camera input, select").each(function(){
        var input = $(this);
        postData[input.attr('id')] = input.val();
    });
    $.post("cgi-bin/camera.cgi",postData,function(result){
        if ( result != "")
            $('#save_result').html(result);
        else
            $('#save_result').html("Nothing to update");
    });
    
}

//Function get config
function getConfig() {
    // get config and put to hmtl elements
    $.get("cgi-bin/control.cgi", {cmd: "get_config"}, function(config){             
        var config_all = config.split("\n");
        for (var i = 0; i < config_all.length-1; i++) {
         var config_info = config_all[i].split("#:#");       
         // If element is a select, selected good value
         if (config_info[0] == "osdFonts") {
            $('#'+config_info[0]).html(config_info[1]);
         }
         else if ($('#'+config_info[0]).is('select'))
            $('#'+config_info[0]+' > option').each(function() {
                if($(this).val() == config_info[1])
                    $(this).attr('selected','selected');
            });
         
         else
            $('#'+config_info[0]).attr("value",config_info[1]);
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
    getConfig();
    showupdatepage();
    update(true);
}

onLoad();


