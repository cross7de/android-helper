from pathlib import Path

VERSION = "2.0.0"

class Ctx:
    dry_run: bool = False
    quiet: bool = False
    yes: bool = False
    adb_path: str = "adb"
    config_dir: Path = Path.cwd() / "config"
    apks_dir: Path = Path.cwd() / "apks"
    state_dir: Path = Path.cwd() / "state"
    profile: str = "auto"  # auto | moto | xiaomi_miui | xiaomi_hyperos | generic

ctx = Ctx()

# Fallback-Defaults, wenn kein Profil/keine Listen gefunden werden
DEFAULT_DEBLOAT_GENERIC = [
    "com.facebook.katana|Facebook",
    "com.facebook.appmanager|Facebook App Manager",
    "com.facebook.services|Facebook Services",
    "com.facebook.system|Facebook System",
    "com.instagram.android|Instagram",
    "com.netflix.mediaclient|Netflix",
    "com.booking|Booking.com",
    "com.linkedin.android|LinkedIn",
    "com.amazon.mShop.android.shopping|Amazon Shopping",
    "com.amazon.appmanager|Amazon App Manager",
    "cn.wps.moffice_eng|WPS Office",
    "com.google.android.youtube|YouTube",
    "com.google.android.youtube.music|YouTube Music",
    "com.google.android.videos|Google TV",
    "com.google.android.apps.magazines|Google News",
    "com.google.android.apps.podcasts|Google Podcasts",
    "com.google.android.apps.tachyon|Google Meet",
    "com.google.android.apps.subscriptions.red|Google One",
    "com.google.ar.lens|Google Lens",
    "com.google.android.gm|Gmail",
    "com.google.android.apps.docs|Google Drive",
    "com.google.android.apps.photos|Google Photos",
    "com.google.android.apps.messaging|Google Messages",
    "com.google.android.googlequicksearchbox|Google App/Assistant",
]

DEFAULT_DEBLOAT_MOTO = DEFAULT_DEBLOAT_GENERIC + [
    "com.motorola.help|Moto Hilfe",
    "com.motorola.genie|Moto Tipps/Assistent",
    "com.motorola.timeweatherwidget|Moto Zeit & Wetter Widget",
    "com.motorola.android.fmradio|Moto FM Radio",
    "com.motorola.gamemode|Moto Game Mode",
    "com.motorola.bug2go|Moto Feedback/Bug2Go",
    "com.motorola.screenshoteditor|Screenshot Editor",
    "com.motorola.demo|Retail Demo",
]

DEFAULT_DEBLOAT_XIAOMI = DEFAULT_DEBLOAT_GENERIC + [
    "com.miui.player|Mi Music",
    "com.miui.videoplayer|Mi Video",
    "com.xiaomi.mipicks|GetApps Store",
    "com.xiaomi.glgm|Game Center",
    "com.miui.cleanmaster|Cleaner",
    "com.miui.miwallpaper|Wallpaper Carousel",
    "com.miui.bugreport|Feedback",
    "com.miui.notes|Xiaomi Notizen",
    "com.miui.browser|Mi Browser",
    "com.mi.globalbrowser|Mi Browser (Global)",
    "com.mi.android.globalFileexplorer|Dateimanager",
]

DEFAULT_PROTECT = {
    "com.google.android.gms",
    "com.google.android.gsf",
    "com.android.vending",
    "com.android.systemui",
    "com.android.phone",
    "com.android.providers.downloads",
    "com.android.providers.media",
    "com.motorola.ccc.ota",
}

def init_ctx(args):
    ctx.dry_run   = bool(getattr(args, "dry_run", False))
    ctx.quiet     = bool(getattr(args, "quiet", False))
    ctx.yes       = bool(getattr(args, "yes", False))
    ctx.adb_path  = getattr(args, "adb_path", ctx.adb_path)
    from pathlib import Path as _P
    ctx.config_dir = _P(getattr(args, "config_dir", ctx.config_dir))
    ctx.apks_dir   = _P(getattr(args, "apks_dir", ctx.apks_dir))
    ctx.state_dir  = _P(getattr(args, "state_dir", ctx.state_dir))
    ctx.profile    = getattr(args, "profile", ctx.profile)
