function userClicked(username){
	$.ajax({
		type : 'POST',
		url : '/application-accepted',
		data : {
			username : username
		},
		success: function (value) {
			location.reload(); 
		}
	});
}