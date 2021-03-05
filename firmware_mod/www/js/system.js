//Function save config
function saveConfig() {
    //Open modal window
    document.getElementById('save_confirm').style.display='block'

    var postData = { cmd: "save_config",
                     hostname: $('#hostname').val(),
                     password: $('#password').val(),
                     timezone: $('#timezone').children("option:selected").val(),
                     github_token: $('#github_token').val(),
                     wifi_ssid: $('#wifi_ssid').val(),
                     wifi_password: $('#wifi_password').val(),
                     ap_ssid: $('#ap_ssid').val(),
                     ap_password: $('#ap_password').val(),
                     connect_timeout: $('#connect_timeout').val(),
                     scan_interval: $('#scan_interval').val(),
                     usb_eth: $('#usb_eth').is(":checked") ? 'on' : 'off',
                     ssh_port: $('#ssh_port').val(),
                     ssh_key: $('#ssh_key').val().replace(/ /g,'%20'),
                     ssh_password: $('#ssh_password').is(":checked") ? 'on' : 'off',
                     ntp: $('#ntp').val()};

    $.post("cgi-bin/ui_system.cgi",postData,function(result){
        //Open modal window
        if ( result != "")
            $('#save_result').html(result);
        else
            $('#save_result').html("Nothing to update");
    });


}

//Function get config
function getConfig() {
    // get config and put to hmtl elements
    $.get("cgi-bin/ui_system.cgi", {cmd: "get_config"}, function(config){
        var config_all = config.split("\n");
        for (var i = 0; i < config_all.length-1; i++) {
         var config_info = config_all[i].split("#:#");
         if ( config_info[0] == "timezone" || config_info[0] == "currenttime")
            $('#'+config_info[0]).html(config_info[1]);
         else if (config_info[0] === "usb_eth")
            $('#'+config_info[0]).prop('checked', config_info[1] === 'on');
         else if (config_info[0] === "ssh_password")
            $('#'+config_info[0]).prop('checked', config_info[1] === 'on');
         else
            $('#'+config_info[0]).attr("value",config_info[1]);

       }
    });

}

//Function loaded when script load
function onLoad() {
    //Activate accordion
    accordion();
    getConfig();
}

//Main program
onLoad();
