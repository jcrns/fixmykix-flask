// Handling search
$("#range-value-display").html("Value: $50")
function updateTextPriceValueInput(e){
	$("#range-value-display").html("Value: $" + e)
}
$("#filter-btn").click(function () {
	alert("qergwrtgw");
	var selectedService = $("#selected-service").val();
	var selectedBrand = $("#selected-brand").val();
	alert(selectedService)
	var tags = $("#filter-tags").val()
	var maxPrice = $("#filter-price-change").val()
	window.location.href = '/explore?service_type=' + selectedService + "&selected_brand=" + selectedBrand + "&tags=" + tags + "&max_price=" + maxPrice;
});