$( "#get-now-btn" ).click(function() {
	var splitUrl = window.location.pathname.split('/');
	var postId = splitUrl[2]
	$.ajax({
		type : 'POST',
		url : '/service-request-post-api',
		data : {
			post_id : postId
		},
		success: function (value) {
			location.reload(); 
		}
	});
});