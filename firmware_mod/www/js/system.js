//Function save config
function saveConfig() {
    //Open modal window
    document.getElementById('save_confirm').style.display='block'
    
    var postData = { cmd: "save_config",
                     hostname: $('#hostname').val(),
                     password: $('#password').val(),
                     timezone: $('#timezone').children("option:selected").val(),
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