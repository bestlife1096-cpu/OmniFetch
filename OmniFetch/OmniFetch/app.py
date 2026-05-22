from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
import yt_dlp
import os
import asyncio
import time
import threading
import urllib.request

app = FastAPI(title="OmniFetch Pro Master Engine v2.5")

VAULT_DIR = "omnifetch_vault"
os.makedirs(VAULT_DIR, exist_ok=True)

# 🕒 1. SYSTEM KEEP-ALIVE COOLDOWN BYPASS (No More Loading/504 Screens)
def self_ping_heartbeat():
    """Pings the server every 5 minutes so Render never goes to sleep."""
    time.sleep(30) # Allow system startup
    while True:
        try:
            # Replaces with local loopback to keep engine alive internally
            urllib.request.urlopen("http://127.0.0.1:10000/")
            print("[Heartbeat] Server pinged successfully. Standing by active.")
        except Exception:
            pass
        time.sleep(300) # Ping every 5 minutes

threading.Thread(target=self_ping_heartbeat, daemon=True).start()

# 🧹 2. AUTOMATIC VAULT PURGE ROUTINE
def auto_clear_vault(file_path: str, delay: int = 600):
    """Safely removes downloaded files after 10 minutes to protect disk storage."""
    def target_clearance():
        time.sleep(delay)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[Vault Status] Purged asset safely: {file_path}")
        except Exception as e:
            print(f"[Vault Warning] Clean loop bypass: {e}")
    threading.Thread(target=target_clearance, daemon=True).start()

# --- GLOBAL FRONTEND MULTI-TAB INTERFACE ---
@app.get("/", response_class=HTMLResponse)
async def production_dashboard():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OmniFetch Pro Control Room</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            .platform-panel { display: none; }
            .platform-panel.active { display: block; }
            ::-webkit-scrollbar { width: 6px; }
            ::-webkit-scrollbar-track { background: #020617; }
            ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 10px; }
        </style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen font-sans flex flex-col md:flex-row">

        <nav class="w-full md:w-80 bg-slate-900/50 border-b md:border-b-0 md:border-r border-slate-800/80 p-6 flex flex-col justify-between backdrop-blur-xl">
            <div>
                <div class="flex items-center gap-3 mb-8 px-2">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white text-xl shadow-lg shadow-cyan-500/20">
                        <i class="fa-solid fa-cloud-arrow-down"></i>
                    </div>
                    <div>
                        <h1 class="text-lg font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400">OMNIFETCH PRO</h1>
                        <p class="text-[10px] text-cyan-400 font-bold tracking-widest uppercase">Engine V2.5 Anti-Block</p>
                    </div>
                </div>

                <p class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-3 px-2">Channels Ecosystem</p>
                <div class="space-y-1" id="navGroup">
                    <button onclick="switchTab('youtube')" id="btn-youtube" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 text-cyan-400"><i class="fa-brands fa-youtube text-red-500 w-5"></i> YouTube Studio</button>
                    <button onclick="switchTab('tiktok')" id="btn-tiktok" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-tiktok text-pink-500 w-5"></i> TikTok Module</button>
                    <button onclick="switchTab('threads')" id="btn-threads" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-solid fa-threads text-white w-5"></i> Threads Core</button>
                    <button onclick="switchTab('instagram')" id="btn-instagram" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-instagram text-pink-400 w-5"></i> Instagram Core</button>
                    <button onclick="switchTab('facebook')" id="btn-facebook" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-facebook text-blue-500 w-5"></i> Facebook Client</button>
                    <button onclick="switchTab('twitter')" id="btn-twitter" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-x-twitter text-slate-200 w-5"></i> Twitter X Engine</button>
                    <button onclick="switchTab('expansion')" id="btn-expansion" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-solid fa-globe text-emerald-400 w-5"></i> Expanded Networks</button>
                </div>
            </div>
            <div class="hidden md:block pt-6 border-t border-slate-900 text-center">
                <p class="text-[10px] text-slate-600">OmniFetch Pro Multi-Platform Client &copy; 2026</p>
            </div>
        </nav>

        <main class="flex-1 p-6 md:p-12 max-w-4xl mx-auto w-full relative">
            <div class="absolute top-0 right-1/4 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none"></div>

            <div id="panel-youtube" class="platform-panel active space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-youtube text-red-500 mr-2"></i> YouTube & YT Music Downloader</h2>
                    <p class="text-slate-400 text-sm mt-1">Extract high-speed MP4 videos, track extractions, or YouTube Studio Music.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-xl space-y-4">
                    <input type="text" id="url-youtube" placeholder="Paste YouTube link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <button onclick="executeFetch('youtube', 'mp4_high')" class="bg-slate-950 border border-slate-800 hover:border-red-500/50 py-3 rounded-xl text-xs font-bold transition-all"><i class="fa-solid fa-video text-red-500 mr-1"></i> Download MP4 Video</button>
                        <button onclick="executeFetch('youtube', 'mp3')" class="bg-slate-950 border border-slate-800 hover:border-red-500/50 py-3 rounded-xl text-xs font-bold transition-all"><i class="fa-solid fa-music text-amber-400 mr-1"></i> Extract MP3 Audio</button>
                        <button onclick="executeFetch('youtube', 'music')" class="bg-gradient-to-r from-red-600 to-amber-600 text-white py-3 rounded-xl text-xs font-bold transition-all"><i class="fa-solid fa-radio mr-1"></i> YouTube Music Downloader</button>
                    </div>
                </div>
            </div>

            <div id="panel-tiktok" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-tiktok text-pink-500 mr-2"></i> TikTok Video Downloader</h2>
                    <p class="text-slate-400 text-sm mt-1">Bypasses TikTok download security filters automatically.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-xl space-y-4">
                    <input type="text" id="url-tiktok" placeholder="Paste TikTok URL here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('tiktok', 'standard')" class="w-full bg-gradient-to-r from-pink-500 to-cyan-500 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-bolt mr-1"></i> Download TikTok Video</button>
                </div>
            </div>

            <div id="panel-threads" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-solid fa-threads mr-2"></i> Threads Video Downloader</h2>
                    <p class="text-slate-400 text-sm mt-1">Custom data stream unblocker for Threads video assets.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-xl space-y-4">
                    <input type="text" id="url-threads" placeholder="Paste Threads link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('threads', 'standard')" class="w-full bg-white text-slate-950 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-play mr-1"></i> Download Threads Video</button>
                </div>
            </div>

            <div id="panel-instagram" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-instagram text-pink-400 mr-2"></i> Instagram Video Downloader</h2>
                    <p class="text-slate-400 text-sm mt-1">Extract high-definition Reels and layout frames.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-xl space-y-4">
                    <input type="text" id="url-instagram" placeholder="Paste Instagram Link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('instagram', 'standard')" class="w-full bg-gradient-to-r from-purple-600 via-pink-500 to-orange-500 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-circle-down mr-1"></i> Download Instagram Video</button>
                </div>
            </div>

            <div id="panel-facebook" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-facebook text-blue-500 mr-2"></i> Facebook Video Downloader</h2>
                    <p class="text-slate-400 text-sm mt-1">Extract public feed videos, shorts, and system stories.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-xl space-y-4">
                    <input type="text" id="url-facebook" placeholder="Paste Facebook link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('facebook', 'standard')" class="w-full bg-blue-600 hover:bg-blue-500 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-download mr-1"></i> Download Facebook Video</button>
                </div>
            </div>

            <div id="panel-twitter" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-x-twitter mr-2"></i> Twitter X Video Downloader</h2>
                    <p class="text-slate-400 text-sm mt-1">Converts timeline statuses and text post clips cleanly.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-xl space-y-4">
                    <input type="text" id="url-twitter" placeholder="Paste Twitter X link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('twitter', 'standard')" class="w-full bg-slate-200 text-slate-950 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-arrow-down-long mr-1"></i> Download Twitter X Video</button>
                </div>
            </div>

            <div id="panel-expansion" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-solid fa-globe text-emerald-400 mr-2"></i> Expansion Pack Scraper Engine</h2>
                    <p class="text-slate-400 text-sm mt-1">Multi-threaded download channels configured for world platform expansions.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 backdrop-blur-xl space-y-4">
                    <input type="text" id="url-expansion" placeholder="Paste Pinterest, LinkedIn, Snapchat, Twitch, Reddit, Rednote links..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('expansion', 'standard')" class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-satellite-dish mr-1"></i> Execute High-Speed Extraction</button>
                    
                    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-2 text-[11px] text-slate-400 text-center font-bold">
                        <div class="p-3 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-pinterest text-red-500 mr-1"></i> Pinterest Video</div>
                        <div class="p-3 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-linkedin text-blue-400 mr-1"></i> LinkedIn Video</div>
                        <div class="p-3 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-snapchat text-yellow-400 mr-1"></i> Snapchat Video</div>
                        <div class="p-3 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-twitch text-purple-400 mr-1"></i> Twitch Video</div>
                        <div class="p-3 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-reddit text-orange-500 mr-1"></i> Reddit Video</div>
                        <div class="p-3 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-solid fa-note-sticky text-red-400 mr-1"></i> Rednote Video</div>
                    </div>
                </div>
            </div>

            <div id="monitorBox" class="mt-6 hidden bg-slate-950 border border-slate-800 rounded-2xl p-4 font-mono text-xs text-slate-400 shadow-inner">
                <div id="monitorContent" class="flex items-center gap-2">
                    <i class="fa-solid fa-satellite animate-spin text-cyan-400"></i> Linking satellite array tunnels...
                </div>
            </div>
        </main>

        <script>
            function switchTab(tabId) {
                document.querySelectorAll('.platform-panel').forEach(p => p.classList.remove('active'));
                document.getElementById('panel-' + tabId).classList.add('active');
                
                document.querySelectorAll('#navGroup button').forEach(b => {
                    b.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left text-slate-400 hover:bg-slate-800/40";
                });
                
                const activeBtn = document.getElementById('btn-' + tabId);
                if(tabId === 'youtube') activeBtn.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 text-cyan-400";
                else if(tabId === 'tiktok') activeBtn.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left bg-gradient-to-r from-pink-500/10 to-purple-500/10 border border-pink-500/30 text-pink-400";
                else if(tabId === 'threads') activeBtn.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left bg-slate-800 border border-slate-700 text-white";
                else if(tabId === 'instagram') activeBtn.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left bg-gradient-to-r from-purple-500/10 to-orange-500/10 border border-pink-500/30 text-pink-400";
                else if(tabId === 'facebook') activeBtn.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left bg-blue-500/10 border border-blue-500/30 text-blue-400";
                else if(tabId === 'twitter') activeBtn.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left bg-slate-800 border border-slate-700 text-slate-200";
                else activeBtn.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm transition-all text-left bg-emerald-500/10 border border-emerald-500/30 text-emerald-400";
            }

            function executeFetch(platform, mode) {
                const urlInput = document.getElementById('url-' + platform).value.trim();
                const monitorBox = document.getElementById('monitorBox');
                const monitorContent = document.getElementById('monitorContent');

                if(!urlInput) {
                    alert('Please input a valid web asset link first!');
                    return;
                }

                const cleanedUrl = urlInput.match(/(https?:\\/\\/[^\\s]+)/);
                if(!cleanedUrl) {
                    alert('Invalid Web Address Protocol Schema.');
                    return;
                }

                monitorBox.classList.remove('hidden');
                monitorContent.innerHTML = `<div class="space-y-1">
                    <p class="text-cyan-400 font-bold"><i class="fa-solid fa-shield-cat animate-pulse"></i> Anti-Block Core Activated [${platform.toUpperCase()}]</p>
                    <p class="text-slate-500">→ Syncing browser spoof headers to prevent server blocking...</p>
                </div>`;

                window.location.href = `/extract?url=${encodeURIComponent(cleanedUrl[0])}&mode=${mode}`;

                setTimeout(() => {
                    monitorContent.innerHTML = `<p class="text-emerald-400 font-bold"><i class="fa-solid fa-truck-ramp-box"></i> Transmission packet compiled! Sending file payload to your device storage...</p>`;
                }, 5000);
            }
        </script>
    </body>
    </html>
    """

# --- ANTI-BLOCK EXTRACTION PIPELINE MECHANISM ---
@app.get("/extract")
async def process_extraction_pipeline(url: str = Query(...), mode: str = Query(...)):
    # Advanced data configurations to unblock YouTube, Pinterest, and Threads data leaks
    base_opts = {
        'outtmpl': f'{VAULT_DIR}/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        'extractor_args': {
            'youtube': ['player_client=android,web'],
            'instagram': ['skip_api_user=true']
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,video/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate',
            'Referer': 'https://www.google.com/'
        }
    }

    # Format routing logic switches
    if mode == 'mp3' or mode == 'music':
        base_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    else:
        # Pulls pre-merged single video streams to prevent cloud compilation crashes
        base_opts.update({'format': 'best[ext=mp4]/best'})

    try:
        loop = asyncio.get_event_loop()
        extractor = yt_dlp.YoutubeDL(base_opts)
        
        metadata = await loop.run_in_executor(
            None, lambda: extractor.extract_info(url, download=True)
        )
        target_file = extractor.prepare_filename(metadata)

        if (mode == 'mp3' or mode == 'music') and not target_file.endswith('.mp3'):
            fallback_base = target_file.rsplit('.', 1)[0] + '.mp3'
            if os.path.exists(fallback_base):
                target_file = fallback_base

        auto_clear_vault(target_file, delay=600)

        return FileResponse(
            path=target_file,
            media_type='application/octet-stream',
            filename=os.path.basename(target_file)
        )

    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Extraction failed: Platform firewall active. {str(err)}")