import copy

from certs import make_pem

VLESS_UUID = "11111111-2222-4333-8444-555555555555"
SHADOWSOCKS_PASSWORD = "AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8="
PUBLIC_KEY = "A" * 43
HYSTERIA2_SERVER_NAME = "hy2.example.com"

_CERTIFICATE = {}


def certificate():
    if "pem" not in _CERTIFICATE:
        _CERTIFICATE["pem"] = make_pem(name=HYSTERIA2_SERVER_NAME)
    return _CERTIFICATE["pem"]


def shadowsocks(**changes):
    outbound = {
        "type": "shadowsocks",
        "tag": "ss-1",
        "server": "192.0.2.11",
        "server_port": 443,
        "method": "2022-blake3-chacha20-poly1305",
        "password": SHADOWSOCKS_PASSWORD,
    }
    outbound.update(changes)
    return outbound


def vless(**changes):
    outbound = {
        "type": "vless",
        "tag": "vless-1",
        "server": "192.0.2.12",
        "server_port": 443,
        "uuid": VLESS_UUID,
        "flow": "xtls-rprx-vision",
        "tls": {
            "enabled": True,
            "server_name": "www.example.com",
            "utls": {"enabled": True, "fingerprint": "chrome"},
            "reality": {"enabled": True, "public_key": PUBLIC_KEY},
        },
    }
    outbound.update(changes)
    return outbound


def samizdat(tag, server, port):
    return {
        "type": "samizdat",
        "tag": tag,
        "server": server,
        "server_port": port,
        "public_key": PUBLIC_KEY,
        "short_id": "0011223344556677",
        "server_name": "decoy.example.net",
    }


def hysteria2x(**changes):
    outbound = {
        "type": "hysteria2x",
        "tag": "hysteria2x-1",
        "server": "192.0.2.14",
        "server_port": 8443,
        "password": "hy2-example-password",
        "tls": {"enabled": True, "server_name": HYSTERIA2_SERVER_NAME, "certificate": certificate()},
        "pre_initial_junk": True,
    }
    outbound.update(changes)
    return outbound


def response():
    outbounds = [
        shadowsocks(),
        vless(),
        samizdat("samizdat-1", "192.0.2.13", 5942),
        hysteria2x(),
        samizdat("samizdat-2", "192.0.2.15", 37183),
    ]
    frankfurt = {"country": "Germany", "city": "Frankfurt", "latitude": 50.11, "longitude": 8.68, "country_code": "DE"}
    amsterdam = {"country": "Netherlands", "city": "Amsterdam", "latitude": 52.37, "longitude": 4.9, "country_code": "NL"}
    return copy.deepcopy(
        {
            "country": "IR",
            "outbound_locations": {
                "ss-1": frankfurt,
                "vless-1": frankfurt,
                "samizdat-1": frankfurt,
                "hysteria2x-1": amsterdam,
                "samizdat-2": frankfurt,
            },
            "options": {"outbounds": outbounds},
            "poll_interval_seconds": 180,
        }
    )
