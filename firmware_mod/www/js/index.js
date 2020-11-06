var version

//Function to get parameters URL
$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results==null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
}

//Function open page 
function openPage(page) {
  $.get(page+".html",function(data) {
    $('#content').html(data);
  });
}

//Function to open tab in pages
function openTab(evt, tabName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("tab");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" w3-border-theme", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.firstElementChild.className += " w3-border-theme";
  }

//Function show/hide accordion
function accordion() {
  var acc = document.getElementsByClassName("accordion");
  var i;
  
  for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
      this.classList.toggle("active");
      var panel = this.nextElementSibling;
      if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
      } else {
        panel.style.maxHeight = panel.scrollHeight + "px";
      } 
    });
  }
}


function checkSDCard() {
  $.get("/cgi-bin/ui_sdcard.cgi", {cmd: "check_sdcard"}, function (result) {
    if ( result == "nok") {
      $('#notifAlarm').attr('style','color:red');
      $('#notifContent').html("<p></p>Your sdcard is mounted read-only. Settings can't be saved. \
      <br><p>Please try rebooting. If the problem persists, please <a target='_blank' href='https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/search?q=read+only+sdcard&type=Issues'> \
      search for possible solutions.</a></p>");
    }
  });
}

$(document).ready(function () {
  
    // Set git version to bottom page
    $.get("cgi-bin/state.cgi", {cmd: "version"}, function(version){document.getElementById("version").innerHTML = version;});

    // Check SD Card
    checkSDCard();

    // Display content depend url parameter
    if ( $.urlParam('url') != null )
        var url = $.urlParam('url')+".html"
    else
        var url = "live.html"

    //Check if theme configured
    var css = localStorage.getItem('theme')
    if ( css == null )
      css = "w3-theme-teal";
    //Select theme for theme modal
    $('#theme  option[value="'+css+'"]').prop("selected", true);
    // Set theme when changed in theme modal
    $('#theme').change(function () {
      var optionSelected = $(this).find("option:selected");
      localStorage.setItem("theme", optionSelected.val());
      location.reload();
    });
    
    $("#content").load(url);

});


