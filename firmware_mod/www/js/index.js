//Function to get parameters URL
$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}

$(document).ready(function () {
   
    // Set title page
    $.get("cgi-bin/state.cgi", {cmd: "hostname"}, function(title){document.title = title;document.getElementById("title").innerHTML = title;});

    // Set git version to bottom page
    $.get("cgi-bin/state.cgi", {cmd: "version"}, function(version){document.getElementById("version").innerHTML = version;});



    // Display content depend url parameter
    if ( $.urlParam('url') != null )
        var url = $.urlParam('url')+".html"
    else
        var url = "live.html"

    $("#content").load(url);
});


