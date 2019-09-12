$('#clean-shoes-selected').hide();
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
