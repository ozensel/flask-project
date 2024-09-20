from flask import Flask, render_template, request

app = Flask(__name__)

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Sonuçları işleyen sayfa
@app.route('/results', methods=['POST'])
def results():
    # Formdan gelen verileri al
    location = request.form.get('location')
    category = request.form.get('category')
    info_requested = request.form.getlist('info')  # Birden fazla checkbox seçilebilir
    
    # Burada Google Maps API'yi entegre edeceğiz
    # Simdilik formdan gelen verileri ekrana yazalım
    results = {
        "location": location,
        "category": category,
        "info_requested": info_requested
    }
    
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
