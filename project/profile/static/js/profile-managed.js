$(document).ready(function(){

	// Socket IO
	var url = 'http://localhost:8000'
	var socket = io.connect(url)
	socket.on('connect', function(){
		socket.on('username', function(){
			console.log('Username Added')
			socket.send('Username Added')
		});
	});

	var message_socket = io(url + '/messages')
	message_socket.emit('username', $('#username').val());
	$( "#submit-message-party" ).click(function() {
		var username_input =  $('#username-input-party').val();
		var message_input = $('#message-input-party').val();
		message_socket.emit('private_message', { 'username' : username_input, 'message' : message_input})
		$('#message-input-party').val('');
		$.ajax({
			url : '/new-message-api',
		    type : 'POST',
		    data : {
		        'username-input' : username_input,
		        'message-input' : message_input
		    },
		    success: function (value) {
		    	// Message span
				var messageSpan = document.createElement("span");
				messageSpan.classList.add("bg-secondary");
				messageSpan.setAttribute("style", "border-radius: 1px;");
				messageSpan.innerHTML += message_input

				// Message p
				var message = document.createElement("p");
				message.appendChild(messageSpan);
				message.setAttribute("class" ,"messages-" + username_input + " messages ");

				var messagesDiv = document.getElementById("new-messages-div");
				messagesDiv.appendChild(message)
				$('#main-div').scrollTop($('#main-div')[0].scrollHeight);
			}
		});
	});
	message_socket.on('new_message', function(msg){

		// Message span
		var messageSpan = document.createElement("span");
		messageSpan.classList.add("bg-white");
		messageSpan.setAttribute("style", "border-radius: 1px; float:right");
		messageSpan.innerHTML += msg.message

		// Message p
		var message = document.createElement("p");
		message.appendChild(messageSpan);
		message.setAttribute("class" ,"messages-" + msg.username + " messages ");

		// Checking if messages are shown
		if($(".messages-" + msg.username).is(":hidden")){
			message.setAttribute("style", "display:none;");
		}
		var messagesDiv = document.getElementById("new-messages-div");
		messagesDiv.appendChild(message)
		$('#view-messages').scrollTop($('#view-messages')[0].scrollHeight);
	});
});
// Div is already scrolled to bottom when clicked on
$('#view-messages').scrollTop($('#view-messages')[0].scrollHeight);

//Handling displayed
$('#transaction-div').show();
$('#messages-div').hide();
$('#view-messages').hide();
$('.service-request').hide();
$('.scope-of-work').hide();
$('#settings-div').hide();
$('#request-obj').hide();
$('#view-posts').hide();
$("#anchor-tag-transactions a" ).click(function() {
	$('#transaction-div').show();
	$('#messages-div').hide();
	$('#view-messages').hide();
	$('#settings-div').hide();
	$('#request-obj').hide();
	$('#view-posts').hide();
});
$( "#anchor-tag-messages a" ).click(function() {
	$('#transaction-div').hide();
	$('#messages-div').hide();
	$('#view-messages').show();
	$('#settings-div').hide();
	$('#request-obj').hide();
	$('#view-posts').hide();
	backToMessages();
});
$( "#anchor-tag-settings a" ).click(function() {
	$('#transaction-div').hide();
	$('#messages-div').hide();
	$('#view-messages').hide();
	$('#settings-div').show();
	$('#request-obj').hide();
	$('#view-posts').hide();
});
$("#anchor-tag-posts a").click(function () {
	$('#transaction-div').hide();
	$('#messages-div').hide();
	$('#view-messages').hide();
	$('#settings-div').hide();
	$('#request-obj').hide();
	$('#view-posts').show();
});
// Transactions Table
// function transactionsHistory(){
// 	// Getting table
// 	var table = document.getElementById('transactions-history-table'); 

// 	// Creating Label Row
// 	var titleRow = document.createElement('tr');
//   	titleRow.setAttribute('class', "bg-info");


// 	var titleName = document.createElement('td');
// 	titleName.innerHTML = "<span style='color: #fff;'>Title of Transaction</span>";

// 	var titleDescription = document.createElement('td');
// 	titleDescription.innerHTML = "<span style='color: #fff;'>Description</span>";

// 	var titleDate = document.createElement('td');
// 	titleDate.innerHTML = "<span style='color: #fff;'>Date</span>";

// 	var titleCostOrPaid = document.createElement('td');
// 	titleCostOrPaid.innerHTML = "<span style='color: #fff;'>Cost/Paid</span>";

// 	titleRow.append(titleName)
// 	titleRow.append(titleDescription)
// 	titleRow.append(titleDate)
// 	titleRow.append(titleCostOrPaid)
// 	table.appendChild(titleRow)

// }
// transactionsHistory();


function showConvo(party){
	$("#convo-past-list").hide();
	$("#send-message-form").attr("id","send-message-form-" + party);
	$("#username-input-party").attr("value",party);
	$(".messages-" + party).show();
	$("#back-from-messages").show();
	$("#message-title-p").html("<a href='" + party + "' style='color:#000'>" + party + "</a>");	
	$("#send-message-form-" + party).show();
	$("#messages").addClass( "row" );
	$('#request-obj').show();
	$('.service-request-' + party).show();
	$('.scope-of-work-' + party).show();
	$('.convo-list-item').hide();
	$('<hr id="hr">').insertBefore(".send-message-form-party");

	// Scrolling to bottom by default
	$('#view-messages').scrollTop($('#view-messages')[0].scrollHeight);

	// Service Request
	$("#service-request-post-select").html("<option selected disabled>Choose Service</option>")
	serviceObj(party);
	$('#service-request-username').text(party + "'s services");
}
function backToMessages() {
	$("#convo-past-list").show();
	$("#send-message-form").show();
	$(".messages").hide();
	$("#back-from-messages").hide();
	$("#message-title-p").text("Messages");	
	$(".send-message-form-party").hide();
	$(".service-request").hide();
	$(".scope-of-work").hide();
	$("#messages").removeClass( "row" );
	$('#request-obj').hide();
	$('.convo-list-item').show();
	$( "hr" ).remove("#hr");

	// Scrolling to bottom by default
	$('#view-messages').scrollTop($('#view-messages')[0].scrollHeight);
}
