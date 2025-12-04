function uploadOriginal() {
    const file = document.getElementById("originalVid").files[0];
    if (!file) {
        alert("Select a video!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload-original", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("result").innerText = JSON.stringify(data, null, 2);
    })
    .catch(err => alert("Error uploading original video"));
}


function verifyNew() {
    const file = document.getElementById("newVid").files[0];
    if (!file) {
        alert("Select a video!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("/verify-new", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("verifyResult").innerText = JSON.stringify(data, null, 2);
    })
    .catch(err => alert("Error verifying video"));
}
