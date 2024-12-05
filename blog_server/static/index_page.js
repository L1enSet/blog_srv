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