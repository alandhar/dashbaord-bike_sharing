# Bike Sharing Dashbord
Dashboard interaktif untuk menganalisis data peminjaman sepeda berdasarkan dataset *Bike Sharing Dataset* (Washington D.C). Visualisasi dibangun menggunakan **Streamlit**, **Pandas**, **Matplotlib**, dan **Seaborn**.

## Fitur Utama
- Ringkasan statistik pengguna
- Visualisasi peminjaman berdasarkan waktu
- Pengaruh cuaca dan musim
- Perbandingan pengguna `casual` vs `registered`
---

## Setup Environment
### Clone Repository
```bash
git clone https://github.com/alandhar/dashbaord-bike_sharing.git
```
### Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Run Streamlit App
```bash
streamlit run dashboard/dashboard.py
```
