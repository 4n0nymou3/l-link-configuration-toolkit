import json
import re

from . import upstream as U
from .errors import ValidationError


def _normalized_key(key):
    return re.sub(r"[^a-z0-9]", "", key.lower())


USER_ID_KEYS = frozenset({"userid", _normalized_key(U.HEADER_USER_ID)})
HEADER_FORM = "[-_]?".join(re.escape(part) for part in U.HEADER_USER_ID.lower().split("-"))


def _is_user_id(value, user_id):
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return value == user_id
    if isinstance(value, str):
        return value.strip() == str(user_id)
    return False


def _json_exposes_user_id(document, user_id):
    pending = [document]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            for key, child in item.items():
                if isinstance(key, str) and _normalized_key(key) in USER_ID_KEYS and _is_user_id(child, user_id):
                    return True
                pending.append(child)
        elif isinstance(item, list):
            pending.extend(item)
    return False


def _text_exposes_user_id(text, user_id):
    pattern = re.compile(
        r"(?<![a-z0-9_-])(?:%s|user[-_]?id)(?![a-z0-9])[\"']?\s*[:=]\s*[\"']?%d(?![0-9a-z])" % (HEADER_FORM, user_id),
        re.IGNORECASE,
    )
    return pattern.search(text) is not None


def ensure_no_state_in_files(files, state):
    token = state.token.encode("utf-8")
    secrets = {"device id": state.device_id.encode("utf-8")}
    secrets["token"] = token if len(token) >= 8 else b'"' + token + b'"'
    for name, content in files.items():
        for label, secret in secrets.items():
            if secret and secret in content:
                raise ValidationError("account data (%s) was found in %s, refusing to publish" % (label, name))
        text = content.decode("utf-8", errors="replace")
        exposed = _text_exposes_user_id(text, state.user_id)
        if not exposed:
            try:
                exposed = _json_exposes_user_id(json.loads(text), state.user_id)
            except ValueError:
                exposed = False
        if exposed:
            raise ValidationError("account data (user id) was found in %s, refusing to publish" % name)
