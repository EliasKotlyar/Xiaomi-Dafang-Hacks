//Function get config
function getConfig() {
    // get config and put to hmtl elements
    $.get("cgi-bin/ui_info.cgi", {cmd: "get_config"}, function(config){             
        var config_all = config.split("\n");
        for (var i = 0; i < config_all.length-1; i++) {
         var config_info = config_all[i].split("#:#");       
         $('#'+config_info[0]).html(config_info[1]);
        }
    });

}

//Get network information
function getInfo(infoname) {
    $.get("cgi-bin/ui_info.cgi", {cmd: "get_info", info: infoname}, function(config){             
        config = config.replace(/\n/g,'<br />');
        $('#'+infoname).html(config);
    });
}

//Function loaded when script load
function onLoad() {
    //Activate accordion
    accordion();
    //Get configuration
    getConfig();
    var infos = ["netInt", "netRoutes", "netDNS", "dmesg", "logVideo", "logCat", "logUpdate", "logProcess", "logMounts" ];
    for (i = 0; i < infos.length; i++)
        getInfo(infos[i]);

}

onLoad();


