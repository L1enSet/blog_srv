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


function looked_form(element) {
	let form = document.forms.comment_form;
	console.log("activated")
	parrent = form.elements.parrent
	parrent.value = element.id

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


async function updateComment(article, selector) {
    const url = "http://127.0.0.1:8000/blog/article/"+article+"/"
    let html = await (await fetch(url)).text()
    let newdoc = new DOMParser().parseFromString(html, 'text/html');
    document.querySelector(selector).outerHTML = newdoc.querySelector(selector).outerHTML;
	console.log('Элемент '+selector+' был успешно обновлен');
	return true;

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