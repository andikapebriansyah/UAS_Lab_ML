import requests
import streamlit as st
from typing import List
import time

# You can change this URL based on where your API is running
API_URL = "http://localhost:8000/generate/"

st.set_page_config(
    page_title="Intelligent Email Writer", 
    layout="centered"
)

st.title("📝 Intelligent Email Writer for Students")

# Check API health
def check_api_health():
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Display API status
api_status = "🟢 Connected" if check_api_health() else "🔴 Disconnected (API not detected)"
st.sidebar.markdown(f"**API Status:** {api_status}")

# 1. Email category
category = st.selectbox(
    "Kategori Email",
    [
        "Akademik",
        "Bimbingan & Skripsi",
        "Magang / MBKM",
        "Beasiswa / Exchange",
        "Organisasi / Kepanitiaan",
        "Karier & Profesional",
        "Umum & Administratif"
    ]
)

# 2. Recipient
recipient = st.text_input(
    "Kepada",
    placeholder="e.g., Dosen Pembimbing, TU Fakultas, dst."
)

# 3. Subject
subject = st.text_input(
    "Subjek Email",
    placeholder="e.g., Permohonan Izin Tidak Hadir Kuliah"
)

# 4. Writing tone
tone = st.selectbox(
    "Gaya/Tone Penulisan",
    ["Formal dan Sopan", "Santai namun Sopan", "Netral"]
)

# 5. Language
language = st.selectbox(
    "Bahasa",
    ["Bahasa Indonesia", "Bahasa Inggris"]
)

# 6. Urgency level (optional)
urgency = st.selectbox(
    "Tingkat Urgensi",
    ["Biasa", "Tinggi", "Rendah"]
)

# 7. Main points (separated by new lines)
points_input = st.text_area(
    "Poin-poin Utama Isi Email",
    placeholder="Tuliskan poin-poin penting, satu poin per baris"
)
# Convert to list
points = [p.strip() for p in points_input.split("\n") if p.strip()]

# 8. Previous email example (optional)
example = st.text_area(
    "Contoh Email Sebelumnya (Opsional)",
    height=100
)

# Generate email
if st.button("✉️ Buat Email"):
    if not (recipient and subject and points):
        st.error("Mohon isi paling tidak: Kepada, Subjek, dan Poin-poin isi email.")
    else:
        # Show processing message
        with st.spinner("Sedang membuat email..."):
            # Build payload
            payload = {
                "category": category,
                "recipient": recipient,
                "subject": subject,
                "tone": tone,
                "language": language,
                "urgency_level": urgency,
                "points": points,
                "example_email": example
            }

            # Send to backend
            try:
                # Check if API is available first
                if not check_api_health():
                    st.error("⚠️ API tidak bisa diakses. Pastikan backend server sedang berjalan di http://localhost:8000")
                else:
                    # Send request to API
                    response = requests.post(API_URL, json=payload, timeout=30)
                    
                    # Check status code
                    response.raise_for_status()
                    
                    # Get data from response
                    data = response.json()
                    
                    # Display results
                    st.subheader("📄 Hasil Email")
                    st.markdown(data.get("generated_email", "– Tidak ada output –"))
                    
                    # Add copy button
                    st.success("Email berhasil dibuat! Anda dapat menyalin teks di atas.")
            
            except requests.exceptions.ConnectionError:
                st.error("Tidak dapat terhubung ke server API. Pastikan server sedang berjalan di http://localhost:8000")
            except requests.exceptions.HTTPError as e:
                st.error(f"Server Error {e.response.status_code}: {e.response.text}")
            except requests.exceptions.Timeout:
                st.error("Timeout: Server membutuhkan waktu terlalu lama untuk merespons.")
            except requests.exceptions.RequestException as e:
                st.error(f"Gagal menghubungi server: {e}")
            except Exception as e:
                st.error(f"Error tidak terduga: {str(e)}")

# Add .env file creation instructions
st.sidebar.markdown("---")
st.sidebar.markdown("### Cara Penggunaan")
st.sidebar.markdown("""
1. Pastikan backend server berjalan (`uvicorn app:app --reload`)
2. Buat file `.env` dengan isi `GEMINI_API_KEY=your_api_key_here`
3. Isi semua kolom yang diperlukan
4. Klik "Buat Email"
""")