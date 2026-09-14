import re, urllib.parse, requests
from flask import Flask, request, jsonify, Response, stream_with_context

app = Flask(__name__)
from flask import send_file

@app.route("/logo2.png")
def serve_logo():
    return send_file("/home/ubuntu/downloader/logo2.png", mimetype="image/png")


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="icon" type="image/png" href="/logo2.png">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BiliSnap HD - Best Free Bilibili Video Downloader Online (HD & MP4)</title>
    <meta name="description" content="Download Bilibili videos in 1080p, 4K MP4 for free. Fast, high-speed Bilibili video saver for creators, students, and anime lovers.">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: #0284c7; --accent: #22c55e; --text-dark: #0f172a; --text-muted: #64748b; --card-border: #e2e8f0; }
        * { margin:0; padding:0; box-sizing:border-box; font-family:"Plus Jakarta Sans",sans-serif; }
        body { background:#ffffff; color:var(--text-dark); line-height:1.6; }
        .container { max-width:1200px; margin:0 auto; padding:0 20px; }
        nav { background:#fff; border-bottom:1px solid var(--card-border); position:sticky; top:0; z-index:100; }
        .nav-wrap { display:flex; justify-content:space-between; align-items:center; height:70px; }
        .logo { font-size:24px; font-weight:800; color:var(--primary); text-decoration:none; display:flex; align-items:center; gap:8px; }
        .logo span { color:var(--text-dark); }
        .hero { background:linear-gradient(180deg, #f0f9ff 0%, #fff 100%); padding:50px 0 35px; text-align:center; }
        .hero-badge { display:inline-block; background:#e0f2fe; color:#0369a1; padding:6px 14px; border-radius:999px; font-size:13px; font-weight:700; margin-bottom:14px; }
        .hero h1 { font-size:34px; font-weight:800; max-width:800px; margin:0 auto 12px; }
        .hero p { color:var(--text-muted); max-width:600px; margin:0 auto 30px; font-size:15px; }
        .card-box { background:#fff; border:2px solid #bae6fd; border-radius:16px; padding:22px; max-width:740px; margin:0 auto; box-shadow:0 15px 30px -10px rgba(0,0,0,0.06); }
        .input-row { display:flex; gap:10px; flex-direction:column; }
        @media(min-width:640px){ .input-row { flex-direction:row; } }
        .input-wrap { position:relative; flex:1; }
        .input-wrap input { width:100%; height:52px; padding:0 90px 0 14px; border:1.5px solid var(--card-border); border-radius:10px; font-size:15px; outline:none; }
        .btn-paste { position:absolute; right:8px; top:8px; height:36px; padding:0 12px; border:none; background:#e2e8f0; border-radius:6px; font-weight:600; cursor:pointer; }
        .btn-extract { height:52px; padding:0 24px; background:var(--primary); color:#fff; border:none; border-radius:10px; font-weight:700; font-size:15px; cursor:pointer; }
        .robot-check { margin-top:12px; font-size:13px; color:var(--text-muted); display:flex; align-items:center; justify-content:center; gap:6px; }
        #status { margin-top:14px; font-weight:600; font-size:14px; }
        #result-box { display:none; margin-top:20px; padding:16px; background:#f8fafc; border:1px solid var(--card-border); border-radius:12px; text-align:left; }
        .dl-btn { display:block; text-align:center; background:var(--accent); color:#fff; padding:12px; border-radius:8px; font-weight:700; text-decoration:none; margin-top:10px; }
        .sec-title { text-align:center; margin:60px 0 30px; }
        .sec-title h2 { font-size:28px; font-weight:800; margin-bottom:6px; }
        .sec-title p { color:var(--text-muted); font-size:15px; }
        .grid-3 { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:20px; }
        .grid-card { background:#fff; border:1px solid var(--card-border); border-radius:14px; padding:24px; }
        .grid-card h3 { font-size:18px; margin-bottom:8px; }
        .grid-card p { color:var(--text-muted); font-size:14px; }
        .article-card { background:#fff; border:1px solid var(--card-border); border-radius:14px; overflow:hidden; }
        .article-card img { width:100%; height:160px; object-fit:cover; }
        .article-card div { padding:18px; }
        .article-card h4 { font-size:16px; margin-bottom:6px; }
        .article-card p { color:var(--text-muted); font-size:13px; }
        footer { background:#0f172a; color:#94a3b8; padding:45px 0 25px; margin-top:70px; font-size:14px; }
        .foot-links { display:flex; flex-wrap:wrap; gap:16px; justify-content:center; margin-bottom:20px; }
        .foot-links a { color:#cbd5e1; text-decoration:none; }
    
        .logo-text { font-size:22px; font-weight:800; letter-spacing:-0.5px; display:inline-flex; align-items:center; gap:6px; }
        .logo-text .main-part { background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .logo-text .sub-part { color: #0f172a; font-weight:800; }
        .logo-badge { font-size:10px; font-weight:800; background: linear-gradient(135deg, #f97316, #ea580c); color:#fff; padding:2px 6px; border-radius:6px; text-transform:uppercase; letter-spacing:0.8px; }

    
        .logo-wrap { display: flex; align-items: center; gap: 12px; text-decoration: none; }
        .logo-img-box { position: relative; display: flex; align-items: center; justify-content: center; }
        .logo-img-box img { height: 42px; width: 42px; object-fit: contain; filter: drop-shadow(0 4px 10px rgba(2, 132, 199, 0.25)); transition: transform 0.3s ease; }
        .logo-img-box img:hover { transform: scale(1.05); }
        .brand-title { display: flex; align-items: center; font-size: 24px; font-weight: 900; letter-spacing: -0.8px; line-height: 1; }
        .brand-bili { background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .brand-save { background: linear-gradient(135deg, #f97316 0%, #ea580c 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-left: 2px; }
        .brand-pill { margin-left: 8px; font-size: 10px; font-weight: 800; background: linear-gradient(135deg, #38bdf8, #0284c7); color: #fff; padding: 2px 7px; border-radius: 999px; letter-spacing: 0.8px; box-shadow: 0 2px 6px rgba(2, 132, 199, 0.3); text-transform: uppercase; }

    
        .hero h1 { font-size: 34px; font-weight: 900; line-height: 1.2; letter-spacing: -1px; margin: 0 auto 14px; max-width: 820px; }
        .hero-gradient-text { background: linear-gradient(135deg, #0284c7 0%, #38bdf8 50%, #6366f1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; display: inline-block; filter: drop-shadow(0 2px 8px rgba(2, 132, 199, 0.2)); }
        .hero-sub { color: #475569; font-size: 15px; font-weight: 500; max-width: 620px; margin: 0 auto 26px; }
        .hero-badge { background: #e0f2fe; color: #0284c7; border: 1px solid #bae6fd; font-weight: 800; font-size: 12px; letter-spacing: 0.5px; text-transform: uppercase; padding: 6px 16px; border-radius: 999px; margin-bottom: 16px; display: inline-flex; align-items: center; gap: 6px; }

    
        .tip-container { display:none; margin-top:16px; padding:16px; background:linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border:1.5px dashed #f59e0b; border-radius:12px; text-align:center; animation:fadeIn 0.5s ease; }
        @keyframes fadeIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }
        .tip-title { font-size:14px; font-weight:800; color:#92400e; margin-bottom:4px; display:flex; align-items:center; justify-content:center; gap:6px; }
        .tip-sub { font-size:12px; color:#78350f; margin-bottom:12px; line-height:1.4; }
        .tip-amounts { display:flex; justify-content:center; gap:8px; margin-bottom:12px; flex-wrap:wrap; }
        .tip-chip { background:#fff; border:1px solid #fcd34d; padding:6px 14px; border-radius:999px; font-size:12.5px; font-weight:700; color:#b45309; text-decoration:none; box-shadow:0 2px 4px rgba(245,158,11,0.1); transition:0.2s; }
        .tip-chip:hover { background:#f59e0b; color:#fff; }
        .btn-bmc { display:inline-flex; align-items:center; justify-content:center; gap:8px; background:#ffdd00; color:#000; font-weight:800; font-size:13px; padding:10px 18px; border-radius:8px; text-decoration:none; box-shadow:0 3px 8px rgba(0,0,0,0.1); }

    </style>
</head>
<body>
    <nav><div class="container nav-wrap"><a href="/" class="logo-wrap">
            <div class="logo-img-box">
                <img src="/logo2.png" alt="BiliSave Logo">
            </div>
            <div class="brand-title">
                <span class="brand-bili">Bili</span><span class="brand-save">Save</span>
                <span class="brand-pill">HD</span>
            </div>
        </a></div></nav>
    <section class="hero">
        <div class="container">
            <div class="hero-badge"><i class="fa-solid fa-bolt"></i> Fastest Bilibili Video Downloader</div>
            <h1>Download Bilibili Videos <br><span class="hero-gradient-text">in Ultra 1080p HD & MP4</span></h1>
            <p class="hero-sub">Save viral clips, anime highlights, and full audio at blazing-fast CDN speeds — completely free and watermark-free.</p>
            <div class="card-box">
                <div class="input-row">
                    <div class="input-wrap">
                        <input type="text" id="urlInput" placeholder="Paste Bilibili link or b23.tv...">
                        <button class="btn-paste" onclick="pasteUrl()"><i class="fa-regular fa-paste"></i> Paste</button>
                    </div>
                    <button class="btn-extract" id="btnEx" onclick="extractVideo()">Get Download Link</button>
                </div>
                <div class="robot-check">
                    <input type="checkbox" id="robot" checked>
                    <label for="robot">I confirm I am not a robot (Safe SSL Download)</label>
                </div>
                <div id="status"></div>
                <div id="result-box">
                    <h4 id="vtitle" style="margin-bottom:8px;"></h4>
                    <a href="" id="dllink" class="dl-btn" onclick="showTipBox()">Download Video (MP4)</a>
                <div id="tipBox" class="tip-container">
                    <div class="tip-title"><i class="fa-solid fa-mug-hot"></i> Fuel Our High-Speed Servers</div>
                    <p class="tip-sub">BiliSave is 100% free with zero ads. If this tool saved your time, consider buying us a coffee! ☕</p>
                    <div class="tip-amounts">
                        <a href="https://buymeacoffee.com/bilisave" target="_blank" class="tip-chip"> Coffee</a>
                        <a href="https://buymeacoffee.com/bilisave" target="_blank" class="tip-chip"> Server Boost</a>
                        <a href="https://buymeacoffee.com/bilisave" target="_blank" class="tip-chip">0 Super Supporter</a>
                    </div>
                    <a href="https://buymeacoffee.com/bilisave" target="_blank" class="btn-bmc"><img src="https://cdn.buymeacoffee.com/buttons/bmc-new-btn-logo.svg" alt="coffee" style="height:18px;"> Buy us a Coffee (PayPal / Card)</a>
                </div>
                </div>
            </div>
        </div>
    </section>
    <div class="container">
        <div class="sec-title"><h2>Built for Every Creator</h2><p>Designed for learning, analyzing, and content creation.</p></div>
        <div class="grid-3">
            <div class="grid-card"><h3>Students & Learners</h3><p>Save full-length tutorials and computer courses for offline study without data loss.</p></div>
            <div class="grid-card"><h3>Researchers & Analysts</h3><p>Archive tech keynotes, AI demonstrations, and public trends in high bitrates.</p></div>
            <div class="grid-card"><h3>Content Creators</h3><p>Extract viral 60FPS references, dance choreography, and anime scenes for reaction edits.</p></div>
        </div>
        <div class="sec-title"><h2>Why Choose BiliSnap HD</h2><p>SEO Optimized, fast buffering, and completely free.</p></div>
        <div class="grid-3">
            <div class="grid-card"><h3>High-Speed 4MB Pipeline</h3><p>Direct buffer pipelines ensure maximum download speeds with zero timeouts.</p></div>
            <div class="grid-card"><h3>100% Free & Unlimited</h3><p>Download as many video clips and tutorials as you need with no subscriptions.</p></div>
            <div class="grid-card"><h3>Original Audio & HD</h3><p>Get original quality video streams with clear synced sound.</p></div>
        </div>
        <div class="sec-title"><h2>Trending Guides & Bilibili Insights</h2><p>Latest articles and media tips.</p></div>
        <div class="grid-3">
            <div class="article-card"><img src="https://images.unsplash.com/photo-1578632767115-351597cf2477?w=600"><div><h4>Saving Exclusive Anime Overseas</h4><p>How fans watch and store official animations for flight trips.</p></div></div>
            <div class="article-card"><img src="https://images.unsplash.com/photo-1536240478700-b869070f9279?w=600"><div><h4>Choreography Reference Editing</h4><p>Analyzing viral 60FPS dance rhythms to create engaging Shorts.</p></div></div>
            <div class="article-card"><img src="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=600"><div><h4>Archiving Open Source AI Benchmarks</h4><p>Why researchers rely on Bilibili for technical model explanations.</p></div></div>
            <div class="article-card"><img src="https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600"><div><h4>Lecture Playlist Archiving</h4><p>How to download full university lectures for focused learning.</p></div></div>
            <div class="article-card"><img src="https://images.unsplash.com/photo-1542751371-adc38448a05e?w=600"><div><h4>High Bitrate Gaming Highlights</h4><p>Extracting frame-perfect tournament replays in HD quality.</p></div></div>
            <div class="article-card"><img src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600"><div><h4>Safe Online Video Downloading</h4><p>Why direct encrypted CDN tunneling prevents intrusive redirects.</p></div></div>
        </div>
    </div>
    <footer>
        <div class="container" style="text-align:center;">
            <div class="foot-links">
                <a href="#">Privacy Policy</a>
                <a href="#">DMCA & Copyright</a>
                <a href="#">Terms of Service</a>
                <a href="#">Contact Support</a>
            </div>
            <p>&copy; 2026 BiliSnap HD.com - Free Bilibili Video Downloader. All rights reserved.</p>
        </div>
    </footer>
    <script>
        async function pasteUrl() {
            try {
                const txt = await navigator.clipboard.readText();
                if(txt) { document.getElementById("urlInput").value = txt; extractVideo(); }
            } catch(e) {
                alert("Please paste manually into the box.");
            }
        }
        function showTipBox() { setTimeout(() => { document.getElementById("tipBox").style.display = "block"; }, 600); }
        async function extractVideo() {
            const val = document.getElementById("urlInput").value.trim();
            const status = document.getElementById("status");
            const resBox = document.getElementById("result-box");
            const btn = document.getElementById("btnEx");
            if(!val) { status.innerText = "దయచేసి లింక్ ఇవ్వండి"; status.style.color = "#ef4444"; return; }
            status.innerText = "⚡ Extracting stream link..."; status.style.color = "#0284c7";
            resBox.style.display = "none"; btn.disabled = true;
            try {
                const res = await fetch("/extract", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({url: val})
                });
                const data = await res.json();
                if(!res.ok) throw new Error(data.error || "Failed");
                document.getElementById("vtitle").innerText = data.title;
                document.getElementById("dllink").href = data.download_url;
                resBox.style.display = "block";
                status.innerText = "Ready! Click download below."; status.style.color = "#22c55e";
            } catch(err) {
                status.innerText = "Error: " + err.message; status.style.color = "#ef4444";
            } finally {
                btn.disabled = false;
            document.getElementById("tipBox").style.display = "none";
            }
        }
    </script>
</body>
</html>"""

@app.route("/")
def home():
    return HTML

@app.route("/extract", methods=["POST"])
def extract():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()
    headers = {"User-Agent": "Bilibili/7.62.0 (Android; 14; 2201117TI)", "Referer": "https://www.bilibili.com/"}
    if "b23.tv" in url:
        m = re.search(r"https?://b23\.tv/[a-zA-Z0-9]+", url)
        if m:
            try:
                r = requests.get(m.group(0), headers=headers, allow_redirects=True, timeout=8)
                url = r.url
            except Exception:
                pass
    m_bv = re.search(r"(BV[a-zA-Z0-9]+)", url)
    if not m_bv: return jsonify({"error": "Valid Bilibili URL not found"}), 400
    bvid = m_bv.group(1)
    try:
        view = requests.get(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}", headers=headers, timeout=8).json()
        cid = view.get("data", {}).get("cid")
        title = view.get("data", {}).get("title", "video")
        play = requests.get(f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&qn=64&otype=json&platform=android&fnval=0", headers=headers, timeout=8).json()
        stream_url = play.get("data", {}).get("durl", [{}])[0].get("url")
        if not stream_url: return jsonify({"error": "Stream URL extraction failed"}), 400
        dl_url = f"/download?stream={urllib.parse.quote(stream_url)}&title={urllib.parse.quote(title)}"
        return jsonify({"title": title, "download_url": dl_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/download")
def download():
    stream_url = request.args.get("stream")
    title = request.args.get("title", "video")
    if not stream_url: return "Stream URL missing", 400
    clean_title = re.sub(r"[\\/*?:\"<>|]", "", title)
    s_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Referer": "https://www.bilibili.com/", "Origin": "https://www.bilibili.com"}
    req = requests.get(stream_url, headers=s_headers, stream=True, timeout=30)
    total_length = req.headers.get("content-length")
    def generate():
        for chunk in req.iter_content(chunk_size=4*1024*1024):
            if chunk: yield chunk
    resp_headers = {"Content-Disposition": f"attachment; filename=\"{clean_title}.mp4\"", "Accept-Ranges": "bytes", "Cache-Control": "no-cache"}
    if total_length: resp_headers["Content-Length"] = total_length
    return Response(stream_with_context(generate()), content_type="application/octet-stream", headers=resp_headers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
