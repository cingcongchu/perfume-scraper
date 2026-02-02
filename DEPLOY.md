# Deployment Guide

Panduan lengkap untuk deploy Perfume Scraper ke web (GRATIS).

## 🎯 Overview

Kita akan deploy ke 2 platform gratis:
- **Backend** (Python/FastAPI) → Render.com
- **Frontend** (React) → Vercel.com

Total waktu: ~10 menit

---

## 📋 Prerequisites

1. Akun GitHub (gratis)
2. Akun Render.com (gratis)
3. Akun Vercel.com (gratis)
4. Project ini sudah di-push ke GitHub

---

## Step 1: Push ke GitHub

Jika belum, push project ini ke repository GitHub:

```bash
# Inisialisasi git (jika belum)
git init
git add .
git commit -m "Initial commit"

# Push ke GitHub
git remote add origin https://github.com/YOUR_USERNAME/perfume-scraper.git
git push -u origin main
```

---

## Step 2: Deploy Backend ke Render

### 2.1 Daftar Render
1. Buka https://render.com
2. Sign up dengan GitHub account
3. Verify email

### 2.2 Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect GitHub repository: **perfume-scraper**
3. Pilih repository Anda

### 2.3 Configure Service
Isi form berikut:

- **Name**: `perfume-scraper-backend`
- **Environment**: `Python 3`
- **Region**: `Singapore` (terdekat dengan Indonesia)
- **Branch**: `main`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
- **Plan**: `Free`

### 2.4 Environment Variables
Tambahkan Environment Variables:
```
PYTHON_VERSION = 3.10.0
```

### 2.5 Advanced Settings (Disk)
Untuk menyimpan database SQLite:
1. Scroll ke bawah ke **"Disks"**
2. Click **"Add Disk"**
3. **Name**: `sqlite-data`
4. **Mount Path**: `/opt/render/project/src`
5. **Size**: `1 GB`
6. **Plan**: `Standard` (Free tier)

### 2.6 Deploy
Click **"Create Web Service"**

⏳ **Tunggu 3-5 menit** untuk deploy selesai

### 2.7 Catat URL Backend
Setelah deploy selesai, Anda akan mendapat URL seperti:
```
https://perfume-scraper-backend.onrender.com
```

**Simpan URL ini!** Diperlukan untuk Step 3.

---

## Step 3: Update Frontend untuk Production

### 3.1 Update API URL
Buka file `frontend/src/services/perfumeService.ts`

Ganti baris:
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://perfume-scraper-backend.onrender.com'  // ← GANTI INI
    : 'http://localhost:8003');
```

Ganti `https://perfume-scraper-backend.onrender.com` dengan URL Anda dari Step 2.7

### 3.2 Commit & Push
```bash
git add .
git commit -m "Update API URL for production"
git push origin main
```

---

## Step 4: Deploy Frontend ke Vercel

### 4.1 Daftar Vercel
1. Buka https://vercel.com
2. Sign up dengan GitHub account
3. Verify email

### 4.2 Import Project
1. Click **"Add New..."** → **"Project"**
2. Import Git Repository: **perfume-scraper**
3. Click **"Import"**

### 4.3 Configure Project
**Framework Preset**: `Create React App`

**Root Directory**: `frontend`

**Build Command**: 
```bash
npm run build
```

**Output Directory**: `build`

**Install Command**:
```bash
npm install --legacy-peer-deps
```

### 4.4 Environment Variables
Click **"Environment Variables"** lalu tambahkan:
```
REACT_APP_API_URL = https://perfume-scraper-backend.onrender.com
```
(Ganti dengan URL backend Anda)

### 4.5 Deploy
Click **"Deploy"**

⏳ **Tunggu 2-3 menit**

### 4.6 Done! 🎉
Anda akan mendapat URL seperti:
```
https://perfume-scraper-xyz123.vercel.app
```

**Ini adalah URL aplikasi Anda yang bisa diakses dari mana saja!**

---

## Step 5: Testing

### 5.1 Buka Aplikasi
Buka URL Vercel Anda di browser

### 5.2 Test Scraping
1. Masukkan brand: `Chanel`
2. Pilih source: `Fragrantica`
3. Click **Search**
4. Tunggu 30-60 detik
5. Harusnya muncul hasil scraping

### 5.3 Troubleshooting

**Error CORS?**
- Pastikan URL Vercel sudah di-add di `backend/main.py` bagian CORS
- Restart backend di Render (click "Manual Deploy" → "Deploy latest commit")

**Error 500?**
- Check log di Render Dashboard → Logs
- Pastikan semua dependencies terinstall

**Tidak ada hasil scraping?**
- Fragrantica scraping butuh Chrome browser
- Render free tier mungkin tidak support Selenium/Chrome
- Solusi: Gunakan `SimplePerfumeScraper` (mock data) untuk demo

---

## 📱 Alternative: Deploy Frontend + Backend di 1 Platform

Jika ingin lebih simple, deploy semua di **Railway**:

1. Daftar https://railway.app
2. New Project → Deploy from GitHub repo
3. Railway akan otomatis detect Python + React
4. Deploy sekalian

Tapi Railway free tier terbatas (500 jam/bulan).

---

## 🔒 Keamanan & Limitasi

### Limitasi Render Free Tier:
- ⏰ Spin down after 15 menit idle (cold start ~30 detik)
- 💾 512 MB RAM
- 🗄️ 1 GB Disk
- 🌐 Shared CPU

### Limitasi Vercel Free Tier:
- 📦 100 GB bandwidth/month
- 🚀 10,000 requests/day
- ⏱️ Function timeout 10 seconds

### Tips:
- Untuk production serius, upgrade ke paid plan
- Atau gunakan VPS (DigitalOcean $5/bulan)

---

## 🚀 Next Steps

Setelah berhasil deploy:
1. ✅ Share link ke teman
2. ✅ Custom domain (bisa di Vercel)
3. ✅ Add Google Analytics
4. ✅ Implementasi caching untuk scraping
5. ✅ Upgrade database ke PostgreSQL

---

## 🆘 Bantuan

Jika ada masalah:
1. Check log di Render Dashboard
2. Check log di Vercel Dashboard
3. Pastikan environment variables sudah benar
4. Restart service (Manual Deploy)

**Selamat mencoba! 🎉**
