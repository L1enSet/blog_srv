//page varriables
var tagArticleList = new Array();
function readTags() {
    let html = document.getElementsByClassName("article-tag");
    for (i=0; i<html.length; i++) {
        tagArticleList.push(html[i].name)
    }
}
readTags()
console.log(tagArticleList)




function select_tag(element) {
	let tag_form = document.getElementById("formGroupExampleInput");
	if (tag_form.value == "") {
	  tag_form.value += element.value
	} else {
	  tag_form.value += (", " + element.value)
	}
}


function showForm(element) {
    form = document.getElementById("form-block-"+element.name)
    console.log(form.style.getPropertyValue('display'))
    if (form.style.display == 'none') {
        form.style.display = 'block'
    } else if(form.style.display == 'block') {
        form.style.display = 'none'
    }
    
}


function upgradeItems(srvResponse, method, itemId) {
    const containerId = "content-items-block"
    let html = `<div class="container item-block" id="item-block-${srvResponse.id}">`

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
            <a type="button" class="btn btn-success my-2 my-sm-0">Change</a>
            <a type="button" name="${srvResponse.id}" class="btn btn-warning my-2 my-sm-0" onclick="deleteArticleItem(this)">Delete</a>
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
        </div>
        `
        html += formDiv

        //add html to page
        let contentBlock = document.getElementById(containerId)
        contentBlock.innerHTML += html
        
    } else if (method=="delete") {
        let item = document.getElementById(`item-block-`+itemId)
        console.log(itemId)
        console.log(item)
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
    let itemId = element.name;

    //create and send request
    let response = await $.ajax({
        url: `http://127.0.0.1:8000/ajax/article_update/delete_content_block/`+itemId,
        method: "GET",
        success: function(data){
            if (data.status) {
                upgradeItems(data, method="delete", itemId=itemId)
            }
        }
    })
}


// next 2 functions edit global varriable "tagArticleList"
function addTag(element) {
    let tagList = document.getElementById("tag-list-container")
    let html = `
        <a type="button" href="#!" name="${element.name}" id="tag-item-${element.name}" class="btn btn-outline-success article-tag"><b>#${element.getAttribute("data-tagName")}</b></a>
        <a type="button" class="btn btn-success my-2 my-sm-0" data-tagName="${element.name}" onclick="deleteTag(this)">X</a>
        `
    if (tagArticleList.indexOf(element.name)>=0) {
        alert("tag just here")
    } else {
        console.log("no")
        tagList.innerHTML += html
        tagArticleList.push(element.name)
    }
    
    console.log(tagArticleList)   
}


function deleteTag(element) {
    let htmlTag = document.getElementById("tag-item-"+element.getAttribute("data-tagName"))
    console.log(htmlTag)
    let indexElement = tagArticleList.indexOf(element.getAttribute("data-tagName"))
    console.log(indexElement)
    tagArticleList.splice(indexElement, 1)
    console.log(tagArticleList)
    htmlTag.style = "display: none"
    element.style = "display: none"
}

async function editArticleTags(element) {
    const article = element.getAttribute("data-article");
    const url = `http://127.0.0.1:8000/ajax/article_update/edit_article_tags/`+article;
    csrftoken = getCookie('csrftoken')

    data = new FormData()
    data.append("csrfmiddlewaretoken", csrftoken)
    data.append("tags", tagArticleList);
    //create request
    let respose = await $.ajax({
        url: url,
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
    })
}