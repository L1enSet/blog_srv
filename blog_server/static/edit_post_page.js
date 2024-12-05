function select_tag(element) {
	let tag_form = document.getElementById("formGroupExampleInput");
	if (tag_form.value == "") {
	  tag_form.value += element.value
	} else {
	  tag_form.value += (", " + element.value)
	}
}


async function sendAjaxUpdateTitle(element, event) {
    console.log("ok - sendAjaxUpdateTitle") //для отслеживания потом удалить
    event.preventDefault() //не будем рефрешить сраницу после сабмита формы

    const article_slug = element.name;
    const url = `http://127.0.0.1:8000/ajax/article_update/add_title/`+article_slug;
    const csrftoken = getCookie('csrftoken'); // Получение CSRF-токена
    
    //формируем данные и запрос
    let data = {
                'title': element.title.value}
    console.log(data)

    let response = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json;charset=utf-8',
                  'X-CSRFToken': csrftoken},
        title: element.title.value,
        body: JSON.stringify(data),
        });

    let result = await response.json();
    
    //апдейтим елемент
    selector = "title"+article_slug;
    console.log(selector);
    console.log(result.object)
    console.log(document.getElementById(selector).textContent)
    let title_data = result.object
    document.getElementById(selector).textContent = title_data; // тут проблема!


    event.target.reset(); // очищаем форму
    //updateComment(article=element.className, selector="#comment-block")
    return 0;
}


async function sendAjaxUpdateImage(element, event) {
    event.preventDefault();
    const article_slug = element.name;
    let file = element.image.files[0];
    //console.log(file.name)
    const url = `http://127.0.0.1:8000/ajax/article_update/add_image/`+article_slug;
    const csrftoken = getCookie('csrftoken'); // Получение CSRF-токена
    let data = new FormData()
    data.append("file", file)
    data.append("csrfmiddlewaretoken", csrftoken)
    let response = await $.ajax({
        url: `http://127.0.0.1:8000/ajax/article_update/add_image/`+article_slug,
        method: "POST",
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        dataType: 'json',
        mimeType: "multipart/form-data",
        success: function(data){
            // update block
            //console.dir(data);
            newImageUrl = `http://127.0.0.1:8000`+data.img
            imageElement = document.getElementById("image"+article_slug)
            imageElement.src = newImageUrl
            //console.log(newImageUrl)
            //console.log(imageElement.src)
    
        },
        
    });

    //console.log(response.json());
    return 0;
}


async function editArtcleItem(element, event) {
    event.preventDefault();
    const article_slug = element.name;
    const item_id = "item"+element.id;
    const form_id = element.id;
    const csrftoken = getCookie('csrftoken'); // Получение CSRF-токена
    //get form data
    let file = element.image.files[0];
    let text = element.text.value;
    let data = new FormData();

    data.append("file", file);
    data.append("text", text);
    data.append("item", form_id);
    data.append("csrfmiddlewaretoken", csrftoken);
    console.log(data);

    // create and send response
    let response = await $.ajax({
        url: `http://127.0.0.1:8000/ajax/article_update/item_article_edit/`+article_slug,
        method: "POST",
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        dataType: 'json',
        mimeType: "multipart/form-data",
        success: function(data){
            // update block
            //console.dir(data);
            if (data.status == "success") {
                newImageUrl = `http://127.0.0.1:8000`+data.img;
                imageElement = document.getElementById("item-image-"+form_id);
                imageElement.src = newImageUrl;

                textElement = document.getElementById("item-text-"+form_id);
                textElement.textContent = data.text;
                //console.log(newImageUrl);
                //console.log(imageElement.src);
            } else {
                //alert("status = " + {data.status}+"\nError = "+data.error);
                alert("hello")
            }
        },  
    });
    event.target.reset()
}