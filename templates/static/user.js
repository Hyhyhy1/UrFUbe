function onDataInput(){
    if(event.key === 'Enter'){

        let input_data = document.getElementById('name').value;
        const url = '/user/'+ input_data.toString();
        const label = document.getElementById('label');
        fetch(url)
            .then(responce => responce.json())
            .then(data => videoLinkGenerator(data))
            .catch(()=>{label.textContent = 'Wrong username';})

    }

}


function videoLinkGenerator(data){
    const label = document.getElementById('label');
    label.classList.add('disabled');
    const input_field = document.getElementById('name');
    input_field.classList.add('disabled');
    let linksContainer = document.getElementById("links_container");
    for(var item in data){
        item = data[item]
        let listElement = document.createElement('li');
        listElement.className += "watch_link_container";
        let link = document.createElement('a');
        link.className += "watch_link";
        link.textContent = item['title'];
        link.href = '/index/' + item['id']

        listElement.appendChild(link);
        linksContainer.appendChild(listElement)
    }
}

function UploadVideo(){
    window.location.href = 'videos/upload'
}