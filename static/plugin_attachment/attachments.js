// this enables attachments to be dragged/dropped

$(document).ready(function() {
	// stop file opening directly in the browser; and set icon to copy rather than move.
	$(document).on('dragover', function(e) {
							e.originalEvent.dataTransfer.dropEffect='copy';
							e.preventDefault(); e.stopPropagation();}
							)
	// optional but just in case. stop any other actions
	$(document).on('dragenter', function(e) {e.preventDefault(); e.stopPropagation();})
	$(document).on("drop", drop);

	// was needed on earlier versions of jquery as dataTransfer not included by default in jquery event parameter
	$.event.props.push('dataTransfer');
})
// capture documents from drag/drop
function drop(e) {
	dt=e.originalEvent.dataTransfer
	formdata = new FormData()

	// single or multiple files dropped
	if (dt.files.length > 0) {
		for (var i = 0; i < dt.files.length; i++) {
			formdata.append('files', dt.files[i]);
		}
		upload(formdata)
		return false
	}
	// url of an image or document from another web domain
	var url = $(dt.getData('text/html')).filter('img').attr('src');
	if (!url)
		url = $(dt.getData('text/html')).filter('a').attr('href');
	if (url) {
		formdata.append('url', url);
		upload(formdata)
		return false;
	}
}

// upload data added via drag/drop or from file system
function upload(formdata) {
	$.ajax({
		url : addurl,
		type : 'POST',
		data : formdata,
		cache : false,
		contentType : false,
		processData : false,
		error : function(response) {
			alert("Failed to upload file")
			return false
		},
		success : function(response) {
			var flash = jQuery('.flash');
			flash.hide();
			flash.html("Files uploaded")
			flash.slideDown();
			web2py_component($('#attachments').attr('data-w2p_remote'), 'attachments')
		}
	})
}