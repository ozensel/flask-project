from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'secret_key'  # Session kullanımı için gizli anahtar

# Google API Anahtarı
API_KEY = 'AIzaSyDIpjcdH8Cc3ojbUevwJVDFBZ1ZVTKgMkE'  # API anahtarınızı buraya ekleyin

def google_places_api(coordinates, category, include_phone, include_website, include_address, include_open_now, radius=7000):
    """Google Places API'den sadece belirli kurallara uygun yerleri alır ve tüm sayfaları getirir."""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={coordinates}&radius={radius}&type={category}&key={API_KEY}"

    # Eğer kullanıcı sadece açık olan işletmeleri görmek isterse, URL'ye open_now parametresi eklenir
    if include_open_now:
        url += "&opennow=true"

    places_list = []
    while True:
        response = requests.get(url)
        results = response.json().get('results', [])

        for place in results:
            place_details = fetch_place_details(place['place_id'])
            phone = place_details.get("formatted_phone_number")
            website = place_details.get("website")
            address = place.get("vicinity")
            is_open_now = place.get("opening_hours", {}).get("open_now", None)  # İşletmenin açık olup olmadığını çekiyoruz

            # Seçimlere göre telefon, web sitesi, adres ve açık/kapalı filtrelemesi
            place_info = {
                "name": place.get("name"),
                "is_open_now": "Açık" if is_open_now else "Kapalı" if is_open_now is not None else "Bilinmiyor"  # Açık/Kapalı bilgisi
            }
            
            if include_phone and phone and has_cep_tel(place_details):
                place_info["phone"] = phone

            if include_website and website:
                place_info["website"] = website

            if include_address and address:
                place_info["address"] = address

            places_list.append(place_info)

        # 50 sonuçla sınırlıyoruz
        if len(places_list) >= 50:
            break

        # Eğer next_page_token varsa, bir sonraki sayfayı sorgula
        next_page_token = response.json().get('next_page_token')
        if next_page_token and len(places_list) < 50:
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={API_KEY}"
        else:
            break

    return places_list

def fetch_place_details(place_id):
    """Google Places API kullanarak telefon ve web sitesi detaylarını alır."""
    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number,website&key={API_KEY}"
    response = requests.get(details_url)
    return response.json().get('result', {})

def has_cep_tel(details):
    """Detaylarda cep telefonu numarasının olup olmadığını kontrol eder."""
    phone_number = details.get("formatted_phone_number")
    if phone_number and phone_number.startswith('05'):
        return True
    return False

@app.route('/')
def index():
    # Session'dan verileri alıyoruz
    places_list = session.get('places_list', [])
    error_message = session.get('error_message')
    
    # Session'ı temizliyoruz ki sayfa yenilendiğinde sonuçlar tekrar gösterilmesin
    session.pop('places_list', None)
    session.pop('error_message', None)

    return render_template('index.html', places_list=places_list, error_message=error_message)

@app.route('/taramayi_baslat', methods=['POST'])
def taramayi_baslat():
    location = request.form.get('location_name')
    category = request.form.get('category')
    
    # Kullanıcının hangi bilgileri istediğini öğreniyoruz
    info = request.form.getlist('info[]')
    include_phone = 'Telefon Numarası' in info
    include_website = 'Web Sitesi' in info
    include_address = 'Adres' in info
    include_open_now = 'Açık Olan İşletmeler' in info

    # Konumu geocode API ile enlem ve boylam bilgisine çeviriyoruz
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={API_KEY}"
    geocode_response = requests.get(geocode_url).json()

    if geocode_response['status'] == 'OK':
        lat_lng = geocode_response['results'][0]['geometry']['location']
        coordinates = f"{lat_lng['lat']},{lat_lng['lng']}"
        
        # Yakın çevredeki yer bilgilerini çekiyoruz
        places_list = google_places_api(coordinates, category, include_phone, include_website, include_address, include_open_now)

        # Sonuçları session'a kaydediyoruz
        session['places_list'] = places_list

        return redirect(url_for('index'))
    else:
        # Hata durumunda session'a hata mesajını kaydediyoruz
        session['error_message'] = "Konum bulunamadı"
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
