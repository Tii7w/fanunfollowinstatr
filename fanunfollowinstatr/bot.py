"""
FanUnfollowInsta — Instagram takipçi aracı (instagrapi).

Odak: seni takip eden ama senin takip etmediğin kişiler.
  - listele / dosyaya kaydet
  - geri takip et
  - takipçilerinden çıkar
  - gece modu: hepsini gözetimsiz ve yavaşça takipçilerinden çıkar

Giriş bilgileri .env dosyasından okunur (IG_USERNAME, IG_PASSWORD).
Bekleme/mola süreleri ayarlar.txt dosyasındadır.
config/whitelist.txt içindeki kullanıcılara hiçbir işlem yapılmaz.

Kullanım:  python bot.py          (menü)
           python bot.py --gece   (menüsüz doğrudan gece modu)
"""

import json
import os
import random
import sys
import time
from getpass import getpass
from pathlib import Path

from dotenv import load_dotenv
from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword,
    ChallengeRequired,
    ClientThrottledError,
    FeedbackRequired,
    LoginRequired,
    PleaseWaitFewMinutes,
    TwoFactorRequired,
)

BASE = Path(__file__).resolve().parent
CONFIG = BASE / "config"
SESSION_FILE = CONFIG / "session.json"
WHITELIST_FILE = CONFIG / "whitelist.txt"
FOLLOWED_LOG = CONFIG / "followed.txt"
REMOVED_LOG = CONFIG / "removed_followers.txt"
EXPORT_FILE = BASE / "takip_etmediklerim.txt"

# Hesabı korumak için temkinli ayarlar
SETTINGS_FILE = BASE / "ayarlar.txt"

# ayarlar.txt yoksa bu değerlerle oluşturulur. Bekleme/mola ayarları menü
# modunda da gece modunda da kullanılır.
SETTINGS_LAYOUT = [
    ("Her takipçiden çıkarma / geri takip arasındaki bekleme",
     [("bekleme_en_az_saniye", 45), ("bekleme_en_fazla_saniye", 90)]),
    ("Belirli sayıda işlemden sonra verilen uzun mola",
     [("mola_kac_islemde_bir", 10), ("mola_en_az_saniye", 300),
      ("mola_en_fazla_saniye", 600)]),
    ("Gece modunda bir gecede en fazla kaç kişi çıkarılsın",
     [("gece_en_fazla_islem", 300)]),
    ("Menüden (2 / 3) tek seferde önerilen kişi sayısı",
     [("menu_tek_seferde_islem", 30)]),
]
DEFAULT_SETTINGS = {k: v for _, items in SETTINGS_LAYOUT for k, v in items}
S = dict(DEFAULT_SETTINGS)  # main() içinde ayarlar.txt'den doldurulur

FETCH_DELAY_RANGE = (4, 9)  # liste çekerken her 200 kişilik sayfa arası bekleme
FOLLOWER_LIMIT = 1000       # sadece en yeni N takipçi çekilir (0 = hepsi)

# Instagram "dur" dediğinde hemen bırakacağımız hatalar
STOP_ERRORS = (
    FeedbackRequired,
    PleaseWaitFewMinutes,
    ClientThrottledError,
    ChallengeRequired,
    LoginRequired,
)

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ---------------------------------------------------------------- yardımcılar

def read_usernames(path: Path) -> set[str]:
    if not path.exists():
        return set()
    names = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip().lstrip("@").lower()
        if line and not line.startswith("#"):
            names.add(line)
    return names


def append_log(path: Path, username: str) -> None:
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with path.open("a", encoding="utf-8") as f:
        f.write(f"{stamp}\t{username}\n")


def ask_int(prompt: str, default: int) -> int:
    raw = input(f"{prompt} [{default}]: ").strip()
    if not raw:
        return default
    try:
        return max(0, int(raw))
    except ValueError:
        print("Geçersiz sayı, varsayılan kullanılıyor.")
        return default


def confirm(prompt: str) -> bool:
    return input(f"{prompt} (e/h): ").strip().lower() in ("e", "evet", "y", "yes")


# ---------------------------------------------------------------- ayarlar

def save_settings(s: dict) -> None:
    lines = [
        "# Instagram bot ayarları. Değiştirip kaydet; bot bir sonraki açılışta okur.",
        "# Tüm süreler SANİYE cinsindendir. Bot 'en az' ile 'en fazla' arasında",
        "# rastgele bir süre bekler. İkisini eşit yaparsan hep aynı süre bekler.",
    ]
    for title, items in SETTINGS_LAYOUT:
        lines += ["", f"# {title}"]
        lines += [f"{k} = {s[k]}" for k, _ in items]
    SETTINGS_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _fix_ranges(s: dict) -> None:
    for lo, hi in (("bekleme_en_az_saniye", "bekleme_en_fazla_saniye"),
                   ("mola_en_az_saniye", "mola_en_fazla_saniye")):
        if s[lo] > s[hi]:
            s[lo], s[hi] = s[hi], s[lo]


def load_settings() -> dict:
    s = dict(DEFAULT_SETTINGS)
    if not SETTINGS_FILE.exists():
        save_settings(s)
        return s
    for raw in SETTINGS_FILE.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if "=" not in line:
            continue
        key, value = (x.strip() for x in line.split("=", 1))
        if key not in s:
            continue
        try:
            s[key] = max(0, int(value))
        except ValueError:
            print(f"ayarlar.txt: '{key} = {value}' sayı değil, {s[key]} kullanılıyor.")
    _fix_ranges(s)
    return s


def _span(lo: int, hi: int) -> str:
    return f"{lo} sn" if lo == hi else f"{lo}-{hi} sn"


def delay_text() -> str:
    wait = _span(S["bekleme_en_az_saniye"], S["bekleme_en_fazla_saniye"])
    if S["mola_kac_islemde_bir"]:
        rest = _span(S["mola_en_az_saniye"], S["mola_en_fazla_saniye"])
        return f"bekleme {wait}, her {S['mola_kac_islemde_bir']} işlemde {rest} mola"
    return f"bekleme {wait}, mola yok"


def _ask_numbers(prompt: str, max_count: int, minimum: int) -> list[int] | None:
    """Enter = None (değiştirme). Geçersizse tekrar sorar."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            return None
        try:
            nums = [int(x) for x in raw.replace("-", " ").replace(",", " ").split()]
        except ValueError:
            nums = []
        if 1 <= len(nums) <= max_count and min(nums) >= minimum:
            return nums
        print("  Geçersiz giriş, tekrar dene (değiştirmemek için Enter).")


def _ask_range(title: str, lo_key: str, hi_key: str, warn_below: int = 0) -> None:
    current = _span(S[lo_key], S[hi_key])
    nums = _ask_numbers(f"{title} [şu an {current}]: ", 2, 1)
    if nums is None:
        return
    S[lo_key], S[hi_key] = min(nums), max(nums)
    if warn_below and S[lo_key] < warn_below:
        print(f"  Uyarı: {warn_below} sn'den kısa süreler hesabın kısıtlanma riskini artırır.")


def edit_delay() -> None:
    print(f"\nŞu anki ayar: {delay_text()}")
    print("Süreleri SANİYE olarak gir:\n"
          "  tek sayı  (örn. 60)    = her seferinde tam 60 sn\n"
          "  iki sayı  (örn. 45 90) = 45 ile 90 sn arası rastgele\n"
          "  Enter                  = değiştirme\n")

    _ask_range("1) Her işlem arası bekleme (sn)",
               "bekleme_en_az_saniye", "bekleme_en_fazla_saniye", warn_below=20)

    every = _ask_numbers(
        f"2) Kaç işlemde bir uzun mola verilsin? (0 = mola yok) "
        f"[şu an {S['mola_kac_islemde_bir']}]: ", 1, 0)
    if every is not None:
        S["mola_kac_islemde_bir"] = every[0]

    if S["mola_kac_islemde_bir"]:
        _ask_range(f"3) Her {S['mola_kac_islemde_bir']} işlemde mola süresi (sn)",
                   "mola_en_az_saniye", "mola_en_fazla_saniye")

    save_settings(S)
    print(f"Kaydedildi ({SETTINGS_FILE.name}): {delay_text()}")


def action_pause(done_count: int, sleeper) -> None:
    """İki işlem arası bekleme; her N işlemde bir uzun mola."""
    every = S["mola_kac_islemde_bir"]
    if every and done_count and done_count % every == 0:
        sleeper(random.randint(S["mola_en_az_saniye"], S["mola_en_fazla_saniye"]), "Mola")
    else:
        sleeper(random.randint(S["bekleme_en_az_saniye"], S["bekleme_en_fazla_saniye"]),
                "Bekleniyor")


def countdown(seconds: int, label: str) -> None:
    for left in range(seconds, 0, -1):
        print(f"\r  {label}: {left:>3} sn ", end="", flush=True)
        time.sleep(1)
    print("\r" + " " * 40 + "\r", end="")


# ---------------------------------------------------------------- giriş

SESSIONID_HELP = """
sessionid nasıl alınır:
  1. Bilgisayarda tarayıcıdan instagram.com'a gir (bildirimle onayla).
  2. F12 > Application (Chrome/Edge) veya Storage (Firefox) > Cookies
     > https://www.instagram.com
  3. 'sessionid' satırının Value değerini kopyala.
  (Yapıştırınca ekranda görünmez, sonra Enter'a bas.)
"""


def new_client() -> Client:
    cl = Client()
    cl.delay_range = [1, 3]
    return cl


def try_saved_session() -> Client | None:
    if not SESSION_FILE.exists():
        return None
    cl = new_client()
    try:
        cl.load_settings(SESSION_FILE)
        cl.account_info()  # oturum hâlâ geçerli mi?
        print("Kayıtlı oturumla giriş yapıldı.")
        return cl
    except Exception:
        print("Kayıtlı oturumun süresi dolmuş, yeniden giriş gerekiyor.")
        return None


def login_with_sessionid(sessionid: str = "") -> Client:
    if not sessionid:
        print(SESSIONID_HELP)
        sessionid = getpass("sessionid: ")
    sessionid = sessionid.strip().strip('"').strip("'")
    cl = new_client()
    try:
        cl.login_by_sessionid(sessionid)
    except Exception as e:
        sys.exit(f"sessionid ile giriş başarısız ({e}). Değeri tekrar kopyalayıp dene.")
    return cl


def login_with_password(username: str, password: str) -> Client:
    cl = new_client()
    try:
        cl.login(username, password)
        return cl
    except BadPassword:
        sys.exit("Şifre yanlış. .env dosyasındaki IG_PASSWORD değerini kontrol et.")
    except TwoFactorRequired:
        pass

    print("""
Hesabında iki adımlı doğrulama açık.
Instagram'ın bildirimle onayını bu bot kullanamıyor, o yüzden şunlardan birini yap:
  - 8 haneli YEDEK KOD gir (Instagram > Hesaplar Merkezi > Şifre ve güvenlik >
    İki faktörlü kimlik doğrulama > hesabın > Ek yöntemler > Yedek kodlar)
  - SMS veya doğrulama uygulaması kodun varsa onu gir
  - ya da 's' yaz: tarayıcıdaki oturumunla (sessionid) giriş yap
""")
    for _ in range(3):
        answer = input("Kod veya 's': ").strip()
        if answer.lower() == "s":
            return login_with_sessionid()
        try:
            cl.login(username, password, verification_code=answer)
            return cl
        except TwoFactorRequired as e:
            print(f"Kod kabul edilmedi, tekrar dene.\n  (Instagram: {e})")
    sys.exit("Doğrulama başarısız. Birkaç dakika sonra tekrar dene.")


def login() -> Client:
    load_dotenv(BASE / ".env")
    CONFIG.mkdir(exist_ok=True)

    cl = try_saved_session()
    if cl is None:
        sessionid = os.getenv("IG_SESSIONID", "")
        if sessionid:
            cl = login_with_sessionid(sessionid)
        else:
            username = os.getenv("IG_USERNAME") or input("Instagram kullanıcı adı: ").strip()
            password = os.getenv("IG_PASSWORD") or getpass("Şifre: ")
            cl = login_with_password(username, password)
        print("Giriş başarılı.")

    cl.dump_settings(SESSION_FILE)
    return cl


# ---------------------------------------------------------------- veri

class Data:
    def __init__(self, cl: Client, follower_limit: int = FOLLOWER_LIMIT):
        self.cl = cl
        self.follower_limit = follower_limit
        self.followers = {}
        self.following = {}
        self.refresh()

    def _fetch(self, chunk_fn, label: str, limit: int = 0) -> dict:
        """Listeyi 200'lük parçalar halinde, aralarda bekleyerek çeker."""
        users, max_id = {}, ""
        while True:
            chunk, max_id = chunk_fn(str(self.cl.user_id), max_amount=200, max_id=max_id)
            for u in chunk:
                users[u.pk] = u
            print(f"\r  {label}: {len(users)} kişi alındı", end="", flush=True)
            if not max_id or (limit and len(users) >= limit):
                break
            time.sleep(random.uniform(*FETCH_DELAY_RANGE))
        print()
        return users

    def refresh(self) -> None:
        if self.follower_limit:
            print(f"En yeni {self.follower_limit} takipçin alınıyor...")
        else:
            print("Takipçilerin alınıyor (kalabalık hesaplarda birkaç dakika sürebilir)...")
        self.followers = self._fetch(
            self.cl.user_followers_v1_chunk, "Takipçi", self.follower_limit
        )
        print("Takip ettiklerin alınıyor...")
        self.following = self._fetch(self.cl.user_following_v1_chunk, "Takip edilen")

    def not_followed_back(self):
        """Seni takip eden ama senin takip etmediğin kişiler."""
        whitelist = read_usernames(WHITELIST_FILE)
        users = [
            u for pk, u in self.followers.items()
            if pk not in self.following and u.username.lower() not in whitelist
        ]
        return sorted(users, key=lambda u: u.username.lower())


# ---------------------------------------------------------------- işlemler

def show_list(users) -> None:
    if not users:
        print("Seni takip edip senin takip etmediğin kimse yok.")
        return
    for i, u in enumerate(users, 1):
        name = f" ({u.full_name})" if u.full_name else ""
        print(f"{i:>4}. @{u.username}{name}")
    print(f"\nToplam: {len(users)}")


def export_list(users) -> None:
    EXPORT_FILE.write_text(
        "\n".join(u.username for u in users) + "\n", encoding="utf-8"
    )
    print(f"{len(users)} kullanıcı kaydedildi: {EXPORT_FILE}")


def run_batch(data: Data, users, action: str) -> None:
    """action: 'follow' (geri takip) veya 'remove' (takipçiden çıkar)."""
    if not users:
        print("İşlem yapılacak kimse yok.")
        return

    verb = "geri takip edilecek" if action == "follow" else "takipçilerinden çıkarılacak"
    print(f"{len(users)} kişi uygun. Güvenlik için tek seferde en fazla "
          f"{S['menu_tek_seferde_islem']} önerilir. ({delay_text()})")
    limit = min(ask_int("Kaç kişi işlensin?", S["menu_tek_seferde_islem"]), len(users))
    if limit == 0:
        return
    targets = users[:limit]
    print("İlk kişiler: " + ", ".join("@" + u.username for u in targets[:10])
          + (" ..." if limit > 10 else ""))
    if not confirm(f"{limit} kişi {verb}. Devam?"):
        return

    done = 0
    try:
        for i, u in enumerate(targets, 1):
            try:
                if action == "follow":
                    ok = data.cl.user_follow(u.pk)
                else:
                    ok = data.cl.user_remove_follower(u.pk)
            except STOP_ERRORS as e:
                print(f"\nInstagram işlemi durdurdu ({type(e).__name__}). "
                      "Birkaç saat bekleyip tekrar dene.")
                break
            except Exception as e:
                print(f"[{i}/{limit}] @{u.username} atlandı: {e}")
                continue

            if ok:
                done += 1
                if action == "follow":
                    append_log(FOLLOWED_LOG, u.username)
                    data.following[u.pk] = u
                    print(f"[{i}/{limit}] @{u.username} geri takip edildi")
                else:
                    append_log(REMOVED_LOG, u.username)
                    data.followers.pop(u.pk, None)
                    print(f"[{i}/{limit}] @{u.username} takipçilerden çıkarıldı")
            else:
                print(f"[{i}/{limit}] @{u.username} için işlem başarısız")

            if i < limit:
                action_pause(i, countdown)
    except KeyboardInterrupt:
        print("\nKullanıcı tarafından durduruldu.")

    print(f"\nTamamlandı: {done}/{limit}")


# ---------------------------------------------------------------- gece modu
#
# Seni takip eden ama senin takip etmediğin HERKESİ, gözetimsiz ve yavaşça
# takipçilerinden çıkarır. Kaldığı yeri config/gece_durum.json'a yazar;
# yarıda kalırsa tekrar başlatınca listeyi baştan çekmeden devam eder.

NIGHT_STATE = CONFIG / "gece_durum.json"
NIGHT_LOG = CONFIG / "gece_log.txt"
# Bekleme, mola ve gecelik üst sınır ayarlar.txt'den gelir.
NIGHT_COOLDOWN = 2 * 3600       # Instagram sınırlarsa 2 saat bekle
NIGHT_MAX_COOLDOWNS = 2         # en fazla bu kadar kez bekleyip yeniden dene
NIGHT_MAX_FAILS = 5             # art arda bu kadar başarısızlık = sınırlandı say


def log(msg: str) -> None:
    line = f"{time.strftime('%H:%M:%S')}  {msg}"
    print(line, flush=True)
    with NIGHT_LOG.open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d')} {line}\n")


def keep_awake(on: bool) -> None:
    """Windows'un çalışırken uyku moduna geçmesini engeller."""
    try:
        import ctypes
        ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
        flags = ES_CONTINUOUS | (ES_SYSTEM_REQUIRED if on else 0)
        ctypes.windll.kernel32.SetThreadExecutionState(flags)
    except Exception:
        pass


def save_state(state: dict) -> None:
    NIGHT_STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")


def load_or_build_state(cl: Client) -> dict:
    if NIGHT_STATE.exists():
        state = json.loads(NIGHT_STATE.read_text(encoding="utf-8"))
        done = set(state["done"])
        left = sum(1 for t in state["targets"] if t["pk"] not in done)
        if left:
            log(f"Önceki listeden devam ediliyor ({state['created']}): {left} kişi kaldı.")
            return state

    log("Takipçi ve takip listeleri Instagram'dan çekiliyor (tam liste)...")
    data = Data(cl, follower_limit=0)
    users = data.not_followed_back()
    state = {
        "created": time.strftime("%Y-%m-%d %H:%M"),
        "targets": [{"pk": str(u.pk), "username": u.username} for u in users],
        "done": [],
    }
    save_state(state)
    log(f"Takipçi: {len(data.followers)} | Takip edilen: {len(data.following)} | "
        f"Çıkarılacak: {len(users)}  (liste: {NIGHT_STATE.name})")
    return state


def night_mode(cl: Client) -> None:
    keep_awake(True)
    log("=== Gece modu başladı ===")
    try:
        state = load_or_build_state(cl)
    except LoginRequired:
        SESSION_FILE.unlink(missing_ok=True)
        log("Instagram oturumu kapattı. Sabah yeniden giriş yapman gerekiyor.")
        return
    except STOP_ERRORS as e:
        log(f"Liste çekilirken Instagram sınırladı ({type(e).__name__}). Durduruldu.")
        return

    whitelist = read_usernames(WHITELIST_FILE)
    done = set(state["done"])
    todo = [t for t in state["targets"]
            if t["pk"] not in done and t["username"].lower() not in whitelist]
    night_max = S["gece_en_fazla_islem"]
    log(f"{len(todo)} kişi çıkarılacak; bu gece en fazla {night_max}. ({delay_text()})")

    removed = cooldowns = fails = 0
    i = 0
    try:
        while i < len(todo) and removed < night_max:
            t = todo[i]
            limited = None
            try:
                ok = cl.user_remove_follower(t["pk"])
            except (FeedbackRequired, PleaseWaitFewMinutes, ClientThrottledError) as e:
                limited = type(e).__name__
            except (ChallengeRequired, LoginRequired) as e:
                log(f"Instagram doğrulama istedi / oturumu kapattı ({type(e).__name__}). "
                    "Durduruldu — sabah Instagram uygulamasını kontrol et.")
                if isinstance(e, LoginRequired):
                    SESSION_FILE.unlink(missing_ok=True)
                break
            except Exception as e:
                log(f"@{t['username']} atlandı: {e}")
                i += 1
                continue
            else:
                if ok:
                    fails = 0
                    removed += 1
                    state["done"].append(t["pk"])
                    save_state(state)
                    append_log(REMOVED_LOG, t["username"])
                    log(f"[{removed}] @{t['username']} takipçilerden çıkarıldı")
                else:
                    fails += 1
                    log(f"@{t['username']} çıkarılamadı ({fails}/{NIGHT_MAX_FAILS})")
                    if fails >= NIGHT_MAX_FAILS:
                        limited = "art arda başarısız"
                i += 1

            if limited:
                cooldowns += 1
                fails = 0
                if cooldowns > NIGHT_MAX_COOLDOWNS:
                    log(f"Instagram yine sınırladı ({limited}). Bu gecelik durduruldu.")
                    break
                log(f"Instagram sınırladı ({limited}). {NIGHT_COOLDOWN // 3600} saat "
                    f"bekleniyor ({cooldowns}/{NIGHT_MAX_COOLDOWNS})...")
                time.sleep(NIGHT_COOLDOWN)
                continue

            if i < len(todo) and removed < night_max:
                action_pause(i, countdown)
    except KeyboardInterrupt:
        log("Kullanıcı tarafından durduruldu.")
    finally:
        keep_awake(False)

    left = sum(1 for t in state["targets"] if t["pk"] not in set(state["done"]))
    log(f"=== Bitti: bu gece {removed} kişi çıkarıldı, {left} kişi kaldı ===")
    if left == 0:
        NIGHT_STATE.unlink(missing_ok=True)
    else:
        log("Kalanlar için yarın botu açıp menüden 7'yi seç; kaldığı yerden devam eder.")


NIGHT_INFO = """
=== GECE MODU ===
Seni takip eden ama senin takip etmediğin HERKES, sen uyurken tek tek
takipçilerinden çıkarılır. Başlatmadan önce:
  - Bilgisayarı şarja tak, kapağını açık bırak (kapak kapanınca uyuyabilir).
  - Bu pencereyi kapatma. Durdurmak için Ctrl+C.
  - config/whitelist.txt içindeki kişilere dokunulmaz.
  - Yarıda kalırsa tekrar 7'yi seçince kaldığı yerden devam eder.
"""


def start_night_mode(cl: Client) -> bool:
    print(NIGHT_INFO)
    if NIGHT_STATE.exists():
        print("Not: Önceki gece modundan kalan bir liste var, onunla devam edilecek.")
    edit_delay()
    print(f"\nBir gecede en fazla {S['gece_en_fazla_islem']} kişi "
          f"(ayarlar.txt > gece_en_fazla_islem).")
    if not confirm("Gece modu başlasın mı?"):
        return False
    night_mode(cl)
    return True


# ---------------------------------------------------------------- menü

MENU = """
1) Listele: beni takip eden ama benim takip etmediklerim
2) Onları geri takip et
3) Onları takipçilerimden çıkar
4) Listeyi dosyaya kaydet
5) Listeleri Instagram'dan yenile
6) Ayarlar: bekleme ve mola süreleri (saniye)
7) GECE MODU: hepsini otomatik ve yavaşça takipçilerimden çıkar
0) Çıkış
"""


def load_data(cl: Client, data: "Data | None" = None) -> "Data | None":
    """Listeleri çeker/yeniler. Instagram sınırlarsa None döner."""
    try:
        if data is None:
            return Data(cl)
        data.refresh()
        return data
    except LoginRequired:
        SESSION_FILE.unlink(missing_ok=True)
        sys.exit("Instagram oturumu kapattı. Kayıtlı oturum silindi; "
                 "bir süre bekleyip yeniden giriş yap (yedek kod önerilir).")
    except STOP_ERRORS as e:
        print(f"Instagram şu an isteği kısıtladı ({type(e).__name__}). "
              "Birkaç saat sonra tekrar dene.")
        return data


def ensure_whitelist() -> None:
    if not WHITELIST_FILE.exists():
        WHITELIST_FILE.write_text(
            "# Bu dosyaya yazdığın kullanıcı adlarına bot hiçbir işlem yapmaz.\n"
            "# Her satıra bir kullanıcı adı (@ olmadan da olur).\n",
            encoding="utf-8",
        )


def main() -> None:
    CONFIG.mkdir(exist_ok=True)
    S.update(load_settings())
    ensure_whitelist()

    cl = login()
    if "--gece" in sys.argv:  # menüsüz doğrudan gece modu
        night_mode(cl)
        return

    data = None  # listeler ilk ihtiyaç olduğunda çekilir
    while True:
        if data:
            users = data.not_followed_back()
            print(f"\nTakipçi (en yeni {len(data.followers)}) | Takip edilen: "
                  f"{len(data.following)} | Seni takip eden, senin etmediğin: {len(users)}")
        print(MENU)
        try:
            choice = input("Seçim: ").strip()
        except (EOFError, KeyboardInterrupt):
            choice = "0"

        if choice in ("1", "2", "3", "4", "5"):
            if data is None or choice == "5":
                data = load_data(cl, data)
            if data is None:
                continue
            users = data.not_followed_back()

        if choice == "1":
            show_list(users)
        elif choice == "2":
            run_batch(data, users, "follow")
        elif choice == "3":
            run_batch(data, users, "remove")
        elif choice == "4":
            export_list(users)
        elif choice == "5":
            pass  # yukarıda yenilendi
        elif choice == "6":
            edit_delay()
        elif choice == "7":
            if start_night_mode(cl):
                break
        elif choice == "0":
            print("Çıkış yapıldı.")
            break
        else:
            print("Geçersiz seçim.")


if __name__ == "__main__":
    try:
        main()
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception as e:
        import traceback
        CONFIG.mkdir(exist_ok=True)
        with (CONFIG / "hata.txt").open("a", encoding="utf-8") as f:
            f.write(f"\n===== {time.strftime('%Y-%m-%d %H:%M:%S')} =====\n")
            f.write(traceback.format_exc())
        print(f"\nHATA: {type(e).__name__}: {e}")
        print("Ayrıntılar config/hata.txt dosyasına kaydedildi.")
        sys.exit(1)
