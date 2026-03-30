import streamlit as st
import random

st.set_page_config(page_title="Büyülü Wordle", page_icon="🧙", layout="centered")

# ── Stil ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&family=Outfit:wght@400;700;900&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif; background: #0f0f1a; color: #e8e8e8; }

.baslik {
    text-align: center;
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: 6px;
    color: #e8e8e8;
    margin-bottom: 0.1rem;
}
.altbaslik {
    text-align: center;
    color: #666;
    font-size: 0.75rem;
    letter-spacing: 3px;
    margin-bottom: 1rem;
}
.xp-bar {
    text-align: center;
    font-size: 1rem;
    font-weight: 700;
    color: #ffd700;
    margin-bottom: 1rem;
    letter-spacing: 2px;
}
.izgara {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 5px;
    margin-bottom: 1.2rem;
}
.satir { display: flex; gap: 5px; }
.kutu {
    width: 54px; height: 54px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 700;
    border-radius: 4px;
    border: 2px solid #333;
    color: #e8e8e8;
    text-transform: uppercase;
    background: #1a1a2e;
}
.kutu.dogru  { background: #538d4e; border-color: #538d4e; }
.kutu.yakin  { background: #b59f3b; border-color: #b59f3b; }
.kutu.yanlis { background: #2a2a2a; border-color: #3a3a3a; color: #555; }

.klavye { display: flex; flex-direction: column; align-items: center; gap: 5px; margin-bottom: 1rem; }
.klavye-satir { display: flex; gap: 4px; }
.tus {
    height: 48px; min-width: 33px; padding: 0 6px;
    border-radius: 4px; border: none;
    font-family: 'Outfit', sans-serif;
    font-size: 0.8rem; font-weight: 700;
    cursor: pointer;
    background: #2a2a3e; color: #e8e8e8;
}
.tus.dogru  { background: #538d4e; }
.tus.yakin  { background: #b59f3b; }
.tus.yanlis { background: #1a1a1a; color: #444; }

/* Amca pikseli */
.amca-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 0.5rem;
}
.amca-isim {
    font-size: 0.7rem;
    letter-spacing: 2px;
    color: #888;
    margin-top: 4px;
}
.amca-laf {
    font-size: 0.85rem;
    font-style: italic;
    color: #bbb;
    text-align: center;
    min-height: 1.4rem;
    margin-bottom: 0.5rem;
    padding: 0 1rem;
}
.teklif-kutu {
    background: #1a1020;
    border: 1px solid #7c3aed;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    text-align: center;
    margin-bottom: 0.8rem;
}
.teklif-baslik { color: #a855f7; font-size: 0.8rem; letter-spacing: 2px; font-weight: 700; margin-bottom: 0.3rem; }
.teklif-metin  { color: #ddd; font-size: 0.9rem; }
.teklif-ucret  { color: #f59e0b; font-size: 0.75rem; margin-top: 0.3rem; }
</style>
""", unsafe_allow_html=True)

# ── Kelimeler ──────────────────────────────────────────────────────────────────
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
    "jilet", "kakao", "lodos", "rozet", "sunum", "tepsi", "yanık", "ahşap",
    "biber", "cadde", "duman", "hayal", "irmak", "pasta", "rüzgar", "simit",
    "vatan", "şafak", "köpek", "güneş", "çorba", "türkü", "deniz", "kanat",
    "dünya", "barış", "çelik", "demir", "fiyat", "güzel", "hızlı", "kural",
    "metre", "noter", "pamuk", "robot", "sanat", "tünel", "vagon", "yetim",
    "abone", "damar", "eklem", "hamur", "model", "örgüt", "pilot", "reçel",
    "alarm", "bozuk", "devir", "etken", "fırça", "halat", "kabuk", "levha",
    "polis", "vites", "yoğun", "ceviz", "davar", "göbek", "hamsi", "ideal",
    "lüfer", "minik", "nadir", "papaz", "salça", "beyin", "çimen", "dolap",
    "fincan", "güvey", "irade", "kazan", "miras", "nakış", "peşin", "vergi",
    "zorba", "akrep", "beton", "düzey", "engin", "girdi", "hüzün", "kıdem",
    "mezar", "nişan", "tepki", "uyarı", "viraj", "yenge", "alçak", "coşku",
    "dümen", "erkek", "gübre", "kavak", "liman", "müdür", "petek", "şükür",
    "tavan", "vezir", "bilgi", "deste", "evren", "fizik", "hisar", "istek",
    "kilim", "niyet", "pazar", "roket", "silah", "vurgu", "yarım", "zümre",
    "moral", "nasip", "öğlen", "roman", "yiğit", "zarif", "filiz", "kısık",
    "ölçüm", "paket", "ayran", "beden", "çeşit", "farma", "gizem", "hamle",
    "ileri", "kader", "masaj", "nefes", "özgür", "teyze", "yarış", "aktar",
    "çiğne", "dolma", "etnik", "görüş", "makam", "nazar", "parça", "silme",
    "bisik", "çorap", "ekran", "gömme", "hilal", "maket", "palet", "rakam",
    "şenli", "vizit", "yakıt", "zebra", "boyut", "firma", "merak", "nezih",
    "armut", "çeşme", "dönüş", "emsal", "hanım", "özlem", "pembe", "uçucu",
    "aksak", "çınar", "tenha", "yazgı", "altın", "beyaz", "düzin", "göçer",
    "leğen", "örtük", "ambaj", "çırpı", "döşek", "etraf", "hacim", "ikili",
    "kapan", "şöyle", "yaylı", "gözde", "hafız", "imkân", "kapat", "mezra",
    "örtme", "payla", "rızık", "şekil", "zirai", "çiçek", "devam", "gözüm",
    "hamit", "ilave", "misli", "nazım", "penbe", "zımba", "döviz", "emzik",
    "niçin", "öğret", "zıpla", "birle", "dürüm", "erkân", "hamle", "lavta",
    "örnek", "uğraş", "yarık", "alevi", "çömle", "güçlü", "hadis", "lağım",
    "namus", "ölçek", "ritim", "temiz", "çuval", "diken", "hapis", "lakin",
    "mesaj", "öteki", "şimdi", "yazgı", "deney", "güven", "rütbe", "yarın",
    "banka", "çevre", "fazla", "gömüt", "müdür", "nihai", "pembe", "silah",
]
KELIMELER = sorted(set(w for w in KELIMELER if len(w) == 5))

MAX_DENEME = 6

# ── Amca lafları ───────────────────────────────────────────────────────────────
LAFLAR_NORMAL = [
    "Hmmm… Farklı.",
    "Bak ya ne kadar çömezsin sen.",
    "Azıcık sözlük aç.",
    "Devam et bakalım, belki şansın yaver gider.",
    "İlginç... ama yanlış.",
    "Yıllar önce bir çömez vardı, senden iyiydi.",
    "Bu tahmini yaparken ne düşündün acaba?",
    "Eh... en azından denedin.",
    "Sessizce izliyorum. Üzüntüyle.",
    "Büyücülüğü bırak, başka bir şey dene.",
]
LAFLAR_SON_TAHMIN = [
    "Son şansın. Heyecanlanıyorum... ama senin için değil.",
    "Bu son tahmin. Mucize bekliyorum ama umut az.",
    "Son hakkın. Büyü yap.",
]

# ── Piksel art amca ────────────────────────────────────────────────────────────
def amca_svg(renk: str = "normal") -> str:
    renkler = {
        "normal":  {"govde": "#aaaaaa", "cüppe": "#666688", "sakal": "#dddddd", "goz": "#222222", "parlak": "#cccccc"},
        "kahkaha": {"govde": "#44bbaa", "cüppe": "#1a8877", "sakal": "#aaffee", "goz": "#003322", "parlak": "#00ffcc"},
        "kopurme": {"govde": "#cc4444", "cüppe": "#881111", "sakal": "#ffaaaa", "goz": "#330000", "parlak": "#ff6666"},
        "teklif":  {"govde": "#9955cc", "cüppe": "#551188", "sakal": "#ddaaff", "goz": "#220033", "parlak": "#cc88ff"},
        "altin":   {"govde": "#ccaa00", "cüppe": "#886600", "sakal": "#ffee88", "goz": "#332200", "parlak": "#ffd700"},
    }
    r = renkler.get(renk, renkler["normal"])
    # Piksel grid: 16x20 amca
    piksel = [
        "....XXXXXXXX....",  # şapka
        "...XXXXXXXXXX...",
        "..XXXXXXXXXXXX..",
        "....XXXXXXXX....",  # yüz üst
        "...X........X...",
        "...X..O..O..X...",  # gözler
        "...X........X...",
        "...XXXXXXXXXX...",  # sakal başlangıç
        "..XXXXXXXXXXXX..",
        ".XXXXXXXXXXXXXX.",  # sakal geniş
        "....XXXXXXXX....",  # boyun
        "...XXXXXXXXXX...",  # omuz
        "..XXXXXXXXXXXX..",  # gövde
        "..XXXXXXXXXXXX..",
        "..XXXXXXXXXXXX..",
        "...X........X...",  # bel
        "..XX........XX..",  # etek
        ".XXX........XXX.",
        "XXXX........XXXX",
        "XX............XX",  # ayaklar
    ]
    piksel_boyut = 5
    svg_genislik = 16 * piksel_boyut
    svg_yukseklik = 20 * piksel_boyut

    svg = f'<svg width="{svg_genislik}" height="{svg_yukseklik}" xmlns="http://www.w3.org/2000/svg" style="image-rendering:pixelated">'

    for y, satir in enumerate(piksel):
        for x, karakter in enumerate(satir):
            if karakter == "X":
                # Şapka (0-3) vs sakal (7-9) vs gövde
                if y <= 3:
                    renk_kullan = r["cüppe"]
                elif y <= 6:
                    renk_kullan = r["govde"]
                elif y <= 9:
                    renk_kullan = r["sakal"]
                else:
                    renk_kullan = r["cüppe"]
                svg += f'<rect x="{x*piksel_boyut}" y="{y*piksel_boyut}" width="{piksel_boyut}" height="{piksel_boyut}" fill="{renk_kullan}"/>'
            elif karakter == "O":
                svg += f'<rect x="{x*piksel_boyut}" y="{y*piksel_boyut}" width="{piksel_boyut}" height="{piksel_boyut}" fill="{r["goz"]}"/>'

    # Parlak nokta (gözün üstü)
    svg += f'<rect x="{5*piksel_boyut}" y="{4*piksel_boyut}" width="2" height="2" fill="{r["parlak"]}"/>'
    svg += "</svg>"
    return svg

# ── XP hesaplama ───────────────────────────────────────────────────────────────
def xp_hesapla(tahmin, gizli, sonuc, onceki_puan_alan):
    """
    Puan alma kuralları:
    - Sarı (yakin): +0.25 — ama daha önce aynı harf aynı konumda sarı veya yeşil puan almışsa sıfır
    - Yeşil (dogru): +0.50 — ama daha önce aynı harf aynı konumda yeşil puan almışsa sıfır
    - Sarı→Yeşil: toplamda 0.75 (0.25 + 0.50)
    - Yeşil→Sarı: 0 (yeşil zaten en yüksek, geri gidince puan yok)
    """
    kazan = 1.0
    yeni_puan_alan = set()

    for i, (harf, durum) in enumerate(zip(tahmin, sonuc)):
        anahtar_yesil = (harf, i, "dogru")
        anahtar_sari  = (harf, i, "yakin")

        if durum == "dogru":
            # Daha önce bu konumda yeşil puan almamışsa +0.50
            if anahtar_yesil not in onceki_puan_alan:
                kazan += 0.5
                yeni_puan_alan.add(anahtar_yesil)
        elif durum == "yakin":
            # Daha önce bu konumda sarı VEYA yeşil puan almamışsa +0.25
            # (yeşil→sarı durumunda hiç puan yok)
            if anahtar_sari not in onceki_puan_alan and anahtar_yesil not in onceki_puan_alan:
                kazan += 0.25
                yeni_puan_alan.add(anahtar_sari)

    return kazan, yeni_puan_alan

def dogru_tahmin_bonusu(deneme_no):
    # 1. tahminde +5, 2. tahminde +4 ... 6. tahminde +0
    return max(0, 6 - deneme_no)

# ── Session state ──────────────────────────────────────────────────────────────
def yeni_oyun():
    st.session_state.gizli        = random.choice(KELIMELER)
    st.session_state.tahminler    = []
    st.session_state.sonuclar     = []
    st.session_state.klavye       = {}
    st.session_state.oyun_bitti   = False
    st.session_state.kazandi      = False
    st.session_state.hata         = ""
    st.session_state.amca_laf     = ""
    st.session_state.amca_renk    = "normal"
    st.session_state.teklif       = None   # {"harf": "a", "yer": 2, "blof": True/False}
    st.session_state.teklif_kabul = False
    st.session_state.teklif_goster= False
    st.session_state.puan_alanlar = set()  # (harf, konum, renk)

if "gizli" not in st.session_state:
    st.session_state.xp = 0.0
    yeni_oyun()

# ── Başlık ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="baslik">🧙 BÜYÜLÜ WORDLE</div>', unsafe_allow_html=True)
st.markdown('<div class="altbaslik">5 HARFLİ KELİMEYİ BUL</div>', unsafe_allow_html=True)
st.markdown(f'<div class="xp-bar">✨ XP: {st.session_state.xp:.2f}</div>', unsafe_allow_html=True)

# ── Amca göster ────────────────────────────────────────────────────────────────
xp = st.session_state.xp
amca_gorunsun = xp >= 10

if amca_gorunsun:
    col_bos, col_amca, col_bos2 = st.columns([2, 1, 2])
    with col_amca:
        svg = amca_svg(st.session_state.amca_renk)
        st.markdown(f'<div class="amca-wrap">{svg}<div class="amca-isim">BÜYÜCÜ</div></div>', unsafe_allow_html=True)

    if st.session_state.amca_laf:
        st.markdown(f'<div class="amca-laf">"{st.session_state.amca_laf}"</div>', unsafe_allow_html=True)

    # Teklif kutusu
    if st.session_state.teklif_goster and st.session_state.teklif and not st.session_state.teklif_kabul and not st.session_state.oyun_bitti:
        t = st.session_state.teklif
        ucret = len(st.session_state.tahminler) + 1
        st.markdown(f"""
        <div class="teklif-kutu">
            <div class="teklif-baslik">🔮 TEKLİF</div>
            <div class="teklif-metin">{t['mesaj']}</div>
            <div class="teklif-ucret">Bedel: {ucret} XP</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Kabul Et", use_container_width=True):
                if st.session_state.xp >= ucret:
                    st.session_state.xp -= ucret
                    st.session_state.teklif_kabul = True
                    st.session_state.teklif_goster = False
                    # Blöf mü?
                    if t["blof"]:
                        st.session_state.amca_renk = "normal"  # kahkahayı kullanınca göstereceğiz
                        st.session_state.amca_laf = "Al bakalım... 😈"
                    else:
                        st.session_state.amca_renk = "altin"
                        st.session_state.amca_laf = f"'{t['harf'].upper()}' harfi {t['yer']+1}. sıradadır. Kullan."
                    st.rerun()
                else:
                    st.session_state.hata = "⚠️ Yeterli XP yok!"
                    st.rerun()
        with col2:
            if st.button("❌ Reddet", use_container_width=True):
                st.session_state.teklif_goster = False
                if t["blof"]:
                    st.session_state.amca_renk = "kopurme"
                    st.session_state.amca_laf = "Hah! Akıllı sandın kendini..."
                else:
                    st.session_state.amca_renk = "kopurme"
                    st.session_state.amca_laf = "Pişman olacaksın!"
                st.rerun()

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
            izgara_html += '<div class="kutu"> </div>'
    izgara_html += '</div>'
izgara_html += '</div>'
st.markdown(izgara_html, unsafe_allow_html=True)

# ── Hata mesajı ────────────────────────────────────────────────────────────────
if st.session_state.hata:
    st.warning(st.session_state.hata)

# ── Oyun sonu mesajı ───────────────────────────────────────────────────────────
if st.session_state.oyun_bitti:
    if st.session_state.kazandi:
        mesajlar = {1:"Efsane! 🏆", 2:"Muhteşem! 🎉", 3:"Harika! 🌟",
                    4:"İyi iş! 👏", 5:"Neredeyse! 😅", 6:"Tam son anda! 😤"}
        st.success(f"{mesajlar[len(st.session_state.tahminler)]} — Toplam XP: {st.session_state.xp:.2f}")
    else:
        st.error(f"Kaybettin! Kelime: **{st.session_state.gizli.upper()}** — XP: {st.session_state.xp:.2f}")

# ── Giriş ──────────────────────────────────────────────────────────────────────
def normalize(s):
    # Türkçe büyük/küçük harf dönüşümü — standart lower() İ→i ve I→i yapar, biz düzeltiyoruz
    s = s.replace("İ", "i").replace("I", "ı").replace("Ş", "ş").replace("Ğ", "ğ")
    s = s.replace("Ü", "ü").replace("Ö", "ö").replace("Ç", "ç")
    return s.lower()

def degerlendir(tahmin, gizli):
    sonuc = ["yanlis"] * 5
    g = list(gizli)
    kullanildi = [False] * 5
    for i in range(5):
        if tahmin[i] == g[i]:
            sonuc[i] = "dogru"
            kullanildi[i] = True
    for i in range(5):
        if sonuc[i] == "dogru":
            continue
        for j in range(5):
            if not kullanildi[j] and tahmin[i] == g[j]:
                sonuc[i] = "yakin"
                kullanildi[j] = True
                break
    return sonuc

def teklif_olustur(gizli, tahminler):
    """Amca teklif oluşturur. %40 blöf."""
    blof = random.random() < 0.40
    denenen = set()
    for t in tahminler:
        denenen.update(t)

    if blof:
        # Yanlış harf veya yanlış konum ver
        yanlis_harfler = [h for h in "abcçdefgğhıijklmnoöprsştuüvyz" if h not in gizli]
        if yanlis_harfler:
            harf = random.choice(yanlis_harfler)
            yer  = random.randint(0, 4)
        else:
            harf = random.choice(list(gizli))
            yer  = random.choice([i for i in range(5) if gizli[i] != harf])
            if not yer:
                yer = 0
        mesaj = f"'{harf.upper()}' harfi {yer+1}. sırada olabilir... belki."
        return {"harf": harf, "yer": yer, "blof": True, "mesaj": mesaj}
    else:
        # Gerçek ipucu — henüz bulunmamış bir harf
        bilinmeyenler = [(i, gizli[i]) for i in range(5)
                         if not any(len(t) > i and t[i] == gizli[i] for t in tahminler)]
        if not bilinmeyenler:
            bilinmeyenler = list(enumerate(gizli))
        yer, harf = random.choice(bilinmeyenler)
        mesaj = f"Bak, sana gerçeği söyleyeyim. '{harf.upper()}' harfi {yer+1}. sıradadır."
        return {"harf": harf, "yer": yer, "blof": False, "mesaj": mesaj}

if not st.session_state.oyun_bitti:
    col1, col2 = st.columns([4, 1])
    with col1:
        girdi = st.text_input("", max_chars=5, placeholder="5 harf yaz...",
                               label_visibility="collapsed", key="girdi")
    with col2:
        gonder = st.button("Gönder", use_container_width=True)

    if gonder and girdi:
        tahmin = normalize(girdi.strip())
        if len(tahmin) != 5:
            st.session_state.hata = "⚠️ Tam olarak 5 harf gir!"
            st.rerun()
        elif not tahmin.isalpha():
            st.session_state.hata = "⚠️ Sadece harf kullan!"
            st.rerun()
        else:
            st.session_state.hata = ""
            gizli = st.session_state.gizli
            sonuc = degerlendir(tahmin, gizli)
            deneme_no = len(st.session_state.tahminler)

            # XP hesapla
            kazan, yeni_puan = xp_hesapla(tahmin, gizli, sonuc, st.session_state.puan_alanlar)
            st.session_state.puan_alanlar.update(yeni_puan)

            # Blöf kullanıldı mı kontrol et
            teklif = st.session_state.teklif
            if teklif and st.session_state.teklif_kabul and teklif["blof"]:
                # Blöf ipucundaki harf bu tahminde kullanıldı mı?
                blof_harfi = teklif["harf"]
                blof_yeri  = teklif["yer"]
                if len(tahmin) > blof_yeri and tahmin[blof_yeri] == blof_harfi:
                    st.session_state.amca_renk = "kahkaha"
                    st.session_state.amca_laf  = "HAHAHAHA! Düştün tuzağa! 🤣"
                st.session_state.teklif = None
                st.session_state.teklif_kabul = False

            st.session_state.tahminler.append(tahmin)
            st.session_state.sonuclar.append(sonuc)

            # Klavye güncelle
            oncelik = {"dogru": 3, "yakin": 2, "yanlis": 1}
            for i, harf in enumerate(tahmin):
                mevcut = st.session_state.klavye.get(harf)
                if mevcut is None or oncelik[sonuc[i]] > oncelik.get(mevcut, 0):
                    st.session_state.klavye[harf] = sonuc[i]

            # Kazandı mı?
            if all(s == "dogru" for s in sonuc):
                bonus = dogru_tahmin_bonusu(deneme_no)
                kazan += bonus
                st.session_state.xp += kazan
                st.session_state.oyun_bitti = True
                st.session_state.kazandi    = True
                if amca_gorunsun:
                    st.session_state.amca_renk = "altin"
                    st.session_state.amca_laf  = "Şaşırdım. Gerçekten."
            elif len(st.session_state.tahminler) >= MAX_DENEME:
                st.session_state.xp += kazan
                st.session_state.oyun_bitti = True
                st.session_state.kazandi    = False
                if amca_gorunsun:
                    st.session_state.amca_renk = "normal"
                    st.session_state.amca_laf  = "Beklenenden de kötüydü bu."
            else:
                st.session_state.xp += kazan
                # Amca laf atsın
                if amca_gorunsun and st.session_state.amca_renk not in ("kahkaha",):
                    kalan = MAX_DENEME - len(st.session_state.tahminler)
                    if kalan == 1:
                        st.session_state.amca_laf = random.choice(LAFLAR_SON_TAHMIN)
                    else:
                        st.session_state.amca_laf = random.choice(LAFLAR_NORMAL)
                    st.session_state.amca_renk = "normal"

                    # Teklif: XP çift sayıda ise
                    xp_simdi = st.session_state.xp
                    if int(xp_simdi) % 2 == 0 and int(xp_simdi) > 0 and not st.session_state.teklif_goster:
                        st.session_state.teklif = teklif_olustur(gizli, st.session_state.tahminler)
                        st.session_state.teklif_goster = True
                        st.session_state.teklif_kabul  = False
                        st.session_state.amca_renk = "teklif"
                        st.session_state.amca_laf  = "Dur bir dakika... Sana bir teklifim var."

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
    xp_sakla = st.session_state.xp
    yeni_oyun()
    st.session_state.xp = xp_sakla
    st.rerun()

st.markdown(f"<p style='text-align:center;color:#444;font-size:0.7rem;margin-top:1rem'>{len(KELIMELER)} kelime</p>", unsafe_allow_html=True)
