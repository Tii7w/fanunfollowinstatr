<div align="center">

# FanUnfollowInsta

**Seni takip eden ama senin takip etmediğin Instagram hesaplarını bul: listele, geri takip et ya da takipçilerinden çıkar.**

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

---

## İçindekiler

- [Hakkında](#hakkında)
- [Özellikler](#özellikler)
- [Nasıl çalışır?](#nasıl-çalışır)
- [Gereksinimler](#gereksinimler)
- [Nasıl kurulur?](#nasıl-kurulur)
- [Nasıl kullanılır?](#nasıl-kullanılır)
- [Ayarlar](#ayarlar)
- [Dosya yapısı](#dosya-yapısı)
- [Sık sorulan sorular](#sık-sorulan-sorular)
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
                      └──────────────────────┘     └─────────────────────────┘
```

1. **Giriş.** Program, Instagram'ın mobil uygulamasının kullandığı API üzerinden [instagrapi](https://github.com/subzeroid/instagrapi) kütüphanesiyle giriş yapar. Kullanıcı adı ve şifre `.env` dosyasından okunur. İki adımlı doğrulama açıksa kod istenir. Başarılı giriş `config/session.json` dosyasına kaydedilir, böylece sonraki açılışlarda yeniden giriş ve kod gerekmez.

2. **Listeleri çekme.** Takipçi ve takip listeleri 200 kişilik sayfalar halinde çekilir. Instagram'ı yormamak için her sayfa arasında birkaç saniye beklenir. Menü işlemlerinde hız için en yeni 1000 takipçi, gece modunda ise listenin tamamı kullanılır.

3. **Karşılaştırma.** "Takipçiler" kümesinden "takip ettiklerin" ve beyaz listedeki hesaplar çıkarılır. Geriye kalanlar tek taraflı takipçilerindir.

4. **İşlem.** Seçtiğin işlem her hesap için tek tek yapılır. İki işlem arasında, `ayarlar.txt` dosyasındaki aralıktan rastgele seçilen bir süre beklenir. Belirli sayıda işlemden sonra uzun bir mola verilir. Rastgele bekleme, işlemlerin insan davranışına benzemesini sağlar.

5. **Güvenlik freni.** Instagram işlemi sınırlarsa (`FeedbackRequired`, `PleaseWaitFewMinutes` vb.) devam eden toplu işlem hemen durur. Gece modunda ise 2 saat bekleyip yeniden dener. Doğrulama istenirse ya da oturum kapanırsa her durumda durur.

6. **Kayıt.** Yapılan her işlem tarihiyle kaydedilir. Gece modu kaldığı yeri `config/gece_durum.json` dosyasına yazar, böylece program kapansa bile ertesi açılışta listeyi baştan çekmeden devam eder.

## Gereksinimler

- **Python 3.10 veya üstü**: [python.org/downloads](https://www.python.org/downloads/)
- **Windows 10/11**, macOS ya da Linux
- İki adımlı doğrulama açıksa şunlardan biri: **yedek kod**, **SMS** ya da **doğrulama uygulaması**. Instagram'ın "Bu sen misin?" bildirim onayı desteklenmez (bkz. [SSS](#sık-sorulan-sorular)).

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

### Güncelleme

- **Git ile indirdiysen:** proje klasöründe `git pull` çalıştır, ardından `kurulum.bat`'ı bir kez daha çalıştır.
- **ZIP ile indirdiysen:** yeni ZIP'i indir. Eski klasördeki `.env`, `ayarlar.txt` ve `config/` klasörünü yeni klasöre kopyala, sonra `kurulum.bat`'ı çalıştır.

### Kaldırma

Proje klasörünü silmen yeterli. Program bilgisayarında başka bir yere dosya yazmaz.

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

## Sık sorulan sorular

<details>
<summary><b>Kod istiyor ama telefonuma kod gelmiyor.</b></summary>

Hesabını Instagram'ın "Bu sen misin?" bildirimiyle onaylıyorsan SMS gönderilmez ve bu program o bildirimi kullanamaz. 8 haneli **yedek kod** ile giriş yap ya da iki adımlı doğrulamaya bir **doğrulama uygulaması** (Google Authenticator vb.) ekle.
</details>

<details>
<summary><b>"Instagram oturumu kapattı" / <code>login_required</code> hatası alıyorum.</b></summary>

Instagram oturumu sonlandırmış. Kayıtlı oturum otomatik silinir. Instagram uygulamasında "Bu sen miydin?" uyarısı varsa **"Bendim"** de, en az 1 saat bekle ve yeniden giriş yap.
</details>

<details>
<summary><b><code>FeedbackRequired</code> veya <code>PleaseWaitFewMinutes</code> hatası.</b></summary>

Instagram işlemleri geçici olarak sınırladı. Birkaç saat bekle. `ayarlar.txt` dosyasında bekleme sürelerini artır ve `gece_en_fazla_islem` değerini düşür.
</details>

<details>
<summary><b>Hesabım kapatılır mı?</b></summary>

Program temkinli varsayılanlarla gelir: rastgele beklemeler, molalar, gecelik sınır ve Instagram uyardığı anda durma. Yine de her otomasyon aracı risk taşır. Hızı artırmak riski de artırır.
</details>

<details>
<summary><b>Başka bir hata aldım.</b></summary>

Ayrıntılar `config/hata.txt` dosyasına yazılır. Sorun bildirirken bu dosyayı ekleyebilirsin, ama içinde kişisel bilgi olmadığından emin ol.
</details>

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
