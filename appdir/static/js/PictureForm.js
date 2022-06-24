function PictureForm() {
    var PicFormDiv = document.getElementById("PicFormDiv");
    if (PicFormDiv.style.display == 'none') {
        PicFormDiv.style.display = 'active';
    }
    if (PicFormDiv.style.display == 'active') {
        PicFormDiv.style.display = 'none';
    }
}