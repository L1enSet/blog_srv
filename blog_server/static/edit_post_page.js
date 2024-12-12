function select_tag(element) {
	let tag_form = document.getElementById("formGroupExampleInput");
	if (tag_form.value == "") {
	  tag_form.value += element.value
	} else {
	  tag_form.value += (", " + element.value)
	}
}


function showForm(element) {
    console.log("1")
    form = document.getElementById(element.name)
    console.log("2")
    form.style.display = ''
    console.log("3")
}


function upgradeItems(srvResponse, method, itemId=undefined) {
    const containerId = "content-items-block"
    let html = ""

    if (method=="add") {
        //create html element
        if(srvResponse.img) {
            let imageDiv = `
            <div class="image-block">
                <img src="${srvResponse.img}" class="img-fluid mt-2 ml-2" id="item-image-${srvResponse.id}" alt="Responsive image" height="600" width="98%">
            </div>
            `

            html += imageDiv
        }

        if(srvResponse.text){
            let textDiv = `
            <div class="text-block">
                <p id="item-text-${srvResponse.id}">${srvResponse.text}</p>
            </div>
            `

            html += textDiv
        }

        let controlPanelDiv = `
        <div class="control-panel">
            <button type="button" class="btn btn-success my-2 my-sm-0">Change</button>
            <button type="button" class="btn btn-warning my-2 my-sm-0">Delete</button>
        </div>
        `
        html += controlPanelDiv

        let formDiv =  `
        <div class="item-edit-form form-element">
            <form id="${srvResponse.id}" name="${srvResponse.slug}" onsubmit="editArtcleItem(this, event)">
                <div class="mb-3">
                <label for="itemImageForm${srvResponse.id}" class="form-label">Item image</label>
                    <input class="form-control" type="file" name="image" id="itemImageForm${srvResponse.id}">
                </div>
                <div class="mb-3">
                    <label for="itemTextForm${srvResponse.id}" class="form-label">Item text</label>
                    <textarea class="form-control" name="text" id="itemTextForm${srvResponse.id}" rows="3"></textarea>
                </div>
                <button type="submit">Изменить</button>
            </form>
                            
        </div>
        `
        html += formDiv

        //add html to page
        let contentBlock = document.getElementById(containerId)
        contentBlock.innerHTML += html
        
    } else if (method=="delete") {
        let item = document.getElementById(`item`+itemId)
        item.innerHTML = html
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


async function addArticleItem(element, event) {
    event.preventDefault();
    const article_slug = element.name;
    const csrftoken = getCookie('csrftoken'); // Получение CSRF-токена
    
    //get form data
    let file = element.image.files[0];
    let text = element.text.value;
    let data = new FormData();

    data.append("file", file);
    data.append("text", text);
    data.append("csrfmiddlewaretoken", csrftoken);
    console.log(data); 

    // create and send request
    let response = await $.ajax({
        url: `http://127.0.0.1:8000/ajax/add_content_block/`+article_slug,
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
            if (data.status) {
                upgradeItems(data, method="add")
            }
        },  
    });
    event.target.reset()
}


async function deleteArticleItem(element) {
    console.log("delete item")
    const itemId = element.name;

    //create and send request
    let responce = await $.ajax({
        url: `http://127.0.0.1:8000/ajax/article_update/delete_content_block/`+itemId,
        method: "DELETE",
        success: function(data){
            if (data.status) {
                upgradeItems(data, method="delete", itemId=itemId)
            }
        }
    })
}