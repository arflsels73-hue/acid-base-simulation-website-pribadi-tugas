import streamlit as st
import math

# Pengaturan dasar halaman agar terlihat modern, interaktif, dan luas
st.set_page_config(
    page_title="Lab Virtual pH Asam-Basa",
    page_icon="🧪",
    layout="wide"
)

# --- DATABASE SENYAWA KIMIA ---
# Menyimpan informasi lengkap valensi, nilai tetapan (Ka/Kb), dan rumus ionisasi secara rapi
DATABASE_SENYAWA = {
    "Asam (Acid)": {
        "Kuat (Strong)": {
            "Asam Klorida (HCl) - Asam Lambung": {
                "valensi": 1, 
                "rumus_disosiasi": r"\text{HCl} \rightarrow \text{H}^+ + \text{Cl}^-",
                "info_senyawa": "Asam kuat yang terdapat di lambung manusia untuk membantu pencernaan makanan."
            },
            "Asam Nitrat (HNO3)": {
                "valensi": 1, 
                "rumus_disosiasi": r"\text{HNO}_3 \rightarrow \text{H}^+ + \text{NO}_3^-",
                "info_senyawa": "Asam kuat industri yang digunakan untuk pembuatan pupuk dan bahan peledak."
            },
            "Asam Sulfat (H2SO4) - Air Aki": {
                "valensi": 2, 
                "rumus_disosiasi": r"\text{H}_2\text{SO}_4 \rightarrow 2\text{H}^+ + \text{SO}_4^{2-}",
                "info_senyawa": "Asam kuat diprotik yang digunakan sebagai cairan elektrolit pada akumulator (aki)."
            },
            "Kustom / Input Manual": {
                "valensi": 1, 
                "rumus_disosiasi": r"\text{HA} \rightarrow \text{H}^+ + \text{A}^-",
                "info_senyawa": "Gunakan opsi ini untuk menghitung senyawa asam kuat kustom pilihan Anda sendiri."
            }
        },
        "Lemah (Weak)": {
            "Asam Asetat / Cuka (CH3COOH)": {
                "nilai": 1.8e-5, 
                "rumus_disosiasi": r"\text{CH}_3\text{COOH} \rightleftharpoons \text{H}^+ + \text{CH}_3\text{COO}^-",
                "info_senyawa": "Asam organik lemah yang memberikan rasa masam khas pada cuka dapur makanan."
            },
            "Asam Format / Semut (HCOOH)": {
                "nilai": 1.8e-4, 
                "rumus_disosiasi": r"\text{HCOOH} \rightleftharpoons \text{H}^+ + \text{HCOO}^-",
                "info_senyawa": "Asam lemah yang diproduksi secara alami oleh semut sebagai mekanisme pertahanan diri."
            },
            "Asam Sianida (HCN)": {
                "nilai": 6.2e-10, 
                "rumus_disosiasi": r"\text{HCN} \rightleftharpoons \text{H}^+ + \text{CN}^-",
                "info_senyawa": "Gas atau cairan asam yang sangat beracun bagi tubuh manusia bahkan dalam kadar rendah."
            },
            "Asam Fluorida (HF)": {
                "nilai": 6.8e-4, 
                "rumus_disosiasi": r"\text{HF} \rightleftharpoons \text{H}^+ + \text{F}^-",
                "info_senyawa": "Asam lemah yang sangat reaktif, sering digunakan khusus untuk mengukir permukaan kaca."
            },
            "Kustom / Input Manual": {
                "nilai": 1.8e-5, 
                "rumus_disosiasi": r"\text{HA} \rightleftharpoons \text{H}^+ + \text{A}^-",
                "info_senyawa": "Gunakan opsi ini untuk menghitung senyawa asam lemah kustom pilihan Anda sendiri."
            }
        }
    },
    "Basa (Base)": {
        "Kuat (Strong)": {
            "Natrium Hidroksida (NaOH) - Soda Api": {
                "valensi": 1, 
                "rumus_disosiasi": r"\text{NaOH} \rightarrow \text{Na}^+ + \text{OH}^-",
                "info_senyawa": "Basa kuat kaustik yang banyak digunakan dalam pembuatan sabun mandi keras dan pembersih pipa."
            },
            "Kalium Hidroksida (KOH)": {
                "valensi": 1, 
                "rumus_disosiasi": r"\text{KOH} \rightarrow \text{K}^+ + \text{OH}^-",
                "info_senyawa": "Basa kuat alkalis yang umumnya dipakai sebagai bahan baku pembuatan sabun cair atau baterai alkali."
            },
            "Kalsium Hidroksida (Ca(OH)2)": {
                "valensi": 2, 
                "rumus_disosiasi": r"\text{Ca(OH)}_2 \rightarrow \text{Ca}^{2+} + 2\text{OH}^-",
                "info_senyawa": "Senyawa basa kuat bervalensi dua yang sering disebut air kapur, digunakan dalam pemrosesan air minum."
            },
            "Barium Hidroksida (Ba(OH)2)": {
                "valensi": 2, 
                "rumus_disosiasi": r"\text{Ba(OH)}_2 \rightarrow \text{Ba}^{2+} + 2\text{OH}^-",
                "info_senyawa": "Basa kuat bervalensi dua yang biasa digunakan dalam titrasi asam organik di laboratorium analitik."
            },
            "Kustom / Input Manual": {
                "valensi": 1, 
                "rumus_disosiasi": r"\text{BOH} \rightarrow \text{B}^+ + \text{OH}^-",
                "info_senyawa": "Gunakan opsi ini untuk menghitung senyawa basa kuat kustom pilihan Anda sendiri."
            }
        },
        "Lemah (Weak)": {
            "Amonia (NH3 / NH4OH)": {
                "nilai": 1.8e-5, 
                "rumus_disosiasi": r"\text{NH}_3 + \text{H}_2\text{O} \rightleftharpoons \text{NH}_4^+ + \text{OH}^-",
                "info_senyawa": "Basa lemah berupa gas berbau menyengat, sangat umum digunakan pada produk pembersih kaca."
            },
            "Metilamina (CH3NH2)": {
                "nilai": 4.4e-4, 
                "rumus_disosiasi": r"\text{CH}_3\text{NH}_2 + \text{H}_2\text{O} \rightleftharpoons \text{CH}_3\text{NH}_3^+ + \text{OH}^-",
                "info_senyawa": "Turunan amonia organik lemah yang berperan penting sebagai prekusor sintesis bahan kimia obat-obatan."
            },
            "Anilina (C6H5NH2)": {
                "nilai": 4.3e-10, 
                "rumus_disosiasi": r"\text{C}_6\text{H}_5\text{NH}_2 + \text{H}_2\text{O} \rightleftharpoons \text{C}_6\text{H}_5\text{NH}_3^+ + \text{OH}^-",
                "info_senyawa": "Senyawa amin aromatik lemah yang merupakan komponen utama dalam industri pembuatan zat warna tekstil."
            },
            "Kustom / Input Manual": {
                "nilai": 1.8e-5, 
                "rumus_disosiasi": r"\text{B} + \text{H}_2\text{O} \rightleftharpoons \text{BH}^+ + \text{OH}^-",
                "info_senyawa": "Gunakan opsi ini untuk menghitung senyawa basa lemah kustom pilihan Anda sendiri."
            }
        }
    }
}

# --- DETEKSI WARNA pH DINAMIS ---
def dapatkan_warna_ph(ph_val):
    """Mengembalikan warna hex yang sesuai dengan skala indikator pH universal universal"""
    if ph_val < 3: return "#ef4444"      # Merah (Asam Kuat)
    elif ph_val < 5.5: return "#f97316"  # Oranye (Asam Lemah)
    elif ph_val < 6.8: return "#facc15"  # Kuning (Asam Sangat Lemah)
    elif abs(ph_val - 7.0) <= 0.2: return "#22c55e"  # Hijau (Netral)
    elif ph_val < 8.5: return "#06b6d4"  # Sian (Basa Sangat Lemah)
    elif ph_val < 12: return "#3b82f6"   # Biru (Basa Lemah)
    else: return "#8b5cf6"              # Ungu (Basa Kuat)

def dapatkan_gradien_ph(ph_val):
    """Menghasilkan kombinasi gradien CSS berdasarkan tingkat keasaman agar UI estetis"""
    warna = dapatkan_warna_ph(ph_val)
    return f"linear-gradient(135deg, {warna}15, {warna}25)"

# --- STYLING KUSTOM CSS ---
st.markdown("""
<style>
    /* Styling modern untuk Card visualisasi */
    .metric-card-custom {
        border-radius: 16px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.04);
        border: 1px solid rgba(0,0,0,0.06);
        margin-bottom: 15px;
        transition: transform 0.2s ease-in-out;
    }
    .metric-card-custom:hover {
        transform: translateY(-2px);
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 16px;
        padding: 8px 16px;
    }
    .title-banner {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (INPUT & RACIKAN LARUTAN) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🧪 Racik Larutan</h2>", unsafe_allow_html=True)
    st.markdown("Sesuaikan jenis senyawa dan konsentrasi kimia di bawah ini:")
    
    # 1. Pilih Kategori Sifat (Asam / Basa)
    kategori = st.selectbox(
        "Sifat Utama Larutan",
        list(DATABASE_SENYAWA.keys())
    )
    
    # 2. Pilih Tingkat Kekuatan (Kuat / Lemah)
    kekuatan = st.selectbox(
        "Kekuatan Larutan",
        list(DATABASE_SENYAWA[kategori].keys())
    )
    
    # 3. Pilih Senyawa Spesifik dari Database
    daftar_senyawa = list(DATABASE_SENYAWA[kategori][kekuatan].keys())
    senyawa_terpilih = st.selectbox(
        "Senyawa Kimia",
        daftar_senyawa
    )
    
    # Mengambil objek detail senyawa terpilih secara aman
    detail_senyawa = DATABASE_SENYAWA[kategori][kekuatan][senyawa_terpilih]
    rumus_disosiasi = detail_senyawa["rumus_disosiasi"]
    info_senyawa = detail_senyawa["info_senyawa"]
    
    st.info(f"💡 **Info:** {info_senyawa}")
    st.divider()
    
    # 4. Input Konsentrasi (Molaritas)
    molaritas = st.number_input(
        "Konsentrasi / Molaritas (M)", 
        value=0.1, 
        min_value=1e-8, 
        max_value=10.0, 
        step=0.01, 
        format="%.6f"
    )
    
    # 5. Konfigurasi Metode Perhitungan (Kelebihan Ilmiah)
    metode_hitung = st.radio(
        "Metode Perhitungan Kimia",
        ["Aproksimasi Sekolah (Standard)", "Kuadratik Presisi (Highly Accurate)"],
        help="Kuadratik Presisi menghitung derajat ionisasi secara detail tanpa pembulatan, sangat akurat pada asam/basa lemah konsentrasi sangat rendah."
    )
    
    # Inisialisasi parameter kimia dasar
    valensi = 1
    ka_kb_val = 1.8e-5
    
    # Menghubungkan parameter input ke variabel perhitungan secara otomatis tanpa KeyError
    if kekuatan == "Kuat (Strong)":
        if senyawa_terpilih == "Kustom / Input Manual":
            valensi = st.number_input(
                "Valensi (Jumlah ion H⁺ atau OH⁻)", 
                value=1, min_value=1, max_value=3, step=1
            )
        else:
            valensi = detail_senyawa["valensi"]
            st.success(f"Valensi Otomatis: {valensi}")
    else:
        # Menghindari KeyError dengan menyamakan struktur database lewat key "nilai"
        if senyawa_terpilih == "Kustom / Input Manual":
            label_konst = "Nilai Tetapan Asam (Ka)" if kategori == "Asam (Acid)" else "Nilai Tetapan Basa (Kb)"
            ka_kb_val = st.number_input(
                label_konst, 
                value=1.8e-5, 
                min_value=1e-12, 
                max_value=5.0, 
                format="%.2e"
            )
        else:
            ka_kb_val = detail_senyawa["nilai"]
            label_nama_konst = "Ka" if kategori == "Asam (Acid)" else "Kb"
            st.success(f"Nilai {label_nama_konst} Otomatis: {ka_kb_val:.2e}")

    st.divider()
    st.caption("✨ Semoga bermanfaat .")

# --- ENGINE PERHITUNGAN MATEMATIKA KIMIA ---
# Konstanta Auto-Ionisasi Air (Kw = 1.0e-14 pada suhu 25 C)
KW = 1.0e-14

def hitung_ion_terlarut(molar, kuat, kat, val, konst, metode):
    """Menghitung konsentrasi ion primer [H+] atau [OH-] dari zat terlarut"""
    if kuat == "Kuat (Strong)":
        return molar * val
    else:
        if metode == "Kuadratik Presisi (Highly Accurate)":
            # Rumus kuadratik presisi dari persamaan: [X]^2 + K*[X] - K*M = 0
            # [X] = (-K + sqrt(K^2 + 4 * K * M)) / 2
            return (-konst + math.sqrt(konst**2 + 4 * konst * molar)) / 2
        else:
            # Rumus pendekatan sekolah standar: [X] = sqrt(K * M)
            return math.sqrt(konst * molar)

# 1. Hitung konsentrasi ion mentah hasil zat terlarut
ion_primer = hitung_ion_terlarut(molaritas, kekuatan, kategori, valensi, ka_kb_val, metode_hitung)

# 2. Koreksi Ilmiah Auto-Ionisasi Air (Pencegah pH Asam bergeser > 7 saat sangat encer)
# Rumus koreksi air: [Ion]_total = (Ion_zat + sqrt(Ion_zat^2 + 4 * Kw)) / 2
ion_koreksi = (ion_primer + math.sqrt(ion_primer**2 + 4 * KW)) / 2

# 3. Konversi ke Skala Keasaman [pH & pOH]
if kategori == "Asam (Acid)":
    h_plus = ion_koreksi
    ph = -math.log10(h_plus)
    poh = 14.0 - ph
    oh_minus = 10**(-poh)
else:
    oh_minus = ion_koreksi
    poh = -math.log10(oh_minus)
    ph = 14.0 - poh
    h_plus = 10**(-ph)

# Batasi nilai akhir secara aman pada rentang ilmiah normal 0 - 14
ph = max(0.0, min(14.0, ph))
poh = max(0.0, min(14.0, poh))

# --- TAMPILAN UTAMA LAB VIRTUAL ---
st.markdown("""
<div class="title-banner">
    <h1 style="color: #1e293b; margin-bottom: 5px;">🧪 Lab Virtual: pH Asam & Basa Interaktif</h1>
    <p style="color: #64748b; font-size: 17px;">Platform simulasi, perhitungan presisi, dan analisis karakteristik senyawa kimia secara visual.</p>
</div>
""", unsafe_allow_html=True)

# Membuat 2 Halaman Kerja (Tabs)
tab1, tab2 = st.tabs(["📊 Hasil Analisis Senyawa", "💧 Simulator Pengenceran (Dilution)"])

# --- TAB 1: ANALISIS UTAMA ---
with tab1:
    # Bagian Atas: Metrik Dashboard Berwarna Dinamis
    warna_dinamis = dapatkan_warna_ph(ph)
    gradien_kartu = dapatkan_gradien_ph(ph)
    
    col_ph, col_h, col_oh = st.columns(3)
    
    with col_ph:
        st.markdown(f"""
            <div class="metric-card-custom" style="background: {gradien_kartu}; border-top: 5px solid {warna_dinamis};">
                <span style="font-size: 14px; font-weight: bold; color: #475569; letter-spacing: 0.8px;">NILAI pH</span>
                <h1 style="margin: 8px 0; font-size: 50px; color: {warna_dinamis}; font-weight: 800;">{ph:.2f}</h1>
                <span style="font-size: 11px; color: #64748b; font-weight: 500;">Tingkat Keasaman</span>
            </div>
        """, unsafe_allow_html=True)
        
    with col_h:
        st.markdown(f"""
            <div class="metric-card-custom" style="background: linear-gradient(135deg, #eff6ff, #dbeafe); border-top: 5px solid #3b82f6;">
                <span style="font-size: 14px; font-weight: bold; color: #1e40af; letter-spacing: 0.8px;">KONSENTRASI [H⁺]</span>
                <h1 style="margin: 8px 0; font-size: 34px; color: #1d4ed8; font-weight: bold; padding: 6px 0;">{h_plus:.2e} <span style="font-size: 18px;">M</span></h1>
                <span style="font-size: 11px; color: #1e40af; font-weight: 500;">Ion Hidronium / H⁺ Total</span>
            </div>
        """, unsafe_allow_html=True)
        
    with col_oh:
        st.markdown(f"""
            <div class="metric-card-custom" style="background: linear-gradient(135deg, #faf5ff, #f3e8ff); border-top: 5px solid #a855f7;">
                <span style="font-size: 14px; font-weight: bold; color: #6b21a8; letter-spacing: 0.8px;">KONSENTRASI [OH⁻]</span>
                <h1 style="margin: 8px 0; font-size: 34px; color: #7e22ce; font-weight: bold; padding: 6px 0;">{oh_minus:.2e} <span style="font-size: 18px;">M</span></h1>
                <span style="font-size: 11px; color: #6b21a8; font-weight: 500;">Ion Hidroksida / OH⁻ Total</span>
            </div>
        """, unsafe_allow_html=True)

    # Visualisasi Skala Gradasi pH Universal
    st.markdown("### 🌈 Indikator Visual Skala pH Universal")
    posisi_persen = (ph / 14.0) * 100
    
    st.markdown(
        f"""
        <div style="position: relative; width: 100%; height: 38px; border-radius: 19px; 
            background: linear-gradient(to right, 
                #ef4444 0%, #f97316 20%, #eab308 40%, #22c55e 50%, #06b6d4 60%, #3b82f6 80%, #8b5cf6 100%);
            margin-top: 15px; margin-bottom: 25px; box-shadow: inset 0 3px 6px rgba(0,0,0,0.15);">
            <!-- Pin Penunjuk Posisi pH Dinamis -->
            <div style="position: absolute; left: calc({posisi_persen}% - 14px); top: -8px; 
                width: 28px; height: 54px; background-color: #ffffff; border: 4px solid {warna_dinamis}; 
                border-radius: 14px; box-shadow: 0 4px 10px rgba(0,0,0,0.25); transition: left 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 10px; font-weight: 900; color: #1e293b;">{ph:.1f}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Detail Penjelasan Ilmiah & Karakteristik Larutan
    st.markdown("### 📑 Detail Karakteristik Kimia")
    col_info, col_rumus = st.columns(2)
    
    with col_info:
        # Menentukan ulasan berdasarkan tingkat pH
        if ph < 3.0:
            tipe_sifat = "error"
            teks_sifat = "🔥 **Asam Kuat Ekstrem:** Memiliki tingkat keasaman yang sangat tinggi. Sangat korosif terhadap logam, dapat menyebabkan luka bakar parah pada kulit, serta terionisasi sempurna dalam air."
            rek_indikator = "Metil Merah, Timol Biru, atau Metil Jingga"
        elif ph < 7.0:
            tipe_sifat = "warning"
            teks_sifat = "🍋 **Asam Lemah:** Tingkat keasaman sedang atau ringan. Umum dijumpai pada bahan organik konsumsi sehari-hari seperti sari buah sitrus dan cuka dapur."
            rek_indikator = "Bromtimol Biru atau Metil Merah"
        elif abs(ph - 7.0) < 0.05:
            tipe_sifat = "success"
            teks_sifat = "💧 **Netral Seimbang:** Nilai keasaman seimbang sempurna. Jumlah molekul ion $[H^+]$ setara dengan ion $[OH^-]$ (seperti air murni bebas mineral pada suhu kamar)."
            rek_indikator = "Bromtimol Biru (BTB) atau Kertas Indikator Universal"
        elif ph < 12.0:
            tipe_sifat = "info"
            teks_sifat = "🧼 **Basa Lemah:** Bersifat alkali ringan. Terasa licin saat terkena kulit dan umum dimanfaatkan sebagai komponen pembersih sabun cair atau pembersih kaca amonia."
            rek_indikator = "Fenolftalein (PP) atau Alizarin Kuning"
        else:
            tipe_sifat = "error"
            teks_sifat = "☠️ **Basa Kuat Ekstrem:** Sangat kaustik dan reaktif. Merusak protein kulit secara langsung melalui proses saponifikasi lemak tubuh (membuat kulit hancur dan sangat licin)."
            rek_indikator = "Fenolftalein (PP)"
            
        st.markdown(f"**Identitas Senyawa:** {senyawa_terpilih} ({kekuatan})")
        if tipe_sifat == "error":
            st.error(teks_sifat)
        elif tipe_sifat == "warning":
            st.warning(teks_sifat)
        elif tipe_sifat == "success":
            st.success(teks_sifat)
        else:
            st.info(teks_sifat)
            
        st.info(f"🔬 **Rekomendasi Indikator Lab:** {rek_indikator}")
        
        # Edukasi derajat ionisasi alpha jika menggunakan metode lemah
        if kekuatan == "Lemah (Weak)":
            alpha = h_plus / molaritas if kategori == "Asam (Acid)" else oh_minus / molaritas
            st.metric("Derajat Ionisasi (α)", f"{alpha*100:.3f} %", help="Persentase jumlah molekul asam/basa yang terionisasi menjadi ion bebas di dalam air.")

    # Bagian Kanan: Penulisan Rumus LaTeX Ilmiah
    with col_rumus:
        st.markdown("**Persamaan Reaksi Ionisasi (Disosiasi):**")
        st.latex(rumus_disosiasi)
        
        st.markdown(f"**Langkah Perhitungan ({metode_hitung}):**")
        
        # Menuliskan visualisasi rumus matematika langkah-langkahnya
        if kekuatan == "Kuat (Strong)":
            if kategori == "Asam (Acid)":
                st.latex(r"[H^+]_{zat} = M \times \text{Valensi}")
                st.latex(rf"[H^+]_{{zat}} = {molaritas:g} \times {valensi} = {ion_primer:.2e} \text{{ M}}")
            else:
                st.latex(r"[OH^-]_{zat} = M \times \text{Valensi}")
                st.latex(rf"[OH^-]_{{zat}} = {molaritas:g} \times {valensi} = {ion_primer:.2e} \text{{ M}}")
        else:
            # Reaksi Lemah
            if metode_hitung == "Kuadratik Presisi (Highly Accurate)":
                st.latex(r"[Ion]_{zat} = \frac{-K + \sqrt{K^2 + 4 \cdot K \cdot M}}{2}")
                label_k = "K_a" if kategori == "Asam (Acid)" else "K_b"
                st.latex(rf"[Ion]_{{zat}} = \frac{{-{ka_kb_val:.1e} + \sqrt{{({ka_kb_val:.1e})^2 + 4 \cdot {ka_kb_val:.1e} \cdot {molaritas:g}}}}}{{2}} = {ion_primer:.2e} \text{{ M}}")
            else:
                # Aproksimasi Sekolah biasa
                label_k = "K_a" if kategori == "Asam (Acid)" else "K_b"
                st.latex(rf"[Ion]_{{zat}} = \sqrt{{{label_k} \times M}}")
                st.latex(rf"[Ion]_{{zat}} = \sqrt{{{ka_kb_val:.2e} \times {molaritas:g}}} = {ion_primer:.2e} \text{{ M}}")
                
        # Menampilkan koreksi air jika konsentrasi sangat ekstrem encer (< 1e-6 M)
        if ion_primer < 1e-6:
            st.caption("⚠️ *Mengaktifkan rumus koreksi auto-ionisasi air ($K_w = 10^{-14}$) karena larutan sangat encer.*")
            st.latex(r"[Ion]_{total} = \frac{[Ion]_{zat} + \sqrt{[Ion]_{zat}^2 + 4 \cdot K_w}}{2}")
            st.latex(rf"[Ion]_{{total}} = {ion_koreksi:.2e} \text{{ M}}")
            
        if kategori == "Asam (Acid)":
            st.latex(rf"\text{{pH}} = -\log_{{10}}([H^+]) = -\log_{{10}}({h_plus:.2e}) = {ph:.2f}")
        else:
            st.latex(rf"\text{{pOH}} = -\log_{{10}}([OH^-]) = -\log_{{10}}({oh_minus:.2e}) = {poh:.2f}")
            st.latex(rf"\text{{pH}} = 14 - \text{{pOH}} = 14 - {poh:.2f} = {ph:.2f}")

# --- TAB 2: SIMULATOR PENGENCERAN ---
with tab2:
    st.markdown("### ⚗️ Simulasi Pengenceran Larutan (Dilution)")
    st.markdown("Prediksi perubahan tingkat keasaman secara instan saat ditambahkan air pelarut ($V_{air}$).")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        v1 = st.number_input("Volume Awal Larutan ($V_1$ dalam mL)", value=100.0, min_value=0.1, step=10.0)
    with col_v2:
        v_air = st.number_input("Volume Air Bersih yang Ditambahkan (mL)", value=900.0, min_value=0.0, step=100.0)
        
    # Perhitungan hukum pengenceran M1 * V1 = M2 * V2
    v2 = v1 + v_air
    molaritas_baru = molaritas * (v1 / v2)
    
    # Menghitung kembali pH pasca pengenceran
    ion_primer_baru = hitung_ion_terlarut(molaritas_baru, kekuatan, kategori, valensi, ka_kb_val, metode_hitung)
    ion_koreksi_baru = (ion_primer_baru + math.sqrt(ion_primer_baru**2 + 4 * KW)) / 2
    
    if kategori == "Asam (Acid)":
        h_plus_baru = ion_koreksi_baru
        ph_baru = -math.log10(h_plus_baru)
    else:
        oh_minus_baru = ion_koreksi_baru
        poh_baru = -math.log10(oh_minus_baru)
        ph_baru = 14.0 - poh_baru
        
    ph_baru = max(0.0, min(14.0, ph_baru))
    selisih_ph = ph_baru - ph
    
    st.divider()
    
    # Tampilan Dashboard Hasil Pengenceran
    mc1, mc2, mc3 = st.columns(3)
    
    mc1.metric(
        label="Volume Total Akhir (V2)", 
        value=f"{v2:g} mL",
        delta=f"+{v_air:g} mL Air"
    )
    mc2.metric(
        label="Molaritas Baru (M2)", 
        value=f"{molaritas_baru:.2e} M",
        delta=f"-{(molaritas - molaritas_baru):.2e} M"
    )
    
    # Menentukan status delta pergeseran arah pH
    simbol_delta = f"{selisih_ph:+.2f} pH"
    mc3.metric(
        label="pH Baru Setelah Diencerkan", 
        value=f"{ph_baru:.2f}", 
        delta=simbol_delta,
        delta_color="normal" if abs(selisih_ph) > 0.005 else "off"
    )
    
    # Penjelasan edukasi prinsip pengenceran
    st.info(
        "💡 **Prinsip Pengenceran Fisik:** "
        "Penambahan pelarut air murni akan menurunkan konsentrasi ion total di dalam cairan. "
        "Hal ini menyebabkan pH asam bergeser **naik mendekati angka 7** (menurun kadar asamnya), "
        "sedangkan pH senyawa basa akan bergeser **turun mendekati angka 7** (menurun kadar basanya). "
        "Melalui fitur koreksi air kami, pH tidak akan pernah melewati batas netral 7.0 berapa pun jumlah air pengencer yang dimasukkan."
    )