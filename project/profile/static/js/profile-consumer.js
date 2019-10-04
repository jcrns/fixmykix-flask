$("#service-btn-send").hide();
$(".service-request").hide();
function serviceObj(party){
	var serviceObj = $(".service-request-" + party);

	if (serviceObj.length > 0) {
		$("#request-obj").html("<h5>Waiting on response</h5>")
	} else {
		$.ajax({
			type : 'POST',
			url : '/get-services',
			data : {
				party : party
			},
			success: function (value) {
				serviceObjFormatting(value)
			}
		});
	}
}
function serviceObjFormatting(content) {
	// var econtent = JSON.parse(content);
	// alert(content[0]['username'])
	for (var i = 0; i < content.length; i++) {
		var shoeName = content[i]['shoe_name']
		var serviceDescription = content[i]['shoe_description']
		var postId = content[i]['post_id']
		var cost = content[i]['cost']
		var selectService = document.getElementById('service-request-post-select');
		var option = document.createElement("option");
		option.setAttribute("value", postId )
		var text = document.createTextNode(shoeName + "     " + serviceDescription + "  $" + cost);
		option.appendChild(text);
		selectService.appendChild(option);
	}

}

function serviceRequestSelected(){
	var selectTag = document.getElementById("service-request-post-select");
	var postId = selectTag.options[selectTag.selectedIndex].value;
	$("#service-selected-link").html("<a href='../post/" + postId + "' style='color: #000;'>Post Link</a>");
	$("#service-btn-send").show();
}

$("#service-btn-send" ).click(function() {
	var selectTag = document.getElementById("service-request-post-select");
	var postId = selectTag.options[selectTag.selectedIndex].value;
	// var message_socket = io(url + '/messages')
	// message_socket.emit('private_message', { 'username' : username_input, 'message' : message_input})
	$.ajax({
		type : 'POST',
		url : '/service-request-post-api',
		data : {
			post_id : postId
		},
		success: function (value) {
			alert(value)
		}
	});
});
