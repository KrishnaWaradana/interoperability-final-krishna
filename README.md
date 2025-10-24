# Proyek UTS: Campus Event Registration Platform

[cite_start]Proyek ini adalah implementasi sistem registrasi event kampus menggunakan FastAPI, SQLite, dan HTML+Fetch API untuk memenuhi tugas Mata Kuliah Interoperability[cite: 2].

## Fitur
- Backend REST API (FastAPI)
- Database SQLite
- [cite_start]Frontend HTML + JS (Fetch API) 
- CRUD untuk Events
- Registrasi Peserta dengan validasi kuota

## Cara Menjalankan Aplikasi

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/](https://github.com/)KrishnaWaradana/interoperability-final-krishna.git
    cd interoperability-final-krishna
    ```

2.  **Setup Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # (atau .\venv\Scripts\activate di Windows)
    ```

3.  **Install Dependencies**
    ```bash
    pip install fastapi "uvicorn[standard]" sqlalchemy pydantic
    ```

4.  **Jalankan Backend (API)**
    Server akan berjalan di `http://127.0.0.1:8000`.
    ```bash
    uvicorn backend.main:app --reload
    ```

5.  **Buka Frontend**
    - Buka file `frontend/index.html` langsung di browser Anda.

6.  **(PENTING) Tambah Event**
    - Buka dokumentasi API di `http://127.0.0.1:8000/docs`.
    - Gunakan endpoint `POST /events/` untuk menambahkan beberapa data event baru.

## Daftar Endpoint API

- `POST /events/`: Menambah event baru.
- `GET /events/`: Menampilkan semua event.
- `PUT /events/{id}`: Mengubah data event.
- `DELETE /events/{id}`: Menghapus event.
- `POST /register/`: Menambahkan peserta baru ke event.
- `GET /participants/`: Menampilkan daftar peserta.
- `GET /docs`: Dokumentasi Swagger UI.
