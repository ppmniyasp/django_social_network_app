$(document).ready(function(){
	$('#action_menu_btn').click(function(){
		$('.action_menu').toggle();
	});
});

// Get the scroll container
var scrollContainer = document.getElementById('chat-body');

// Set the scroll position to the bottom
scrollContainer.scrollTop = scrollContainer.scrollHeight;

// Remove class
document.getElementById('removeBold').addEventListener('click', function() {
    var myName = document.getElementById('myName');
	var myUsername = document.getElementById('myUsername')
    myName.classList.remove('bold');
	myUsername.classList.remove('bold')
  });