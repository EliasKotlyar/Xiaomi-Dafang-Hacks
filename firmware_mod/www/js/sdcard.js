//Function to delete a file
function deleteFile(fileName,dir) {
    var del = confirm("Confirm delete file: "+fileName);
    if ( del ) { 
        $.get("cgi-bin/sdcard.cgi", {cmd: "del_file",file: fileName});
        getFiles(dir);
    }
}

//Function to get video and images files from dir
function getFiles(dir) {
    // Get files from dir
    $.get("cgi-bin/sdcard.cgi", {cmd: "getFiles", dir: dir}, function(config){             
        $('#'+dir).html(" <p></p>\
        <table class='w3-table-all' id='result'>\
        <thead>\
          <tr class='w3-theme'>\
            <th>Filename</th>\
            <th>Size</th>\
            <th>Date</th>\
            <th>Actions</th>\
          </tr>\
        </thead>\
        <tbody>");
        var config_all = config.split("\n");    
        if ( config_all.length == 1)
            $('#'+dir).html("<h1>No file found</h1>");
        for (var i = 0; i < config_all.length-1; i++) {
         var config_info = config_all[i].split("#:#");       
         $('#result').append("<tr> \
         <td>"+config_info[0]+"</td> \
         <td>"+config_info[1]+"</td> \
         <td>"+config_info[2]+"</td> \
         <td> \
             <a href=\""+config_info[3]+"\"><i class='fas fa-download'></i></a> \
            <span onclick=\"deleteFile('"+config_info[3]+"','"+dir+"')\"><i class='fas fa-trash'></i></span> \
         </td></tr>");       
        }
        $('#'+dir).append("</tbody></table><p></p>");
        var table = $('#result').DataTable();
        $('#result'+dir).on( 'click', 'tr', function () {
            //$(this).toggleClass('selected');
        } );
     
        $('#result'+dir).click( function () {
            //alert( table.rows('.selected').data().length +' row(s) selected' );
        } );

    });

}
//Function loaded when script load
function onLoad() {
    //Activate accordion
    accordion();
    //Get configuration
    getFiles('motion');

   
}

onLoad();


