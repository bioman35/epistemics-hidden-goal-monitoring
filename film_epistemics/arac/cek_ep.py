# coding: utf-8
"""TESLIM VIDEOSU · 3B sahne cekimi (cik.py duzeni, 14 Kas). Her kosu ayri sayfa: index.html?ep=1&f=N&render=1, 960x600.
Yazi yok; yazilar kur.py katmaninda. GPU: d3d11. Yayin programi ve baska basliksiz tarayici kapaliyken, yazilimciyla sirayla.
python -I cek_ep.py plan                     EP_PLAN (cekim listesi) ve sure, iki kosu
python -I cek_ep.py pano CIKTI.jpg t1 t2 ..  iki kosu yan yana, secilen anlar (her an icin 1 sn geriden 1/30 adimla gelinir)
python -I cek_ep.py tam KLASOR               KLASOR/DU/000000.jpg ... ve KLASOR/EG/..., KLASOR/plan.json"""
import functools
import http.server
import io
import json
import os
import sys
import threading

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

KOK = os.path.dirname(os.path.abspath(__file__))
FPS = 30
EN, BOY = 960, 600
KOSU = (("DU", 0), ("EG", 1))
KIP = os.environ.get("EPKIP", "1")   # v4 (14 Kas): EPKIP=4 tek akis (film.js epBaslat4)


class Sessiz(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass


def sunucu():
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Sessiz, directory=KOK))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


def ac(p, port, f):
    tr = p.chromium.launch(headless=True, args=["--use-angle=d3d11", "--ignore-gpu-blocklist", "--enable-webgl"])
    s = tr.new_page(viewport={"width": EN, "height": BOY}, device_scale_factor=1)
    h = []
    s.on("pageerror", lambda e: h.append(str(e)[:300]))
    s.on("console", lambda m: h.append(m.text[:300]) if m.type == "error" else None)
    s.goto("http://127.0.0.1:%d/index.html?ep=%s&f=%d&render=1" % (port, KIP, f))
    try:
        s.wait_for_function("window.HAZIR === true", timeout=90000)
    except Exception:
        print("hazir olmadi", h[:5])
        raise
    s.evaluate("document.fonts.ready.then(() => 1)")
    s.add_style_tag(content="*{transition:none!important}")
    return tr, s, h


def kare(s, t):
    s.evaluate("t => window.kare(t)", t)
    return s.screenshot(type="jpeg", quality=94)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    A = sys.argv
    srv = sunucu()
    port = srv.server_address[1]
    with sync_playwright() as p:
        if A[1] == "plan":
            for ad, f in KOSU:
                tr, s, h = ac(p, port, f)
                print(ad, json.dumps(s.evaluate("window.EP_PLAN"), ensure_ascii=False))
                print("SURE", round(s.evaluate("window.SURE"), 3), "hata", h[:4])
                print("renderer", s.evaluate("(() => { const g = document.createElement('canvas').getContext('webgl2'); const e = g.getExtension('WEBGL_debug_renderer_info'); return g.getParameter(e.UNMASKED_RENDERER_WEBGL); })()"))
                tr.close()
        elif A[1] == "pano":
            tl = [float(x) for x in A[3:]]
            g = Image.new("RGB", (2 * EN, len(tl) * BOY)); d = ImageDraw.Draw(g)
            for j, (ad, f) in enumerate(KOSU):
                tr, s, h = ac(p, port, f)
                for i, t in enumerate(tl):
                    for q in range(30, 0, -1):
                        s.evaluate("t => window.kare(t)", max(0, t - q / FPS))
                    g.paste(Image.open(io.BytesIO(kare(s, t))), (j * EN, i * BOY))
                    d.rectangle([j * EN, i * BOY, j * EN + 120, i * BOY + 24], fill=(0, 0, 0)); d.text((j * EN + 6, i * BOY + 6), "%s %.2f" % (ad, t), fill=(255, 230, 0))
                print(ad, "hata", h[:4], "carp", s.evaluate("window.__carp()"))
                tr.close()
            g.save(A[2], quality=88)
            print("pano", A[2])
        elif A[1] == "tam":
            ck = A[2]
            plan = {}
            for ad, f in KOSU:
                os.makedirs(os.path.join(ck, ad), exist_ok=True)
                tr, s, h = ac(p, port, f)
                plan[ad] = s.evaluate("window.EP_PLAN")
                n = int(round(s.evaluate("window.SURE") * FPS))
                carp = []
                ekran = {}
                dur = {i: d["an"] for d in plan[ad].get("duruslar", []) for i in range(int(d["t0"] * FPS), int(round(d["t1"] * FPS)))}   # durusun her karesi (kamera duruşta da kayar)
                for i in range(n):
                    with open(os.path.join(ck, ad, "%06d.jpg" % i), "wb") as o:
                        o.write(kare(s, i / FPS))
                    if i in dur:
                        ekran[i] = dict(s.evaluate("i => window.__ekranAn(i)", dur[i]), an=dur[i])
                    if i % 15 == 0:
                        c = s.evaluate("window.__carp()")
                        if c:
                            carp.append([i, c])
                    if i % 300 == 0:
                        print(ad, i, "/", n, flush=True)
                plan[ad]["kare"] = n
                plan[ad]["carp"] = carp
                plan[ad]["ekran"] = ekran
                print(ad, "tamam", n, "kare, hata", h[:3], "carp", carp[:5])
                tr.close()
            json.dump(plan, open(os.path.join(ck, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
