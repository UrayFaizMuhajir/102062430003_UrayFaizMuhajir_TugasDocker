# 102062430003_UrayFaizMuhajir_TugasDocker

Aplikasi Flask untuk mengelola data mahasiswa yang terhubung ke MySQL, dijalankan dengan Docker Compose di Azure VM.

## Struktur
```
102062430003_UrayFaizMuhajir_TugasDocker/
├── app.py
├── templates/index.html
├── requirements.txt
├── Dockerfile          # multi-stage build (builder + runtime)
├── compose.yaml        # service app + database
├── .env.example        # contoh variabel rahasia
├── .gitignore          # .env tidak ikut di-push
└── .dockerignore
```

## Menjalankan
```
cp .env.example .env    # lalu isi password
sudo docker compose up -d --build
```
Buka `http://<IP_PUBLIC_VM>`.
