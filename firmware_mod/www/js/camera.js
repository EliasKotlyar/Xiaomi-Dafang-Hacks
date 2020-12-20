//Function save config
function saveConfig(elements) {
    //Open modal window
    document.getElementById('save_confirm').style.display='block'
    $('#save_result').html("Waiting for save result...");
    var postData = { cmd: "save_config" }
    $("#"+elements+" input, #"+elements+" select").each(function(){
        var input = $(this);
        postData[input.attr('id')] = input.val();
    });
    $.post("cgi-bin/ui_camera.cgi",postData,function(result){
        if ( result != "")
            $('#save_result').html(result);
        else
            $('#save_result').html("Nothing to update");
    });
    
}

//Function get config
function getConfig() {
    // get config and put to hmtl elements
    $.get("cgi-bin/ui_camera.cgi", {cmd: "get_config"}, function(config){             
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
                    $(this).prop('selected',true);
            });
         
         else
            $('#'+config_info[0]).attr("value",config_info[1]);
       }
    });
}

//Function loaded when script load
function onLoad() {
    //Activate accordion
    accordion();
    //Get configuration
    getConfig();

}

onLoad();


