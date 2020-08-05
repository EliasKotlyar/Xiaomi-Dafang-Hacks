// Function to 
function zones() {
	var ratio = $('img#motion_picture').get(0).naturalWidth / 640;
	var zones = $('#currentRegions').val();
	var zones_d = zones.split(",");
	var zones_r = new Array();
	for (var i = 0; i < zones_d.length-1; i=i+4) {
		var zone = new Object();
		zone.x = zones_d[i] / ratio;
		zone.y = zones_d[i+1] / ratio;
		zone.width = (zones_d[i+2] - zones_d[i]) / ratio;
		zone.height = (zones_d[i+3] - zones_d[i+1]) / ratio;
		zones_r.push(zone);
	}
	$('img#motion_picture').selectAreas({
		minSize: [10, 10],
		width: 640,
		maxAreas: 5,
		areas: zones_r
	});
}			


//Function save config
function saveConfig(elements) {
    //Open modal window
    document.getElementById('save_confirm').style.display='block'
    $('#save_result').html("Waiting for save result...");
	var postData = { cmd: "save_config" }
	if( elements == "regions" ) {
		var areas = $('img#motion_picture').selectAreas('relativeAreas');
		var regions = "";
		var i = 0;
		$.each(areas, function (id, area) {
			if ( i != 0 )
				regions += ',';
			i++;
			var area_x2 = area.x + area.width;
			var area_y2 = area.y + area.height;
			regions += area.x + ',' + area.y  + ',' + area_x2 + ',' + area_y2;

		});
		postData['regions'] = regions;
	}
	else {
    	$("#"+elements+" input, #"+elements+" select").each(function(){
        	var input = $(this);
        	postData[input.attr('id')] = input.val();
		});
	}
	
    $.post("cgi-bin/ui_motion.cgi",postData,function(result){
        if ( result != "")
            $('#save_result').html(result);
        else
            $('#save_result').html("Nothing to update");
    });
    
}

//Function get config
function getConfig() {
    // get config and put to hmtl elements
    $.get("cgi-bin/ui_motion.cgi", {cmd: "get_config"}, function(config){             
        var config_all = config.split("\n");
        for (var i = 0; i < config_all.length-1; i++) {
         var config_info = config_all[i].split("#:#");       
         // If element is a select, selected good value
		 if ($('#'+config_info[0]).is('select'))
            $('#'+config_info[0]+' > option').each(function() {
                if($(this).val() == config_info[1])
                    $(this).attr('selected','selected');
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
				
			

			


