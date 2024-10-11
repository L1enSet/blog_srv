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


function looked_form(element) {
	let form = document.forms.comment_form;
	console.log("activated")
	parrent = form.elements.parrent
	parrent.value = element.id

}


function select_tag(element) {
	let tag_form = document.getElementById("formGroupExampleInput");
	if (tag_form.value == "") {
	  tag_form.value += element.value
	} else {
	  tag_form.value += (", " + element.value)
	}
}

//AJAX

async function article_like_request(element) {
	const url = "http://127.0.0.1:8000/ajax/art_likes/"+element.id;		// константа урл адреса для запроса
	csrftoken = getCookie('csrftoken')
    response = await fetch(url, {
                                 method: 'POST',
                                 headers: {'Content-Type': 'application/json;charset=utf-8',
                                           'X-CSRFToken': csrftoken},
                                 })
    let json = await response.json()
    txt = element.querySelector("p")									// изменяем елемент
	txt.textContent = json["likes"]
	console.log( json["likes"] )
	console.log( request.responseText );
}


async function addLikeComment(element) {
    const url = "http://127.0.0.1:8000/ajax/comment_like/"+element.name;
    csrftoken = getCookie('csrftoken')
    response = await fetch(url, {
                                 method: 'POST',
                                 headers: {'Content-Type': 'application/json;charset=utf-8',
                                           'X-CSRFToken': csrftoken},
                                 })
    let result = await response.json()
    txt = element.querySelector("p")
    txt.textContent = result['likes']
}



async function send_ajax_comment(element, event) {
    event.preventDefault()
    const post_id = element.name;
    const url = `http://127.0.0.1:8000/ajax/art_comment/`+post_id;
    const csrftoken = getCookie('csrftoken'); // Получение CSRF-токена
    let data = {
                'parrent': element.parrent.value,
                'text': element.text.value}
    console.log(data)

    let response = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json;charset=utf-8',
                  'X-CSRFToken': csrftoken},
        parrent: element.parrent.value,
        text: element.text.value,
        body: JSON.stringify(data),
        });

    let result = await response.json();
    event.target.reset(); // очищаем форму
    updateComment(article=element.className, selector="#comment-block")
    return 0;
}


async function deleteComment(element) {
    const url = "http://127.0.0.1:8000/ajax/delete_comment/"+element.name;
    csrftoken = getCookie('csrftoken')
    response = await fetch(url, {
                                 method: 'POST',
                                 headers: {'Content-Type': 'application/json;charset=utf-8',
                                           'X-CSRFToken': csrftoken},
                                 })
    let result = await response.json()
    updateComment(article=element.id, selector="#comment-block")
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break; // Выходим, как только найдём нужное cookie
            }
        }
    }
    return cookieValue;
}


async function updateComment(article, selector) {
    const url = "http://127.0.0.1:8000/blog/article/"+article+"/"
    let html = await (await fetch(url)).text()
    let newdoc = new DOMParser().parseFromString(html, 'text/html');
    document.querySelector(selector).outerHTML = newdoc.querySelector(selector).outerHTML;
	console.log('Элемент '+selector+' был успешно обновлен');
	return true;

}