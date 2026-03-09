# LAPORAN INTELIJEN KEAMANAN: ANALISIS SURXRAT V5 C2 PANEL

## 1. Ringkasan Eksekutif
Laporan ini merinci temuan teknis dari analisis **SURXRAT V5**, sebuah platform *Mobile Remote Access Trojan (RAT)* berbasis Android yang menargetkan pengguna di Indonesia. Platform ini beroperasi sebagai *Spyware-as-a-Service*, di mana satu infrastruktur digunakan oleh lebih dari **1.000 penyerang unik** untuk memantau lebih dari **3.700 korban aktif**.

---

## 2. Infrastruktur Teknis
Panel kontrol (C2) dihosting menggunakan layanan cloud modern untuk menghindari deteksi tradisional:
*   **Frontend:** `https://panel-penting-surxrat.vercel.app` (Hosted on Vercel)
*   **Backend:** Firebase Realtime Database
*   **Firebase Project ID:** `fir-e9e7b`
*   **Database URL:** `https://fir-e9e7b-default-rtdb.firebaseio.com`
*   **API Key:** `AIzaSyDfHMsNoknifGnkJEr6DJPSoEiwmbmlYBc`

---

## 3. Skala Operasional
Berdasarkan sensus data pada 9 Maret 2026:
*   **Total Korban Aktif:** 3.764 perangkat Android.
*   **Total Penyerang (User Panel):** 1.009 UID unik.
*   **Target Utama:** Pengguna di Indonesia (terdeteksi dari provider seluler: XL Axiata, Telkomsel, Tri, Axis).
*   **Perangkat Korban:** Mayoritas perangkat kelas menengah ke bawah (Oppo, Vivo, Samsung, Xiaomi, Nubia).

---

## 4. Analisis Kapabilitas Malware (Spyware)
Berdasarkan kode sumber JavaScript dan struktur database, SURXRAT memiliki kemampuan berikut:

### A. Surveillance & Penyadapan
*   **SMS & Call Logs:** Intersepsi real-time semua pesan masuk/keluar dan riwayat panggilan.
*   **Penyadapan Notifikasi:** Memantau notifikasi aplikasi pesan (WhatsApp, Telegram) dan aplikasi perbankan menggunakan *Accessibility Service*.
*   **Stealth Camera:** Mengambil foto secara diam-diam menggunakan kamera depan/belakang dan mengunggahnya dalam format Base64 ke Firebase.
*   **GPS Tracking:** Pelacakan lokasi presisi secara real-time yang diintegrasikan dengan Leaflet Maps di panel.
*   **Keylogging:** Memantau *clipboard* untuk mencuri password atau kode 2FA yang disalin pengguna.

### B. Kontrol Jarak Jauh (C2 Commands)
*   **Remote Lock:** Mengunci perangkat dengan PIN kustom dan mengganti wallpaper dengan gambar dari server penyerang (Top4Top).
*   **File Manager:** Akses penuh ke penyimpanan internal (List, Delete, Rename, Download). File seringkali dikirim melalui bot Telegram.
*   **Lag Sinyal:** Fitur destruktif untuk menghabiskan kuota data korban dengan melakukan download file besar secara terus-menerus.

### C. Persistensi & Anti-Detection
*   **Anti-Uninstall:** Memanfaatkan *Accessibility Service* untuk mencegah pengguna menghapus aplikasi (malware secara otomatis menekan tombol "Cancel" jika user mencoba uninstall).
*   **Hide Icon:** Aplikasi seringkali menyamar sebagai sistem (misal: "Setting" atau "Google Service") dan menyembunyikan ikonnya setelah instalasi.

---

## 5. Struktur Database Firebase
Penyerang mengorganisir data curian ke dalam jalur (path) berikut:
1.  `surxrat5/`: Metadata sistem korban, IP, lokasi, dan hasil foto kamera.
2.  `database/sms/`: Log SMS lengkap.
3.  `database/contacts/`: Daftar kontak telepon.
4.  `database/calls/`: Riwayat panggilan.
5.  `database/accounts/`: Daftar akun Google (Gmail) yang terhubung.
6.  `notif/`: Aliran notifikasi real-time dari aplikasi korban.
7.  `control/`: Antrian perintah yang dikirim dari panel ke perangkat.

---

## 6. Temuan Forensik Penting
*   **Kebocoran Kredensial:** Kredensial Firebase terpampang jelas dalam file JavaScript frontend (`index-0CLwk5Y_.js`), memungkinkan siapa saja dengan pengetahuan teknis untuk mengakses database penyerang.
*   **Multi-Tenancy:** Sistem ini dirancang untuk banyak penyerang sekaligus. Setiap korban ditandai dengan `UID` milik penyerang yang melakukan infeksi.
*   **Pencurian Akun:** Ditemukan ribuan email Gmail milik korban yang telah tereksfiltrasi, meningkatkan risiko serangan *Account Takeover* (ATO) pada layanan perbankan atau media sosial.

---

## 7. Kesimpulan & Rekomendasi
SURXRAT V5 adalah ancaman serius bagi privasi pengguna Android di Indonesia. Penggunaan *Accessibility Service* memberikan malware ini kontrol total atas perangkat.

**Rekomendasi bagi Korban:**
1.  Matikan izin *Accessibility Service* untuk aplikasi yang mencurigakan.
2.  Segera ganti password akun Google dan aktifkan 2FA menggunakan aplikasi authenticator (bukan SMS).
3.  Lakukan *Factory Reset* jika aplikasi tidak bisa dihapus secara normal.
