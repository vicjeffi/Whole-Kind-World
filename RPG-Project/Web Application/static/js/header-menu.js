var active = false
document.getElementById('notificationIcon').addEventListener('click', function () {
    if (!active){
        active = true
        this.classList.add("active");
    } else {
        active = false
        this.classList.remove("active");
    }
});