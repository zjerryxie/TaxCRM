///////////////// ajax error opens the web2py formatted error page ////////////////////////
$(document).ready(function() {
	$.ajaxSetup({
		type : 'POST',
	});
	//$(document).ajaxError(showerror)
});
// alert the url then open the web2py error page
function showerror(e, xhr, settings, exception) {
	alert('ajax error in: ' + settings.url)
	$.get('/admin/default/errors/crm/old.html', function(data) {
		errorurl = $('[href^="/admin/default/ticket"]', data).attr('href')
		// if not logged in then show login screen
		if(errorurl == undefined)
			errorurl = '/admin/default/errors/crm/old.html'
		window.location = errorurl
	})
}
/////////////////// dump variable contents /////////////////////////////////////
function dump(variable, level) {
	var output = "";
	if(!level)
		level = 0;

	//The padding given at the beginning of the line.
	var indent = "";
	for(var j = 0; j < level; j++)
	indent += "    ";

	if( typeof (variable) == 'object') {
		for(var item in variable) {
			var value = variable[item];

			if( typeof (value) == 'object') {
				output += indent + item + "...\n";
				output += dump(value, level + 1);
			} else {
				output += indent + item + " => " + value + "\n";
			}
		}
	} else {
		output = variable + " (" + typeof (variable) + ")";
	}
	alert(output)
	return;
}