$('#update-setup-button').click(function(){
    var delay = 2500;
    var background_info = $('#background-info').val();
    var write_about_brand = $('#write-about-brand').val();
    var username = $('#username').data("name");
    var clean_shoes = $('#clean-shoes').is(":checked");
    var shoe_artist = $('#shoe-artist').is(":checked");
    // var 
    $.ajax({
      type : 'POST',
      url : '/provider-setup-api',
      data : {
      	// Data that will be posted
        background_info : background_info,
        write_about_brand : write_about_brand,
        username : username,
        clean_shoes : clean_shoes,
        shoe_artist : shoe_artist
      },
      headers: {'X-Requested-With': 'XMLHttpRequest'},
      success: function (value) {
        setTimeout(function() {
          if(value == "success"){
            location.reload();
          } else {
          	alert(value)
          }
        }, delay);
      }
    });
});