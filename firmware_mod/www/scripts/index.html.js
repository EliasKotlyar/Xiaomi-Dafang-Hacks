var SWITCHES = [
    "yellow_led", "blue_led", "ir_led", "ir_cut",
    "rtsp_h264", "rtsp_mjpeg", "auto_night_detection",
    "mqtt_status", "mqtt_control",
    "sound_on_startup", "motion_detection", "motion_mail", "motion_telegram",
    "motion_led","motion_snapshot","motion_mqtt", "motion_mqtt_snapshot", "motion_mqtt_video"];

var timeoutJobs = {};

function refreshLiveImage() {
    var ts = new Date().getTime();
    $("#liveview").attr("src", "cgi-bin/currentpic.cgi?" + ts);
}
function scheduleRefreshLiveImage(interval) {
    if (timeoutJobs['refreshLiveImage'] != undefined) {
        clearTimeout(timeoutJobs['refreshLiveImage']);
    }
    timeoutJobs['refreshLiveImage'] = setTimeout(refreshLiveImage, interval);
}
function syncSwitch(sw) {
    var e = $('#' + sw);
    if (!e.prop('disabled')) {
        $.get("cgi-bin/state.cgi", {
            cmd: sw
        }).done(function (status) {
            // console.log(sw + " status " + status + " / current " + e.prop('checked'));
            e.prop('checked', (status.trim().toLowerCase() == "on"));
        });
    }
}
function syncSwitches() {
    for (var i in SWITCHES) {
        if (timeoutJobs[SWITCHES[i]] != undefined) {
            clearTimeout(timeoutJobs[SWITCHES[i]]);
        }
        syncSwitch(SWITCHES[i]);
    }
}

function showResult(txt) {
    var qv = $("#quickviewDefault");
    var v = $("#quicViewContent");
    if (qv.hasClass("is-active")) {
        // hide first if it's already active
        qv.toggleClass("is-active");
    }
    v.html(txt);
    qv.toggleClass("is-active");
    // auto close after 2.5 seconds
    setTimeout(function () { $("#quickViewClose").click(); }, 2500);
}

$(document).ready(function () {

    setTheme(getThemeChoice());

    // Set title page and menu with hostname
    $.get("cgi-bin/state.cgi", {cmd: "hostname"}, function(title){document.title = title;document.getElementById("title").innerHTML = title;});

    // Set git version to bottom page
    $.get("cgi-bin/state.cgi", {cmd: "version"}, function(version){document.getElementById("version").innerHTML = version;});

    // Show dpad according camera version
    $.get("cgi-bin/action.cgi", {cmd: "show_HWmodel"}, function(model){

        if (model == "Xiaomi Dafang\n") 
            document.getElementById("dpad_container").style.visibility = "visible";
        else
            document.getElementById("dpad_container").style.visibility = "hidden";
    });

    // Load link into #content
    $('.onpage').click(function () {
        var e = $(this);
        var target = e.data('target');
        var cachebuster = "_=" + new Date().getTime();
        if (target.indexOf("?") >= 0) {
            // append as additional param
            cachebuster = "&" + cachebuster;
        } else {
            // new param
            cachebuster = "?" + cachebuster;
        }
        $('#content').load(target + cachebuster);
    });
    // Load link into window
    $('.direct').click(function () {
        window.location.href = $(this).data('target');
    });
    // Ask before proceeding
    $('.prompt').click(function () {
        var e = $(this);
        if (confirm(e.data('message'))) {
            window.location.href = e.data('target');
        }
    });
    // Camera controls
    $(".cam_button").click(function () {
        var b = $(this);
        $.get("cgi-bin/action.cgi?cmd=" + b.data('cmd')).done(function (data) {
            setTimeout(refreshLiveImage, 500);
        });
    });

    // Switch controls
    $(".switch").click(function () {
        var e = $(this);
        e.prop('disabled', true);
        $.get("cgi-bin/state.cgi", {
            cmd: e.attr('id')
        }).done(function (status) {
            if (status.trim().toLowerCase() == "on") {
                $.get(e.data('unchecked')).done(function (data) {
                    e.prop('checked', false);
                });
            } else {
                $.get(e.data('checked')).done(function (data) {
                    e.prop('checked', true);
                });
            }
            e.prop('disabled', false);
        });
    });

    // Initial syncing of switches
    timeoutJobs['syncSwitches'] = setTimeout(syncSwitches, 10);
    $('#camcontrol_link').hover(function () {
        // for desktop
        var e = $(this);
        e.toggleClass('is-active');
        if (!e.hasClass('is-active')) {
            return;
        }
        // refresh switches on hover over Camera Controls menu
        if (timeoutJobs['syncSwitches'] != undefined) {
            clearTimeout(timeoutJobs['syncSwitches']);
        }
        timeoutJobs['syncSwitches'] = setTimeout(syncSwitches, 10);
    }, function () { $(this).toggleClass('is-active'); });

    // Hookup navbar burger for mobile
    $('#navbar_burger').click(function () {
        // for mobile
        var e = $(this);
        e.toggleClass('is-active');
        $('#' + e.data('target')).toggleClass('is-active');

        if (!e.hasClass('is-active')) {
            return;
        }
        // refresh switches on burger is tapped
        if (timeoutJobs['syncSwitches'] != undefined) {
            clearTimeout(timeoutJobs['syncSwitches']);
        }
        timeoutJobs['syncSwitches'] = setTimeout(syncSwitches, 10);
    });

    // Close action for quickview
    $("#quickViewClose").click(function () {
        $("#quickviewDefault").removeClass("is-active");
    });

    // Use the hash for direct linking
    if (document.location.hash != "") {
        $(document.location.hash).click();
    }

    // Make liveview self refresh
    $("#liveview").attr("onload", "scheduleRefreshLiveImage(1000);");

});

// set theme cookie
function setCookie(name, value) {
    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value) + "; path=/";
}
// get theme cookie
function getCookie(name) {
    var nameEQ = encodeURIComponent(name) + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ')
            c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0)
            return decodeURIComponent(c.substring(nameEQ.length, c.length));
    }
    return null;
}
function setTheme(c) {
    if (!c) {
        return;
    }
    // clear any existing choice
    $('.theme_choice').removeClass('is-active');

    var theme = $('#theme_choice_' + c);
    theme.addClass('is-active');    // set active
    if (theme.data('css')) {
        // Purge any current custom theme
        $('link.custom_theme').remove();

        // Append css to head
        var css = $('<link>', {
            'class': 'custom_theme',
            'rel': 'stylesheet',
            'href': theme.data('css'),
        });
        $('head').append(css);

        // reapply the custom css
        var customCss = $('#custom_css').clone();
        $('#custom_css').remove()
        $('head').append(customCss);
        setCookie('theme', c);
    }
}
function getThemeChoice() {
    var c = getCookie('theme');
    return c;
}
