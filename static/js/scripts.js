document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    form.addEventListener("submit", function() {
        form.classList.add("form-submitted");
    });
});

document.querySelectorAll('.form-check-input').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        if (this.checked) {
            alert(`${this.nextElementSibling.nextElementSibling.innerText} seçildi!`);
        }
    });
});
