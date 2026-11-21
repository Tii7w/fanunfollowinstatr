Instagram Non-Followers Finder 🔍

Instagram'da takip ettiğiniz ancak sizi geri takip etmeyen hesapları kolayca tespit edin!

Bu proje, Instagram takipçi ve takip edilen listelerini karşılaştırarak sizi takip etmeyen kullanıcıları belirlemenizi sağlar.

✨ Özellikler

Takip ettiğiniz ancak sizi takip etmeyen hesapları listeleme.

Sizi takip eden ve sizin takip ettiğiniz hesapları karşılaştırma.

Karşılıklı takip durumunu analiz etme.

Takipçi ve takip edilen listelerindeki farklılıkları tespit etme.

Kolay ve kullanıcı dostu arayüz.

🎯 Amaç

Instagram takip listenizi daha kolay yönetmenizi, karşılıklı takip durumlarını analiz etmenizi ve sizi takip etmeyen hesapları hızlıca belirlemenizi sağlamak.



## İçindekiler

- [Hakkında](#hakkında)
- [Özellikler](#özellikler)
- [Nasıl çalışır?](#nasıl-çalışır)
- [Nasıl kurulur?](#nasıl-kurulur)
- [Nasıl kullanılır?](#nasıl-kullanılır)
- [Ayarlar](#ayarlar)
- [Dosya yapısı](#dosya-yapısı)
- [Uyarı](#uyarı)
- [Katkıda bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

---

## Hakkında

Takipçi sayın büyüdükçe kimi geri takip ettiğini, kimi etmediğini elle kontrol etmek imkânsız hale gelir. **FanUnfollowInsta**, takipçi listenle takip listeni karşılaştırır ve **seni takip eden ama senin takip etmediğin** ("tek taraflı") hesapları bulur.

Bu hesaplarla ne yapacağına sen karar verirsin:

- **listelersin** ya da dosyaya kaydedersin,
- **geri takip edersin**,
- **takipçilerinden çıkarırsın**,
- ya da **gece modunu** açarsın; program hepsini sen uyurken yavaşça takipçilerinden çıkarır.

Program bir terminal menüsüyle çalışır. Kod bilgisi gerektirmez. Windows'ta iki dosyaya çift tıklayarak kurulur ve başlatılır.

> Takipçiden çıkarılan kişiye Instagram bildirim göndermez. Geri takip ettiğin kişiye ise bildirim gider.

## Özellikler

| | Özellik | Açıklama |
|---|---|---|
| 🔍 | **Tek taraflı takipçileri bulma** | Seni takip eden ama senin takip etmediğin hesapları listeler |
| ➕ | **Toplu geri takip** | Seçtiğin sayıda hesabı geri takip eder |
| ➖ | **Toplu takipçiden çıkarma** | Seçtiğin sayıda hesabı takipçilerinden çıkarır |
| 🌙 | **Gece modu** | Hepsini gözetimsiz çıkarır; sınırlanırsa bekler, yarıda kalırsa kaldığı yerden devam eder |
| ⏱️ | **Ayarlanabilir hız** | Bekleme ve mola süreleri saniye cinsinden ayarlanır |
| 🛡️ | **Beyaz liste** | Listedeki hesaplara asla dokunulmaz |
| 💾 | **Dışa aktarma** | Listeyi metin dosyasına kaydeder |
| 🔐 | **Güvenli giriş** | Şifre `.env` dosyasında durur; oturum kaydedilir; iki adımlı doğrulama desteklenir |
| 📝 | **Kayıt** | Kimin ne zaman çıkarıldığı ve takip edildiği dosyalara yazılır |

## Nasıl çalışır?

```
 ┌──────────────┐     ┌──────────────────────┐     ┌─────────────────────────┐
 │  1. Giriş    │ ──▶ │ 2. Listeleri çekme   │ ──▶ │ 3. Karşılaştırma        │
 │ .env + 2FA   │     │ takipçiler / takip   │     │ takipçiler − takip      │
 │ oturum kayıt │     │ 200'lük parçalar     │     │ − beyaz liste           │
 └──────────────┘     └──────────────────────┘     └────────────┬────────────┘
                                                                │
                      ┌──────────────────────┐     ┌────────────▼────────────┐
                      │ 5. Kayıt             │ ◀── │ 4. İşlem                │
                      │ log dosyaları,       │     │ listele / geri takip /  │
                      │ gece modu durumu     │     │ çıkar (bekleyerek)      │



## Nasıl kurulur?

> **Kısaca (Windows):** Python'u kur → projeyi indir → `kurulum.bat` → `.env` dosyasına bilgilerini yaz → `baslat.bat`

### Windows'ta adım adım kurulum

#### Adım 1: Python'u kur

1. [python.org/downloads](https://www.python.org/downloads/) adresine git ve **Download Python** düğmesine tıkla.
2. İndirilen dosyayı çalıştır.
3. Kurulumun **ilk ekranında** alttaki **"Add python.exe to PATH"** kutusunu işaretle. Bu adım önemli; işaretlemezsen kurulum çalışmaz.
4. **Install Now**'a tıkla ve kurulumun bitmesini bekle.

Doğru kurulduğunu kontrol etmek için Başlat menüsünden **Komut İstemi**'ni (`cmd`) aç ve şunu yaz:

```bash
python --version
```

Ekranda `Python 3.10` veya üstü bir sürüm görmelisin.

#### Adım 2: Projeyi indir

**A) ZIP olarak (en kolayı):**

1. Bu sayfanın üstündeki yeşil **Code** düğmesine tıkla ve **Download ZIP**'i seç.
2. İnen ZIP dosyasına sağ tıkla ve **Tümünü ayıkla** de. Örneğin Masaüstüne çıkar.

**B) Git ile:**

```bash
git clone https://github.com/tii7w/fanunfollowinsta.git
cd fanunfollowinsta
```

#### Adım 3: Kurulumu çalıştır

Proje klasöründeki **`kurulum.bat`** dosyasına **çift tıkla**. Bu dosya:

- Python'un kurulu olup olmadığını kontrol eder,
- projeye özel bir sanal ortam (`.venv`) oluşturur,
- gerekli paketleri (`instagrapi`, `python-dotenv`) kurar,
- bir `.env` dosyası hazırlar.

Ekranda **"Kurulum tamam."** yazısını görünce pencereyi kapatabilirsin.

> Windows "Bilgisayarınız korundu" uyarısı gösterirse **Ek bilgi → Yine de çalıştır**'a tıkla.

#### Adım 4: Giriş bilgilerini yaz

Proje klasöründeki **`.env`** dosyasına sağ tıkla, **Birlikte aç → Not Defteri**'ni seç ve kendi bilgilerini yaz:

```env
IG_USERNAME="kullanici_adin"
IG_PASSWORD="sifren"
```

Kaydet (**Ctrl+S**) ve kapat.

> `.env` dosyası şifreni içerir. Kimseyle paylaşma; GitHub'a yüklenmez.

#### Adım 5: Programı başlat

**`baslat.bat`** dosyasına çift tıkla. Menü açılıyorsa kurulum tamam. 🎉
İlk girişte doğrulama kodu istenebilir, bkz. [Nasıl kullanılır?](#nasıl-kullanılır)

### macOS / Linux kurulumu

Terminali aç ve sırasıyla şunları çalıştır:

```bash
# 1. Projeyi indir
git clone https://github.com/tii7w/fanunfollowinsta.git
cd fanunfollowinsta

# 2. Sanal ortamı oluştur ve etkinleştir
python3 -m venv .venv
source .venv/bin/activate

# 3. Paketleri kur
pip install -r requirements.txt

# 4. .env dosyasını oluştur ve düzenle
cp .env.example .env
nano .env        # kullanıcı adını ve şifreni yaz, Ctrl+O ile kaydet, Ctrl+X ile çık

# 5. Başlat
python bot.py
```

Sonraki açılışlarda sadece şunları çalıştırman yeterli:

```bash
cd fanunfollowinsta
source .venv/bin/activate
python bot.py
```


## Nasıl kullanılır?

### 1. İlk giriş

`baslat.bat` ile programı aç. Hesabında iki adımlı doğrulama açıksa şunlardan birini girmen istenir:

| Yöntem | Nasıl? |
|---|---|
| **Yedek kod** ⭐ önerilir | Instagram → Ayarlar → Hesaplar Merkezi → Şifre ve güvenlik → İki faktörlü kimlik doğrulama → hesabın → Ek yöntemler → **Yedek kodlar**. 8 haneli kodlardan birini gir (her kod bir kez kullanılabilir). |
| **SMS / doğrulama uygulaması** | Gelen 6 haneli kodu gir. |
| **Tarayıcı oturumu** | `s` yaz, instagram.com çerezlerindeki `sessionid` değerini yapıştır. Instagram bu oturumu kısa sürede kapatabilir, o yüzden son çare olarak kullan. |

Giriş bir kez yapılır. Sonraki açılışlarda kod sorulmaz.

### 2. Menü

```
1) Listele: beni takip eden ama benim takip etmediklerim
2) Onları geri takip et
3) Onları takipçilerimden çıkar
4) Listeyi dosyaya kaydet
5) Listeleri Instagram'dan yenile
6) Ayarlar: bekleme ve mola süreleri (saniye)
7) GECE MODU: hepsini otomatik ve yavaşça takipçilerimden çıkar
0) Çıkış
```

**Önerilen ilk kullanım:**

1. **1** ile listeyi gör.
2. Dokunulmasını istemediğin hesapları `config/whitelist.txt` dosyasına ekle ve **5** ile listeyi yenile.
3. **3** ile önce az sayıda (örneğin 10) hesabı çıkararak dene.
4. Her şey yolundaysa **7** ile gece modunu başlat.

> 2 ve 3 numaralı işlemler, başlamadan önce kaç kişi işleneceğini sorar ve onay ister. İstediğin an **Ctrl+C** ile durdurabilirsin.

### 3. Gece modu

Tek taraflı takipçilerinin **hepsini** sen uyurken tek tek takipçilerinden çıkarır.

1. Menüden **7**'yi seç.
2. Bekleme ve mola sürelerini onayla ya da değiştir, sonra `e` ile başlat.
3. Bilgisayarı **şarja tak** ve **kapağını açık bırak**. Program çalışırken Windows'un uykuya geçmesini engeller, ama kapak kapanınca bilgisayar yine de uyuyabilir.
4. Pencereyi kapatma ve yat. 😴

**Sabah:** Gecenin özeti `config/gece_log.txt` dosyasında. İş bitmediyse tekrar **7**'yi seçtiğinde program kaldığı yerden devam eder.

| Durum | Gece modunun davranışı |
|---|---|
| Gecelik sınıra ulaşıldı (varsayılan 300) | Durur, kalanları ertesi geceye bırakır |
| Instagram işlemi sınırladı | 2 saat bekler, yeniden dener (en fazla 2 kez) |
| Doğrulama istendi / oturum kapandı | Hemen durur |
| Program kapandı | Ertesi açılışta kaldığı yerden devam eder |

Menüsüz doğrudan başlatmak için: `python bot.py --gece`

## Ayarlar

Ayarlar `ayarlar.txt` dosyasındadır. Program bu dosyayı ilk açılışta oluşturur. Dosyayı elle düzenleyebilir ya da menüden **6** ile soru-cevap şeklinde değiştirebilirsin. Tüm süreler **saniye** cinsindendir. Program "en az" ile "en fazla" arasında rastgele bir süre bekler; ikisini eşit yaparsan hep aynı süre bekler.

| Ayar | Varsayılan | Açıklama |
|---|---|---|
| `bekleme_en_az_saniye` / `bekleme_en_fazla_saniye` | 45 / 90 | Her işlem arası bekleme |
| `mola_kac_islemde_bir` | 10 | Kaç işlemde bir uzun mola (`0` = mola yok) |
| `mola_en_az_saniye` / `mola_en_fazla_saniye` | 300 / 600 | Uzun mola süresi |
| `gece_en_fazla_islem` | 300 | Gece modunda bir gecede en fazla işlem |
| `menu_tek_seferde_islem` | 30 | Menüde (2 / 3) önerilen kişi sayısı |

> ⚠️ 20 saniyeden kısa beklemeler Instagram'ın hesabı geçici olarak kısıtlama riskini artırır.

**Beyaz liste:** `config/whitelist.txt` dosyasına her satıra bir kullanıcı adı yaz. Bu hesaplar hiçbir işleme dahil edilmez.

```
yakin_arkadasim
@annem
```

## Dosya yapısı

```
fanunfollowinsta/
├── bot.py                  # Programın kendisi
├── kurulum.bat             # Windows kurulumu
├── baslat.bat              # Windows başlatma
├── requirements.txt        # Python paketleri
├── .env.example            # .env şablonu
├── .env                    # Kullanıcı adı / şifre       (kurulumda oluşur, paylaşma)
├── ayarlar.txt             # Hız ayarları                (ilk açılışta oluşur)
└── config/                 # (ilk açılışta oluşur)
    ├── whitelist.txt       # Dokunulmayacak hesaplar
    ├── session.json        # Kayıtlı oturum              (paylaşma)
    ├── removed_followers.txt  # Takipçilerden çıkarılanlar
    ├── followed.txt        # Geri takip edilenler
    ├── gece_log.txt        # Gece modu kaydı
    ├── gece_durum.json     # Gece modunun kaldığı yer
    └── hata.txt            # Beklenmeyen hataların ayrıntısı
```

`.env`, `ayarlar.txt` ve `config/` `.gitignore`'dadır, GitHub'a yüklenmez.


## Uyarı

Bu proje Instagram ya da Meta ile **bağlantılı değildir**. Otomasyon araçları Instagram'ın kullanım koşullarına aykırı olabilir ve hesabın geçici olarak kısıtlanmasına yol açabilir. Programı **yalnızca kendi hesabında** ve **kendi sorumluluğunda** kullan.

## Katkıda bulunma

Hata bildirimleri ve öneriler için [Issues](https://github.com/tii7w/fanunfollowinsta/issues) sayfasını kullanabilirsin. Pull request'ler memnuniyetle karşılanır.

1. Depoyu fork'la
2. Yeni bir dal aç: `git checkout -b ozellik/yeni-ozellik`
3. Değişikliklerini commit'le ve push'la
4. Pull request aç

## Teşekkür

- [instagrapi](https://github.com/subzeroid/instagrapi): Instagram özel API istemcisi
- Bu proje, [uwpear/instabot](https://github.com/uwpear/instabot) temel alınarak yeniden yazılmıştır.

## Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.
