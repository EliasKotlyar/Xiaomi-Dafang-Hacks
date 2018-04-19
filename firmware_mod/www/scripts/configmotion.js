function preview(img, selection) {
	if (!selection.width || !selection.height)
		return;

	var scaleX = 100 / selection.width;
	var scaleY = 100 / selection.height;

	$('#x0').val(selection.x1);
	$('#y0').val(selection.y1);
	$('#x1').val(selection.x2);
	$('#y1').val(selection.y2);
	$('#restart_server').val(1);
}

function setTracking(obj, init) {

	var ias = $('#picture').imgAreaSelect({
		instance: true
	});

	if ($(obj).is(":checked")) {
		ias.setOptions({
			hide: true
		});
		$('#picture').css('opacity', 0.5);
		$("#RegionDisabled").show();
		document.getElementById('motion_timeout').readOnly = false;
		document.getElementById('motion_timeout').style.backgroundColor = "#FFFFFF";

	} else {
		ias.setOptions({
			show: true
		});
		$('#picture').css('opacity', 1);
		$("#RegionDisabled").hide();
		document.getElementById('motion_timeout').readOnly = true;
		document.getElementById('motion_timeout').style.backgroundColor = "#B0E0E6";
	}
	ias.update();

	if (init == false) {
		$('#restart_server').val(1);
	}

}

$(function () {
	var httpRequest = new XMLHttpRequest();
	httpRequest.open('GET', 'cgi-bin/getMotionInfo.cgi', false);
	httpRequest.send(null);
	eval(httpRequest.responseText)
	$('#picture').imgAreaSelect({
		handles: true,
		fadeSpeed: 200,
		onSelectChange: preview,
		movable: true,
		persistent: true
	});
	var ias = $('#picture').imgAreaSelect({
		instance: true
	});

	if ((region_of_interest[0] == 0 && region_of_interest[1] == 0 && region_of_interest[2] == 0 && region_of_interest[3] == 0) ||
		(region_of_interest[0] > width || region_of_interest[1] > height || region_of_interest[2] > width || region_of_interest[3] > height)) {
		ias.setSelection(0, 0, width, height, true);
	}
	else {
		ias.setSelection(region_of_interest[0], region_of_interest[1], region_of_interest[2], region_of_interest[3], false);
	}

	$('#x0').val(region_of_interest[0]);
	$('#y0').val(region_of_interest[1]);
	$('#x1').val(region_of_interest[2]);
	$('#y1').val(region_of_interest[3]);
	$('#restart_server').val(0);
	$('#motion_indicator_color').val(motion_indicator_color).change();
	$('#motion_sensitivity').val(motion_sensitivity).change();
	console.log(motion_tracking);
	$('#motion_tracking').prop('checked', motion_tracking);
	$('#motion_timeout').val(motion_timeout).change();
	setTracking($('#motion_tracking').get(0), true);
});