document.addEventListener('DOMContentLoaded', function() {
    // Kategori dropdown'ını doldur
    const categoryDropdown = document.getElementById('category');
    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.value;
        option.text = category.label;
        categoryDropdown.appendChild(option);
    });

    // Şehir veya İlçe input alanına "Enter" tuşu ile gönderimi engelle
    const locationInput = document.getElementById('location_name');
    locationInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();  // Enter tuşunun formu göndermesini engelle
        }
    });
});

let autocomplete;
function initializeAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('location_name'),
        { types: ['geocode'], componentRestrictions: { country: 'tr' } }
    );
    autocomplete.setFields(['geometry', 'name']);
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    const place = autocomplete.getPlace();
    if (!place.geometry) {
        document.getElementById('location_name').placeholder = 'Yer bulunamadı';
    } else {
        console.log("Seçilen yer: ", place.name);
    }
}
