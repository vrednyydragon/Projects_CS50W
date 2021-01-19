document.addEventListener('DOMContentLoaded', () => {
	var topping_list = []
	$('#pizza_table').on("click", "button", function(){
		var pizza_value = $(this).val().split(", ")
		console.log(pizza_value);
		// localStorage.setItem("pizza_value", pizza_value);
		localStorage.setItem("menu_position", pizza_value[0]);
		localStorage.setItem("pizza_id", pizza_value[1]);
		localStorage.setItem("price_category", pizza_value[2]);
		localStorage.setItem("topping_count", pizza_value[3]);
	});
	// work with modal window
	$('#myModal').on("shown.bs.modal", function(){
		// console.log("modal window")
		var text1 = $('#topping_info1')
		// console.log(text1[0])
		text1[0].innerHTML = "Choose " + localStorage.getItem("topping_count")+ " topping(s)"
	});

	$('#topping_table').on("click", "button", function(){
		var topping_value = $(this).val().split(",")
		console.log(topping_value) 
		if (topping_list.length < localStorage.getItem("topping_count")){
			topping_list.push(topping_value[0]);
			var text2 = $('#topping_info2')
			text2[0].innerHTML = topping_list.length + " topping(s) selected"
			var list = $('#selected_toppings_list');
			var li = document.createElement('li');
			li.innerHTML = topping_value[1]
			list.append(li)
		};
		if (topping_list.length == localStorage.getItem("topping_count")){
			var a = $('#confirm_pizza_link')
			console.log(localStorage.getItem("menu_position"))
			a[0].href = encodeURI("/add_in_basket/"+
			 				localStorage.getItem("menu_position")+"/"+
			 				localStorage.getItem("pizza_id")+"/"+
			 				localStorage.getItem("price_category")+ "/" +
			 				topping_list)

			console.log($("#confirm_btn"))
		}
		console.log(topping_list)
		console.log(topping_list.length)
	});

	$("#close_btn").on("click", function(){ 
		localStorage.clear()
		topping_list = []
		$('#topping_info2').empty()
		$('#selected_toppings_list li').remove()
	});
	$("#confirm_btn").on("click", function(){ 
		localStorage.clear()
		topping_list = []
		// $('#topping_info2').empty()
		// $('#selected_toppings_list li').remove()
	});

});


