			$(document).ready(function () {
				$('img#motion_picture').selectAreas({
					minSize: [10, 10],
					onChanged: debugQtyAreas,
					width: 640
				});
				$('#btnView').click(function () {
					var areas = $('img#motion_picture').selectAreas('areas');
					displayAreas(areas);
				});
				$('#btnViewRel').click(function () {
					var areas = $('img#motion_picture').selectAreas('relativeAreas');
					displayAreas(areas);
				});
				$('#btnReset').click(function () {
					output("reset")
					$('img#motion_picture').selectAreas('reset');
				});
				$('#btnDestroy').click(function () {
					$('img#motion_picture').selectAreas('destroy');

					output("destroyed")
					$('.actionOn').attr("disabled", "disabled");
					$('.actionOff').removeAttr("disabled")
				});
				$('#btnCreate').attr("disabled", "disabled").click(function () {
					$('img#motion_picture').selectAreas({
						minSize: [10, 10],
						onChanged : debugQtyAreas,
						width: 500,
					});

					output("created")
					$('.actionOff').attr("disabled", "disabled");
					$('.actionOn').removeAttr("disabled")
				});
				$('#btnNew').click(function () {
					var areaOptions = {
						x: Math.floor((Math.random() * 200)),
						y: Math.floor((Math.random() * 200)),
						width: Math.floor((Math.random() * 100)) + 50,
						height: Math.floor((Math.random() * 100)) + 20,
					};
					output("Add a new area: " + areaToString(areaOptions))
					$('img#motion_picture').selectAreas('add', areaOptions);
				});
				$('#btnNews').click(function () {
					var areaOption1 = {
						x: Math.floor((Math.random() * 200)),
						y: Math.floor((Math.random() * 200)),
						width: Math.floor((Math.random() * 100)) + 50,
						height: Math.floor((Math.random() * 100)) + 20,
					}, areaOption2 = {
						x: areaOption1.x + areaOption1.width + 10,
						y: areaOption1.y + areaOption1.height - 20,
						width: 50,
						height: 20,
					};
					output("Add a new area: " + areaToString(areaOption1) + " and " + areaToString(areaOption2))
					$('img#motion_picture').selectAreas('add', [areaOption1, areaOption2]);
				});
			});

			var selectionExists;

			function areaToString (area) {
				return (typeof area.id === "undefined" ? "" : (area.id + ": ")) + area.x + ':' + area.y  + ' ' + area.width + 'x' + area.height + '<br />'
			}

			function output (text) {
				$('#output').html(text);
			}

			// Log the quantity of selections
			function debugQtyAreas (event, id, areas) {
				console.log(areas.length + " areas", arguments);
			};

			// Display areas coordinates in a div
			function displayAreas (areas) {
				var text = "";
				$.each(areas, function (id, area) {
					text += areaToString(area);
				});
				output(text);
			};
