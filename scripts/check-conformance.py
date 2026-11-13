"""Reference evaluator for the code-analysis rules of the SchemaFirst A11y Standard.

Validates standards/a11y/standard.json against its schema (when jsonschema is installed),
checks that every rule references a known category, then runs every case in cases/ and
reports mismatches. Only rules this script implements may appear in a case's `expected`.

Usage: python3 scripts/check-conformance.py
"""
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STANDARD = json.load(open(os.path.join(ROOT, "standards/a11y/standard.json")))
SCHEMA = json.load(open(os.path.join(ROOT, "schemas/a11y-standard.schema.json")))
LABELLESS_INPUTS = {"hidden", "submit", "reset", "button", "image"}
BCP47 = re.compile(r"^[A-Za-z]{2,3}(-[A-Za-z0-9]{2,8})*$")


class Doc(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.stack = []
        self.title = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        el = {"tag": tag, "attrs": dict(attrs), "ancestors": [e["tag"] for e in self.stack], "text": ""}
        self.elements.append(el)
        if tag not in ("img", "input", "meta", "link", "br", "hr", "source", "track"):
            self.stack.append(el)
        if tag == "title":
            self._in_title = True
            self.title = ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        for el in self.stack:
            el["text"] += data


def find(doc, *tags):
    return [e for e in doc.elements if e["tag"] in tags]


def result(failures, applicable=True):
    if not applicable:
        return "not-applicable"
    return "fail" if failures else "pass"


def page_language(doc):
    html = find(doc, "html")
    lang = html[0]["attrs"].get("lang") if html else None
    return result(not (lang and BCP47.match(lang.strip())))


def page_title(doc):
    return result(doc.title is None or not doc.title.strip())


def viewport_zoom_enabled(doc):
    metas = [m for m in find(doc, "meta") if (m["attrs"].get("name") or "").lower() == "viewport"]
    bad = False
    for m in metas:
        content = (m["attrs"].get("content") or "").lower().replace(" ", "")
        opts = dict(p.split("=", 1) for p in content.split(",") if "=" in p)
        if opts.get("user-scalable") in ("no", "0"):
            bad = True
        try:
            if "maximum-scale" in opts and float(opts["maximum-scale"]) < 2:
                bad = True
        except ValueError:
            pass
    return result(bad)


def images_alt_present(doc):
    imgs = find(doc, "img") + [i for i in find(doc, "input") if (i["attrs"].get("type") or "").lower() == "image"]
    return result(any("alt" not in i["attrs"] for i in imgs), applicable=bool(imgs))


def focus_order(doc):
    def positive(e):
        try:
            return int(e["attrs"].get("tabindex", "0")) > 0
        except ValueError:
            return False
    return result(any(positive(e) for e in doc.elements))


def no_autofocus(doc):
    return result(any("autofocus" in e["attrs"] and "dialog" not in e["ancestors"] for e in doc.elements))


def landmarks(doc):
    mains = find(doc, "main") + [e for e in doc.elements if e["attrs"].get("role") == "main" and e["tag"] != "main"]
    return result(len(mains) != 1)


def h1_present(doc):
    return result(not find(doc, "h1"))


def heading_hierarchy(doc):
    heads = [e for e in doc.elements if re.fullmatch(r"h[1-6]", e["tag"])]
    prev, bad = 0, False
    for h in heads:
        level = int(h["tag"][1])
        if prev and level > prev + 1:
            bad = True
        if not h["text"].strip():
            bad = True
        prev = level
    return result(bad, applicable=bool(heads))


def form_labels(doc):
    controls = [
        e for e in find(doc, "input", "select", "textarea")
        if not (e["tag"] == "input" and (e["attrs"].get("type") or "text").lower() in LABELLESS_INPUTS)
    ]
    label_for = {l["attrs"].get("for") for l in find(doc, "label") if l["attrs"].get("for")}
    bad = False
    for c in controls:
        a = c["attrs"]
        labelled = (
            (a.get("id") and a["id"] in label_for)
            or "label" in c["ancestors"]
            or (a.get("aria-label") or "").strip()
            or (a.get("aria-labelledby") or "").strip()
        )
        if not labelled:
            bad = True
    return result(bad, applicable=bool(controls))


CHECKS = {
    "page-language": page_language,
    "page-title": page_title,
    "viewport-zoom-enabled": viewport_zoom_enabled,
    "images-alt-present": images_alt_present,
    "focus-order": focus_order,
    "no-autofocus": no_autofocus,
    "landmarks": landmarks,
    "h1-present": h1_present,
    "heading-hierarchy": heading_hierarchy,
    "form-labels": form_labels,
}


def check_standard():
    errors = []
    try:
        import jsonschema
        for e in jsonschema.Draft202012Validator(SCHEMA).iter_errors(STANDARD):
            errors.append(f"schema: {'/'.join(map(str, e.absolute_path))}: {e.message}")
    except ImportError:
        print("note: jsonschema not installed; skipped schema validation")
    for rid, r in STANDARD["rules"].items():
        if r["category"] not in STANDARD["categories"]:
            errors.append(f"rule {rid}: unknown category {r['category']}")
    for rid in CHECKS:
        if rid not in STANDARD["rules"] or "code-analysis" not in STANDARD["rules"][rid]["detection"]:
            errors.append(f"checker implements {rid}, which is not a code-analysis rule")
    return errors


def main():
    errors = check_standard()
    cases = sorted(glob.glob(os.path.join(ROOT, "cases/*.json")))
    for path in cases:
        case = json.load(open(path))
        doc = Doc()
        doc.feed(case["input"]["subject"])
        for rid, want in case["expected"]["results"].items():
            got = CHECKS[rid](doc)
            if got != want["status"]:
                errors.append(f"{os.path.basename(path)}: {rid} expected {want['status']}, got {got}")
    for e in errors:
        print("FAIL", e)
    print(f"{len(cases)} cases, {len(STANDARD['rules'])} rules, {len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
