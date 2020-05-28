//Function to delete a file
function deleteFile(fileName,dir) {
    var del = confirm("Confirm delete file: "+fileName);
    if ( del ) { 
        $.get("cgi-bin/sdcard.cgi", {cmd: "del_file",file: fileName});
        getFiles(dir);
    }
}

//Function to open picure
function openPicture(img) {
    $('#modal_picture_content').html("<img class='w3-modal-content w3-center' src="+img+">");
    document.getElementById('modal_picture').style.display='block'
}

//Function to get video and images files from dir
function getFiles(dir) {
    // Get files from dir
    $.get("cgi-bin/sdcard.cgi", {cmd: "getFiles", dir: dir}, function(config){             
        $('#'+dir).html(" <p></p>\
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
        var config_all = config.split("\n");    
        if ( config_all.length == 1)
            $('#'+dir).html("<h1>No file found</h1>");
        for (var i = 0; i < config_all.length-1; i++) {
         var config_info = config_all[i].split("#:#");
         var file_info = config_info[3].split(".");       
         var html_photo = "";
         if (file_info[1] == "jpg")
            html_photo = "<span onclick='openPicture(\""+config_info[3]+"\");' title='View picture'><i class='far fa-eye'></i>";
         $('#result_'+dir).append("<tr> \
         <td>"+config_info[0]+"</td> \
         <td>"+config_info[1]+"</td> \
         <td>"+config_info[2]+"</td> \
         <td> \
             <a href=\""+config_info[3]+"\" download><i class='fas fa-download' title='Download file'></i></a> \
            <span onclick=\"deleteFile('"+config_info[3]+"','"+dir+"')\"><i class='fas fa-trash' title='Delete file'></i></span>\
            "+html_photo+"\
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


