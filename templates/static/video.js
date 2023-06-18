function UploadVideo(){
    const title = document.getElementById('title').value;
        const desc = document.getElementById('desc').value;
        const file = document.getElementById('file_upload').files[0];
        const token = getCookie("token");
        fetch('/videos/upload', {
            method: 'POST',
            headers: {'Authorization': `Bearer ${token}`},
            body: JSON.stringify({
                              "title": title,
                              "description": desc,
                              "file": file})
        })
            .then((response) => console.log(response))
            .catch((error) => console.log(error));

    }



/*
const form = document.querySelector('form');
form.addEventListener('submit', UploadVideo);

function UploadVideo(event){
    event.preventDefault();
    const form = event.currentTarget;
    const url = new URL(form.action);
    const formData = new FormData(form);
    const token = getCookie("token");
    const fetchOptions = {
        method: form.method,
        headers: {'Authorization': `Bearer ${token}`},
        body: formData};

    fetch(url, fetchOptions)
        .then((response) => console.log(response))
        .then(data => {
            document.getElementById("responseArea").innerHTML = data;
        })
        .catch((error) => console.log(error));

}*/