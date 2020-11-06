//Function to delete a file
function deleteFile(fileName,dir,confirm) {
    if (confirm)
        var del = confirm("Confirm delete file: "+fileName);
        if ( del ) { 
            $.get("cgi-bin/ui_sdcard.cgi", {cmd: "del_file",file: fileName});
            getFiles(dir);
        }
    else {
        $.get("cgi-bin/ui_sdcard.cgi", {cmd: "del_file",file: fileName});
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
    $.get("cgi-bin/ui_sdcard.cgi", {cmd: "getFiles", dir: dir}, function(config){             
        $('#'+dir).html(" <p><button id='del_"+dir+"' class='w3-btn w3-theme'>Delete selected</button></p>\
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
            $('#'+dir).html("<h1>No files found</h1>");
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
            <span onclick=\"deleteFile('"+config_info[3]+"','"+dir+",true')\"><i class='fas fa-trash' title='Delete file'></i></span>\
            "+html_photo+"\
            </td></tr>");
        }
        $('#'+dir).append("</tbody></table><p></p>");

        var table = $('#result_'+dir).DataTable();
        $('#result_'+dir+' tbody').on( 'click', 'tr', function () {
            $(this).toggleClass('selected');
        } );
     
        $('#del_'+dir).click( function () {
            var del = confirm("Confirm delete of "+ table.rows('.selected').data().length +" files");
            if(del) {
                table.rows('.selected').data().each( function ( value, index ) {   
                    filename = value[3].split("\"");                 
                    deleteFile(filename[1],dir,false);
                } );
            }
        } );

    });

}

function showEvents() {

    $.getJSON("cgi-bin/ui_sdcard.cgi", {cmd: "events"}, function(data){             
        
        var events = data.filter(item => item.file.endsWith("jpg") ).map(item => {
            return { date: new Date(item.date),
                    detail: { 
                        file : item.file
                    }}; 
        });
       var chart = eventDrops({
        range: {
            start: events.reduce((a, b) => a.date < b.date ? a : b).date,
            end: events.reduce((a, b) => a.date > b.date ? a : b).date
          },
          drop: {
              date: d => d.date,
              onClick : data => {
                openPicture(data.detail.file);
              }
          }
        });
        d3.select('#events-graph').html("").datum([{ name: "Events", data : events}]).call(chart);
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


