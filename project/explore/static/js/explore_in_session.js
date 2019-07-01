function newPost(){
	if(document.getElementById('new-post-service-select').value == "design-shoes") {
		$('#design-shoes-selected').show();
		$('#clean-shoes-selected').hide();
	}
	if(document.getElementById('new-post-service-select').value == "clean-shoes") {
		$('#design-shoes-selected').hide();
		$('#clean-shoes-selected').show();
	}
}
$("#new-post-submit-button" ).click(function() {

	// Checking if shoes are being designed are cleaned and getting data based on that
	if(document.getElementById('new-post-service-select').value == "design-shoes") {
		// Defining variables that will be posted
		var shoeName = $('#new-post-shoe').val();
		var shoeDescription = $('#new-post-description').val();
		var cost = $('#new-post-design-shoes-cost').val();
		var selectedTime = $('#new-post-time-design-shoes-select').find(":selected").val();
		var username = $('#username').data("name");
		var shoe_artist = true;
		var clean_shoes = false;
	}

	if(document.getElementById('new-post-service-select').value == "clean-shoes") {
		// Defining variables that will be posted
		var shoeName = 'varies';
		var shoeDescription = 'cleaned';
		var cost = $('#new-post-clean-shoes-cost').val();
		var selectedTime = $('#new-post-time-clean-shoes-select').find(":selected").val();
		var username = $('#username').data("name");
		var shoe_artist = false;
		var clean_shoes = true;
	}

	if(shoeName == '' || shoeDescription == '' || selectedTime == 'none'){
		$('#error-message').html('Empty Field');
		return;
	} 
	if(clean_shoes == false && shoe_artist == false){
		$('#error-message').html('Service not selected');
		return;
	}
    // Delay
    var delay = 2500;
	$.ajax({
	  type : 'POST',
	  url : '/new-post-api',
	  data : {
	  	// Data that will be posted
	    shoe_name : shoeName,
	    shoe_description : shoeDescription,
	    cost : cost,
	    username : username,
	    selected_time: selectedTime,
	    clean_shoes : clean_shoes,
	    shoe_artist : shoe_artist
	  },
	  headers: {'X-Requested-With': 'XMLHttpRequest'},
	  success: function (value) {
	    setTimeout(function() {
	      if(value == "success"){
	        location.reload();
	        $('#dismiss-new-post-modal').click();
	      } else {
	      	alert(value)
	      }
	    }, delay);
	  }
	});
});