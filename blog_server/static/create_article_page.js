function select_tag(element) {
	let tag_form = document.getElementById("formGroupExampleInput");
	if (tag_form.value == "") {
	  tag_form.value += element.value
	} else {
	  tag_form.value += (", " + element.value)
	}
}