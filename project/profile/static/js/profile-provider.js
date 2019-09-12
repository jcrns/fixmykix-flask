function serviceObj(party){
	var serviceRequest = $('.service-request-' + party);
	var title = serviceRequest.data('title');
	scope = $(".scope-of-work-" + party)
	if (title != undefined && serviceRequest.length > scope.length){
		$("#request-obj").html("<h5>Scope Of Work</h5><p>TURN AROUND TIME: 4 WEEKS</p><h6>" + title + "</h6><textarea cols='5' rows='5' id='scope-of-work-description-services'  name='scope-of-work-description-services' placeholder='Description of services that will be provided'></textarea><small>Note: Be CLEAR on what services you will be providing</small><button id='scope-of-work-btn' class='btn btn-outline-success'>Confirm & Proceed Forward With Order</button>");
		$("#scope-of-work-btn").click(function() {
			var postId = serviceRequest.data('postid');
			var servicesDescription = $('#scope-of-work-description-services').val();
			$.ajax({
				type : 'POST',
				url : '/scope-of-work-post-api',
				data : {
					services_description : servicesDescription,
					party : party,
					post_id : postId
				},
				success: function (value) {
					alert(value);
				}
			});
		});
	} else {
		$("#request-obj").html("<h5 class='text-center'>Waiting for service request</h5>");
	}
}