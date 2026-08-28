import json
import re


def _maybe_unescape_payload(text, start):
    idx = start + 1
    while idx < len(text) and text[idx].isspace():
        idx += 1

    if text[idx:idx + 2] != '\\"':
        return text

    try:
        return json.loads(f'"{text}"', strict=False)
    except Exception:
        return text.replace('\\"', '"')


def _extract_js_object(text):
    start = text.find("{")
    if start == -1:
        return None

    text = _maybe_unescape_payload(text, start)
    start = text.find("{")
    if start == -1:
        return None

    deep = 0
    in_string = False
    quote = ""
    escaped = False

    for idx in range(start, len(text)):
        ch = text[idx]

        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                in_string = False
            continue

        if ch in ('"', "'"):
            in_string = True
            quote = ch
            continue

        if ch == "{":
            deep += 1
        elif ch == "}":
            deep -= 1

        if deep == 0:
            result = text[start: idx + 1]
            result = result.replace("undefined", "{}")
            try:
                return json.loads(result)
            except Exception:
                result = result.replace('\\"', '"')
                result = result.replace("\\'", "'")
                return json.loads(result)
    return None


def _extract_html(html, rule, key=None):
    if isinstance(html, bytes):
        html = html.decode("utf-8", errors="ignore")

    payloads = re.findall(rule, html)
    for raw_payload in payloads:
        if key and key not in raw_payload:
            continue
        # logging.info(raw_payload)
        data = _extract_js_object(raw_payload)
        if not data:
            continue
        return data