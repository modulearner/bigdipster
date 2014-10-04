$(document).ready(function(){

	$(".button").click(function() {

		var $input_data = $('#new_content : input');

		var content_data = {}
		$input_data.each(function(){
			content_data[this.name] = $(this).val();
		});

		$.ajax({
			url: '/api/v0/contentnode',
			method: 'PUT',
			data: content_data,
			success: function(data){
				console.log(data);
			},
			error: function(){
				console.log("Request Failed!");
			}

		});
	});
});