//Dropdown menu
var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
	dropdown[i].addEventListener("click", function () {
		this.classList.toggle("active");
		var dropdownContent = this.nextElementSibling;
		if (dropdownContent.style.display === "block") {
			dropdownContent.style.display = "none";
		} else {
			dropdownContent.style.display = "block";
		}
	});
}

//LIVE VIEW
$("#live").click(function () {
	$("#content").html("<div class='mdl-card__supporting-text text-center m-0'>" +
		"<img id='liveview' src='../cgi-bin/currentpic.cgi' class='img-fluid'/>" +
		"</div>" +
		"<div class='mdl-card__actions mdl-card--border text-center'>" +
		"<button id='up' class='mdl-button mdl-js-button mdl-button&#45;&#45;raised mdl-js-ripple-effect mdl-button&#45;&#45;colored'>" +
		"&#9650;" +
		"</button>" +
		"<a id='up' class='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect'\n" +
			"href='javascript:void(0)'>&#9650;</a>" +
		"<a id='down' class='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect'\n" +
		   "href='javascript:void(0)'>&#9660;</a>" +
		"<a id='left' class='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect'\n" +
		   "href='javascript:void(0)'>&#9668;</a>" +
		"<a id='right' class='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect'\n" +
		   "href='javascript:void(0)'>&#9658;</a>" +
		"</div>");
});

//COMMANDS
// UP COMMAND
$("#up").click(function () {
	$.get("../cgi-bin/action.cgi?cmd=motor_up").done(function (data) {
	});
	$("#log").html("<b>Send UP Command</b>")
});

// DOWN COMMAND
$("#down").click(function () {
	$.get("../cgi-bin/action.cgi?cmd=motor_down").done(function (data) {
	});
	$("#log").html("<b>Send DOWN Command</b>")
});

// LEFT COMMAND
$("#left").click(function () {
	$.get("../cgi-bin/action.cgi?cmd=motor_left").done(function (data) {
	});
	$("#log").html("<b>Send LEFT Command</b>")
});

// RIGHT COMMAND
$("#right").click(function () {
	$.get("../cgi-bin/action.cgi?cmd=motor_right").done(function (data) {
	});
	$("#log").html("<b>Send RIGHT Command</b>")
});

// IR LED TOGGLE
$("#ir_led").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "ir_led"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/action.cgi?cmd=ir_led_off").done(function (data) {
			});
			$('#ir_led_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/action.cgi?cmd=ir_led_on").done(function (data) {
			});
			$('#ir_led_toggle').prop('checked', true);
		}
	});
});

// IR CUT TOGGLE
$("#ir_cut").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "ir_cut"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/action.cgi?cmd=ir_cut_off").done(function (status) {
			});
			$('#ir_cut_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/action.cgi?cmd=ir_cut_on").done(function (data) {
			});
			$('#ir_cut_toggle').prop('checked', true);
		}
	});
});

// AUTO NIGHT DETECTION TOGGLE
$("#auto_night_detection").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "auto_night_detection"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/scripts.cgi?cmd=stop&script=auto-night-detection").done(function (status) {
			});
			$('#auto_night_detection_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/scripts.cgi?cmd=start&script=auto-night-detection").done(function (data) {
			});
			$('#auto_night_detection_toggle').prop('checked', true);
		}
	});
});

// BLUE LED TOGGLE
$("#blue_led").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "blue_led"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/action.cgi?cmd=blue_led_off").done(function (data) {
			});
			$('#blue_led_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/action.cgi?cmd=blue_led_on").done(function (data) {
			});
			$('#blue_led_toggle').prop('checked', true);
		}
	});
});

// YELLOW LED TOGGLE
$("#yellow_led").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "yellow_led"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/action.cgi?cmd=yellow_led_off").done(function (data) {
			});
			$('#yellow_led_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/action.cgi?cmd=yellow_led_on").done(function (data) {
			});
			$('#yellow_led_toggle').prop('checked', true);
		}
	});
});

// MOTION DETECTION TOGGLE
$("#motion_detection").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "motion_detection"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/action.cgi?cmd=motion_detection_off").done(function (data) {
			});
			$('#motion_detection_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/action.cgi?cmd=motion_detection_on").done(function (data) {
			});
			$('#motion_detection_toggle').prop('checked', true);
		}
	});
});

// RTSP H264 TOGGLE
$("#rtsp_h264").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "rtsp_h264"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/scripts.cgi?cmd=stop&script=rtsp-h264").done(function (data) {
			});
			$('#rtsp_h264_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/scripts.cgi?cmd=start&script=rtsp-h264").done(function (data) {
			});
			$('#rtsp_h264_toggle').prop('checked', true);
		}
	});
});

// RTSP MJPEG TOGGLE
$("#rtsp_mjpeg").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "rtsp_mjpeg"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/scripts.cgi?cmd=stop&script=rtsp-mjpeg").done(function (data) {
			});
			$('#rtsp_mjpeg_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/scripts.cgi?cmd=start&script=rtsp-mjpeg").done(function (data) {
			});
			$('#rtsp_mjpeg_toggle').prop('checked', true);
		}
	});
});

// MQTT STATUS TOGGLE
$("#mqtt_status").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "mqtt_status"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/scripts.cgi?cmd=stop&script=mqtt-status").done(function (data) {
			});
			$('#mqtt_status_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/scripts.cgi?cmd=start&script=mqtt-status").done(function (data) {
			});
			$('#mqtt_status_toggle').prop('checked', true);
		}
	});
});

// MQTT STATUS TOGGLE
$("#mqtt_control").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "mqtt_control"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/scripts.cgi?cmd=stop&script=mqtt-control").done(function (data) {
			});
			$('#mqtt_control_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/scripts.cgi?cmd=start&script=mqtt-control").done(function (data) {
			});
			$('#mqtt_control_toggle').prop('checked', true);
		}
	});
});

// SOUND ON STARTUP TOGGLE
$("#sound_on_startup").click(function () {
	$.get("../cgi-bin/state.cgi", {
		cmd: "sound_on_startup"
	}).done(function (status) {
		if (status.trim() == "ON") {
			$.get("../cgi-bin/scripts.cgi?cmd=stop&script=sound-on-startup").done(function (data) {
			});
			$('#sound_on_startup_toggle').prop('checked', false);
		} else {
			$.get("../cgi-bin/scripts.cgi?cmd=start&script=sound-on-startup").done(function (data) {
			});
			$('#sound_on_startup_toggle').prop('checked', true);
		}
	});
});

//ADMINISTRATIVE COMMANDS
$("#conf").click(function () {
	$("#content").load("../cgi-bin/status.cgi");
});

//MANAGE RUNNING SCRIPTS
$("#scripts").click(function () {
	$("#content").load("../cgi-bin/scripts.cgi");
});

//CONFIGURE MOTION
$("#motion").click(function () {
	$("#content").load("/configmotion.html");
});

//NETWORK
$("#network").click(function () {
	$("#content").load("../cgi-bin/network.cgi");
});

//LOGS
$("#logs").click(function () {
	$("#content").load("../cgi-bin/action.cgi?cmd=showlog");
});

//REBOOT
$("#reboot").click(function () {
	$("#content").html("<h1>Are you sure you want to reboot ?</h1> <br /><button onclick=\"window.location.href='../cgi-bin/action.cgi?cmd=reboot'\">YES</button> <button onclick=\"window.location.href='livestream.html'\">NO</button>")
});

setInterval(function () {
	$("#liveview").attr("src", "../cgi-bin/currentpic.cgi?" + new Date().getTime());
}, 4000);


function sync_states() {
	function sync_toggle(entity) {
		$.get("../cgi-bin/state.cgi", {
			cmd: entity
		}).done(function (status) {
			console.log(entity + " status " + status);
			if (status.trim() == "ON") {
				$('#' + entity + '_toggle').prop('checked', true);
			} else {
				$('#' + entity + '_toggle').prop('checked', false);
			}
		});
	}

	var entities = ["yellow_led", "blue_led", "ir_led", "ir_cut", "rtsp_h264", "rtsp_mjpeg", "auto_night_detection", "mqtt_status", "mqtt_control", "sound_on_startup", "motion_detection"];
	for (var i in entities) {
		sync_toggle(entities[i]);
	}
}

window.onload = sync_states;

setInterval(function () {
	sync_states()
}, 4000);