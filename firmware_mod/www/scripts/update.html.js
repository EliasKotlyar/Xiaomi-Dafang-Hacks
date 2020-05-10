    $(document).ready(function() {      
        showupdatepage();
        update(true);
    });

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