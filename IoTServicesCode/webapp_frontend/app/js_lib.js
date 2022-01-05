/*
 * Javascript file to implement client side usability
 * Operating Systems Design exercises.
 */

 var server_address = "http://35.241.129.25:5000/"

 var device = document.getElementById("currentDevice").innerHTML;

 var get_current_sensor_data = function(){
	  let s_start = document.getElementById("start").value
	 if (s_start != "") {
		 let d_start = new Date(s_start);
		 start = d_start.getTime()/1000;
	 }
	 else
	 	start = 0
	 let s_end = document.getElementById("end").value
	 if (s_end != "") {
		 let d_end = new Date(s_end);
		 end = d_end.getTime()/1000;

	 }
	 else
	 	end = 8640000000000000
     $.getJSON( server_address+"dso/measurements/",{device_id: device, start: start, end: end}, function(data) {

         let html = '<tr class="fields">' +
                        '<th><div class="header_field"><i class="gg-sun"></i>Temperature</div></th>' +
                        '<th><div class="header_field"><i class="gg-drop"></i>Humidity</div></th>' +
                        '<th><div class="header_field"><i class = "gg-calendar-dates"></i>Time</div></th>' +
                    '</tr>';
         $.each(data, function (key, val) {

	 html += '<tr class=\'row ' + val.device_id + '\'>' +
				'<td>'+ val.temperature + '</td>' +
				'<td>'+ val.humidity + '</td>' +
				'<td>'+ val.date_time + '</td>';

	});
        $(".sensor_measures").html(html);
     });
 }

 var get_device_list = function(){
     $.getJSON(server_address+"dso/devices/", function(data) {
          let html = '<tr class="fields">' +
                        '<th><div class="header_field"><i class="gg-data"></i>Device ID</div></th>' +
			'<th><div class="header_field"><i class="gg-check-o"></i>Status</div></th>' +
                        '<th><div class="header_field"><i class="gg-arrow-align-v"></i>Latitude</div></th>' +
                        '<th><div class="header_field"><i class = "gg-arrow-align-h"></i>Longitude</div></th>' +
                        '<th><div class="header_field"><i class = "gg-calendar-dates"></i>Time</div></th>' +
			'<th></th>' +
                    '</tr>';
         $.each(data, function (key, val) {
            	//These two variables will be used as auxiliar quoting elements for the correct specification of strings
		let  single_quote = "'";
		let double_quote = '"';
		
		html += '<tr class="row device_row">' +
                        '<td>' + val.device_id + '</td>' +
			'<td>' + val.status + '</td>' +
                        '<td>'+ val.latitude + '</td>' +
                        '<td>'+ val.longitude + '</td>' +
                        '<td>'+ val.date_time + '</td>' +
			'<td><button type="button" onclick=' + single_quote + 'filter(' + double_quote + val.device_id + double_quote + ')' + single_quote + ' class="measure">Measurements</button></td>';
                    '</tr>';
         });
         $(".device_list").html(html);
     });
 }

function filter(deviceID) {
 	device = deviceID;
	document.getElementById("currentDevice").innerHTML = deviceID;
	document.getElementsByClassName("div_devices")[0].style.display="none"; //hidding the devices table
	document.getElementsByClassName("div_measurements")[0].style.display="block"; //showing the measurements table
}

function goBack(){
	document.getElementsByClassName("div_measurements")[0].style.display="none"; //hidding the measurements table
	document.getElementsByClassName("div_devices")[0].style.display="block"; //showing the devices table	
}

setInterval(get_device_list,2000)
setInterval(get_current_sensor_data, 2000)
