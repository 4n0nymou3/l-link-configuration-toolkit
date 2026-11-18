from . import __version__

DEFAULT_COUNTRY = "IR"
DEFAULT_USER_AGENT = "l-link-configuration-toolkit/" + __version__

CONNECT_TIMEOUT = 15
READ_TIMEOUT = 45
CONFIG_ATTEMPTS = 3
RETRY_BASE_DELAY = 5.0
RETRY_JITTER = 3.0
RETRY_MAX_DELAY = 60.0
RETRY_AFTER_CAP = 120.0
RETRY_STATUSES = (429, 500, 502, 503, 504)

MIN_CONFIGS = 1
MAX_CONFIGS = 1000

DEFAULT_OUTPUT_DIR = "subscription"
DEFAULT_STATE_FILE = "state/upstream-account.enc"
STATE_KEY_ENV = "L_STATE_ENCRYPTION_KEY"
BOOTSTRAP_MODES = ("none", "create", "recreate")
HYSTERIA2_LINK_MODES = ("omit", "include")
DEFAULT_HYSTERIA2_LINKS = "omit"

SHADOWSOCKS_METHODS = (
    "2022-blake3-aes-128-gcm",
    "2022-blake3-aes-256-gcm",
    "2022-blake3-chacha20-poly1305",
    "aes-128-gcm",
    "aes-256-gcm",
    "chacha20-ietf-poly1305",
    "xchacha20-ietf-poly1305",
)

SUBSCRIPTION_LINKS_FILE = "sub.txt"
SUBSCRIPTION_SINGBOX_FILE = "singbox.json"
SUBSCRIPTION_XRAY_FILE = "xray.json"
URLTEST_URL = "https://www.gstatic.com/generate_204"

PROFILE_NAME = "\U0001F47D Anonymous L \U0001F680"
URLTEST_NAME = "\U0001F47D Anonymous L \U0001F310"
IRAN_RULES_BASE_URL = "https://raw.githubusercontent.com/Chocolate4U/Iran-sing-box-rules/rule-set/"
