/*
********* Easy bootstrap dialog boxes for web2py **************
*/
$(document).ready(function() {
	// need id to pass to web2py_component
	$('.modal-body').attr('id', 'modal-body')
	
	// bigger X to close
	$('.close').text("X")

	// set focus to first input field
	$('#myModal').on('shown', function () {
		$(this).find(':text:enabled:input:first').focus();
	});

	// primary button submits form
    $('#myModal').find('.btn-primary').click(function() {
	   	$('#modal-body').find('form').submit();
	})	
})

// call controller and place result in dialog box
function getdialog(url) {
	web2py_component(url, 'modal-body');
}
// called by response.js after form is available
function opendialog() {
	// hide form submit button as bootstrap primary button used instead
    $('#modal-body form :submit').css('display', 'none')
	
	$('#myModal').modal('show');
}
function closedialog() {
	$('#myModal').modal('hide');
}
 
// called by response.js to refresh any components that may have changed
function refresh(component) {
	var href = $("#" + component).attr("url")

	// for SQLFORM.grid add current page number to href
	page = $("#"+ component + " .web2py_paginator .current").text()
	if (page) {
		var symbol
		if (href.indexOf("?") < 0)
			symbol = "?"
		else
			symbol = "&"
		href = href + symbol + "page=" + page
	}
	web2py_component(href, component);
}