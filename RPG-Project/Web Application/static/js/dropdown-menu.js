document.addEventListener("DOMContentLoaded", function() {
    var dropdownArrows = document.querySelectorAll(".custom-event-dropdown-arrow");

    dropdownArrows.forEach(function(dropdownArrow) {
        dropdownArrow.addEventListener("click", function() {
            var dropdownList = dropdownArrow.closest('.custom-event-menu').querySelector(".custom-event-dropdown-list");
            alert(dropdownList.classList)
            if (!dropdownList.classList.contains("custom-event-dropdown-list.active")) {
                dropdownList.style.display = "block";
                dropdownList.classList.add("custom-event-dropdown-list.active");
            } else {
                dropdownList.style.display = "";
                dropdownList.classList.remove("custom-event-dropdown-list.active");
            }
        });
    });
});