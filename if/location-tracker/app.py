from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def receive_location():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    # Waktu saat lokasi diterima
    waktu = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Buat link Google Maps
    google_maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

    # Tampilkan di terminal
    print("\n" + "="*50)
    print(f"[{waktu}] LOKASI DITERIMA")
    print(f"Latitude  : {latitude}")
    print(f"Longitude : {longitude}")
    print(f"Google Maps: {google_maps_link}")
    print("="*50 + "\n")

    # Simpan ke file lokasi.txt
    with open('lokasi.txt', 'a', encoding='utf-8') as f:
        f.write(f"[{waktu}]\n")
        f.write(f"Latitude: {latitude}\n")
        f.write(f"Longitude: {longitude}\n")
        f.write(f"Google Maps: {google_maps_link}\n")
        f.write("-" * 40 + "\n")

    return jsonify({
        'status': 'success',
        'message': 'Lokasi berhasil diterima',
        'google_maps': google_maps_link,
        'waktu': waktu
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)