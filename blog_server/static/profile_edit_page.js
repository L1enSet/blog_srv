function show_change_avatar() {
	let form = document.getElementById("avatar-choices-form-registration");
	if(form.style.display == "none") {
	  form.style.display = "block";
	} else {
	  form.style.display = "none"
	}
}


function select_avatar(element) {
	let avatar_form = document.getElementById("input_avatar");
	console.log("avatar")
	avatar_form.value = element.value;
}


function change_avatar(element) {
	let avatar_form = document.getElementById("change_avatar");
	console.log("avatar-change")
	avatar_form.value = element.value;
}


