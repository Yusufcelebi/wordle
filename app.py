import streamlit as st
import random

# ── Sayfa ayarları ─────────────────────────────────────────────────────────────
st.set_page_config(page_title="Türkçe Wordle", page_icon="🟩", layout="centered")

# ── Stil ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; }

.baslik {
    text-align: center;
    font-size: 2.2rem;
    font-weight: 900;
    letter-spacing: 8px;
    margin-bottom: 0.2rem;
}

.altbaslik {
    text-align: center;
    color: #888;
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
    letter-spacing: 2px;
}

.izgara {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    margin-bottom: 1.5rem;
}

.satir {
    display: flex;
    gap: 6px;
}

.kutu {
    width: 56px;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.6rem;
    font-weight: 700;
    border-radius: 6px;
    border: 2px solid #d3d6da;
    color: white;
    text-transform: uppercase;
}

.kutu.bos  { background: #fff; color: #333; border: 2px solid #d3d6da; }
.kutu.dolu { background: #fff; color: #333; border: 2px solid #888; }
.kutu.dogru   { background: #538d4e; border-color: #538d4e; }
.kutu.yakin   { background: #b59f3b; border-color: #b59f3b; }
.kutu.yanlis  { background: #3a3a3c; border-color: #3a3a3c; }

.klavye {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    margin-bottom: 1rem;
}

.klavye-satir { display: flex; gap: 5px; }

.tus {
    height: 56px;
    min-width: 36px;
    padding: 0 8px;
    border-radius: 6px;
    border: none;
    font-family: 'Outfit', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    background: #818384;
    color: white;
}

.tus.dogru  { background: #538d4e; }
.tus.yakin  { background: #b59f3b; }
.tus.yanlis { background: #3a3a3c; }

.mesaj {
    text-align: center;
    font-size: 1.1rem;
    font-weight: 700;
    padding: 0.5rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.mesaj.kazandi { background: #538d4e22; color: #538d4e; }
.mesaj.kaybetti { background: #e4333322; color: #e43333; }

stButton > button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ── Kelime listesi ─────────────────────────────────────────────────────────────
KELIMELER = [
    "kalem", "araba", "elmas", "burun", "şeker", "kitap", "bebek", "dalga",
    "korku", "melek", "sabah", "tahta", "yüzük", "bahçe", "limon", "büyük",
    "havlu", "çanta", "aslan", "bulut", "kapak", "fener", "gelin", "küçük",
    "müzik", "perde", "resim", "sokak", "tarak", "uzman", "vakit", "yılan",
    "zemin", "balık", "ceket", "dilek", "ekmek", "hayat", "lamba", "marul",
    "nehir", "pilav", "selam", "tatlı", "yunus", "cevap", "doğru", "fidan",
    "görev", "haber", "koyun", "maden", "neden", "omlet", "tabla", "yazar",
    "çoban", "derin", "erken", "gazoz", "insan", "masal", "orman", "pınar",
    "radyo", "şahin", "taraf", "yufka", "aktif", "çırak", "döngü", "fıkra",
    "jilet", "kakao", "lodos", "müzik", "rozet", "sunum", "tepsi", "yanık",
    "ahşap", "biber", "cadde", "duman", "hayal", "irmak", "pasta", "rüzgar",
    "simit", "tablo", "vatan", "şafak", "köpek", "güneş", "çorba", "türkü",
    "deniz", "kanat", "dünya", "barış", "çelik", "demir", "fiyat", "güzel",
    "hızlı", "kural", "metre", "noter", "pamuk", "robot", "sanat", "tünel",
    "vagon", "yetim", "abone", "damar", "eklem", "hamur", "model", "örgüt",
    "pilot", "reçel", "testi", "alarm", "bozuk", "devir", "etken", "fırça",
    "halat", "kabuk", "levha", "polis", "vites", "yoğun", "ceviz", "davar",
    "göbek", "hamsi", "ideal", "lüfer", "minik", "nadir", "papaz", "salça",
    "beyin", "çimen", "dolap", "fincan", "güvey", "irade", "kazan", "miras",
    "nakış", "peşin", "vergi", "zorba", "akrep", "beton", "düzey", "engin",
    "girdi", "hüzün", "imece", "kıdem", "mezar", "nişan", "tepki", "uyarı",
    "viraj", "yenge", "alçak", "coşku", "dümen", "erkek", "gübre", "kavak",
    "liman", "müdür", "petek", "şükür", "tavan", "vezir", "bilgi", "deste",
    "evren", "fizik", "hisar", "istek", "kilim", "layla", "niyet", "pazar",
    "roket", "silah", "vurgu", "yarım", "zümre", "moral", "nasip", "öğlen",
    "roman", "uygun", "yiğit", "zarif", "filiz", "kısık", "ölçüm", "paket",
    "şişir", "ayran", "beden", "çeşit", "farma", "gizem", "hamle", "ileri",
    "kader", "masaj", "nefes", "özgür", "teyze", "yarış", "aktar", "çiğne",
    "dolma", "etnik", "görüş", "makam", "nazar", "parça", "silme", "yatır",
    "bisik", "çorap", "ekran", "gömme", "hilal", "maket", "palet", "rakam",
    "şenli", "vizit", "yakıt", "zebra", "boyut", "firma", "merak", "nezih",
    "armut", "çeşme", "dönüş", "emsal", "hanım", "özlem", "pembe", "uçucu",
    "aksak", "çınar", "tenha", "yazgı", "altın", "beyaz", "düzin", "göçer",
    "leğen", "örtük", "ambaj", "çırpı", "döşek", "etraf", "hacim", "ikili",
    "kapan", "şöyle", "yaylı", "gözde", "hafız", "imkân", "kapat", "mezra",
    "örtme", "payla", "rızık", "şekil", "zirai", "çiçek", "devam", "gözüm",
    "hamit", "ilave", "misli", "nazım", "penbe", "zımba", "döviz", "emzik",
    "hızlı", "niçin", "öğret", "zıpla", "birle", "dürüm", "erkân", "hamle",
    "lavta", "örnek", "uğraş", "yarık", "alevi", "çömle", "güçlü", "hadis",
    "lağım", "namus", "ölçek", "ritim", "temiz", "çuval", "diken", "hapis",
    "lakin", "mesaj", "öteki", "şimdi", "yazgı", "deney", "güven", "rütbe",
    "yarın", "banka", "çevre", "fazla", "gömüt", "müdür", "nihai", "pembe",
    "silah", "tahıl", "vokal", "yakıt",
]
KELIMELER = sorted(set(w for w in KELIMELER if len(w) == 5))

MAX_DENEME = 6

# ── Yardımcı fonksiyonlar ──────────────────────────────────────────────────────
def normalize(s):
    return s.lower().replace("İ","i").replace("I","ı")

def degerlendir(tahmin, gizli):
    sonuc = ["yanlis"] * 5
    gizli_arr = list(gizli)
    kullanildi = [False] * 5
    for i in range(5):
        if tahmin[i] == gizli_arr[i]:
            sonuc[i] = "dogru"
            kullanildi[i] = True
    for i in range(5):
        if sonuc[i] == "dogru":
            continue
        for j in range(5):
            if not kullanildi[j] and tahmin[i] == gizli_arr[j]:
                sonuc[i] = "yakin"
                kullanildi[j] = True
                break
    return sonuc

# ── Session state başlat ───────────────────────────────────────────────────────
if "gizli" not in st.session_state:
    st.session_state.gizli = normalize(random.choice(KELIMELER))
if "tahminler" not in st.session_state:
    st.session_state.tahminler = []
if "sonuclar" not in st.session_state:
    st.session_state.sonuclar = []
if "klavye" not in st.session_state:
    st.session_state.klavye = {}
if "oyun_bitti" not in st.session_state:
    st.session_state.oyun_bitti = False
if "kazandi" not in st.session_state:
    st.session_state.kazandi = False
if "hata" not in st.session_state:
    st.session_state.hata = ""

# ── Başlık ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="baslik">🟩 WORDLE</div>', unsafe_allow_html=True)
st.markdown('<div class="altbaslik">TÜRKÇE · 5 HARFLİ KELİMEYİ BUL</div>', unsafe_allow_html=True)

# ── Izgara ─────────────────────────────────────────────────────────────────────
izgara_html = '<div class="izgara">'
for r in range(MAX_DENEME):
    izgara_html += '<div class="satir">'
    if r < len(st.session_state.tahminler):
        tahmin = st.session_state.tahminler[r]
        sonuc  = st.session_state.sonuclar[r]
        for i, harf in enumerate(tahmin):
            izgara_html += f'<div class="kutu {sonuc[i]}">{harf.upper()}</div>'
    else:
        for _ in range(5):
            izgara_html += '<div class="kutu bos"> </div>'
    izgara_html += '</div>'
izgara_html += '</div>'
st.markdown(izgara_html, unsafe_allow_html=True)

# ── Mesaj ──────────────────────────────────────────────────────────────────────
if st.session_state.hata:
    st.warning(st.session_state.hata)

if st.session_state.oyun_bitti:
    if st.session_state.kazandi:
        mesajlar = {1:"Efsane! 🏆", 2:"Muhteşem! 🎉", 3:"Harika! 🌟",
                    4:"İyi iş! 👏", 5:"Neredeyse! 😅", 6:"Tam son anda! 😤"}
        st.success(mesajlar[len(st.session_state.tahminler)])
    else:
        st.error(f"Kaybettin! Kelime: **{st.session_state.gizli.upper()}**")

# ── Giriş ──────────────────────────────────────────────────────────────────────
if not st.session_state.oyun_bitti:
    col1, col2 = st.columns([4, 1])
    with col1:
        tahmin_girdi = st.text_input(
            "Tahminin:",
            max_chars=5,
            placeholder="5 harf yaz...",
            label_visibility="collapsed",
            key="girdi"
        )
    with col2:
        gonder = st.button("Gönder", use_container_width=True)

    if gonder and tahmin_girdi:
        tahmin = normalize(tahmin_girdi.strip())
        if len(tahmin) != 5:
            st.session_state.hata = "⚠️ Tam olarak 5 harf gir!"
            st.rerun()
        elif not tahmin.isalpha():
            st.session_state.hata = "⚠️ Sadece harf kullan!"
            st.rerun()
        else:
            st.session_state.hata = ""
            sonuc = degerlendir(tahmin, st.session_state.gizli)
            st.session_state.tahminler.append(tahmin)
            st.session_state.sonuclar.append(sonuc)

            oncelik = {"dogru": 3, "yakin": 2, "yanlis": 1}
            for i, harf in enumerate(tahmin):
                mevcut = st.session_state.klavye.get(harf)
                if mevcut is None or oncelik[sonuc[i]] > oncelik.get(mevcut, 0):
                    st.session_state.klavye[harf] = sonuc[i]

            if all(s == "dogru" for s in sonuc):
                st.session_state.oyun_bitti = True
                st.session_state.kazandi = True
            elif len(st.session_state.tahminler) >= MAX_DENEME:
                st.session_state.oyun_bitti = True
                st.session_state.kazandi = False
            st.rerun()

# ── Klavye ─────────────────────────────────────────────────────────────────────
KB = [
    ["e","r","t","y","u","ı","o","p","ğ","ü"],
    ["a","s","d","f","g","h","j","k","l","ş","i"],
    ["z","x","c","v","b","n","m","ö","ç"],
]

klavye_html = '<div class="klavye">'
for satir in KB:
    klavye_html += '<div class="klavye-satir">'
    for harf in satir:
        durum = st.session_state.klavye.get(harf, "")
        klavye_html += f'<div class="tus {durum}">{harf.upper()}</div>'
    klavye_html += '</div>'
klavye_html += '</div>'
st.markdown(klavye_html, unsafe_allow_html=True)

# ── Yeni oyun ──────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔄 Yeni Oyun", use_container_width=True):
    st.session_state.gizli     = normalize(random.choice(KELIMELER))
    st.session_state.tahminler = []
    st.session_state.sonuclar  = []
    st.session_state.klavye    = {}
    st.session_state.oyun_bitti = False
    st.session_state.kazandi    = False
    st.session_state.hata       = ""
    st.rerun()

st.markdown(f"<p style='text-align:center;color:#aaa;font-size:0.75rem;margin-top:1rem'>{len(KELIMELER)} kelime · Türkçe Wordle</p>", unsafe_allow_html=True)
