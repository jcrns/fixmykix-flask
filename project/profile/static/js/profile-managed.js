//Handling displayed
$('#transaction-div').show();
$('#messages-div').hide();
$('#settings-div').hide();

$("#anchor-tag-transactions a" ).click(function() {
	$('#transaction-div').show();
	$('#messages-div').hide();
	$('#settings-div').hide();
});
$( "#anchor-tag-messages a" ).click(function() {
	$('#transaction-div').hide();
	$('#messages-div').show();
	$('#settings-div').hide();
});
$( "#anchor-tag-settings a" ).click(function() {
	$('#transaction-div').hide();
	$('#messages-div').hide();
	$('#settings-div').show();
});
// Transactions Table
function transactionsHistory(){
	// Getting table
	var table = document.getElementById('transactions-history-table'); 

	// Creating Label Row
	var titleRow = document.createElement('tr');
  	titleRow.setAttribute('class', "bg-info");


	var titleName = document.createElement('td');
	titleName.innerHTML = "<span style='color: #fff;'>Title of Transaction</span>";

	var titleDescription = document.createElement('td');
	titleDescription.innerHTML = "<span style='color: #fff;'>Description</span>";

	var titleDate = document.createElement('td');
	titleDate.innerHTML = "<span style='color: #fff;'>Date</span>";

	var titleCostOrPaid = document.createElement('td');
	titleCostOrPaid.innerHTML = "<span style='color: #fff;'>Cost/Paid</span>";

	titleRow.append(titleName)
	titleRow.append(titleDescription)
	titleRow.append(titleDate)
	titleRow.append(titleCostOrPaid)
	table.appendChild(titleRow)

}
transactionsHistory();