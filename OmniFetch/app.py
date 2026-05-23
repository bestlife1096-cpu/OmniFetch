from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
import yt_dlp
import os
import asyncio
import time
import threading
import urllib.request

app = FastAPI(title="OmniFetch Pro Enterprise Engine v3.5")

VAULT_DIR = "omnifetch_vault"
os.makedirs(VAULT_DIR, exist_ok=True)

# 🕒 1. ANTI-SLEEP HEARTBEAT CONTROLLER (Kills the Render Loading Flash)
def self_ping_heartbeat():
    time.sleep(15)
    while True:
        try:
            urllib.request.urlopen("http://127.0.0.1:10000/")
            print("[Heartbeat Core] System keep-alive status: active.")
        except Exception:
            pass
        time.sleep(120)

threading.Thread(target=self_ping_heartbeat, daemon=True).start()

# 🧹 2. SERVER FILE RECLAMATION PURGE
def auto_clear_vault(file_path: str, delay: int = 300):
    def target_clearance():
        time.sleep(delay)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[Vault Core] Automatically purged file asset: {file_path}")
        except Exception:
            pass
    threading.Thread(target=target_clearance, daemon=True).start()

# --- HIGH-PERFORMANCE DEDICATED FRONTEND DASHBOARD ---
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
            .floating-btn:hover .floating-menu { display: flex; }
        </style>
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen font-sans flex flex-col md:flex-row pb-20 md:pb-0">

        <nav class="w-full md:w-80 bg-slate-900/50 border-b md:border-b-0 md:border-r border-slate-800/80 p-6 flex flex-col justify-between backdrop-blur-xl">
            <div>
                <div class="flex items-center gap-3 mb-8 px-2">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white text-xl shadow-lg shadow-cyan-500/20">
                        <i class="fa-solid fa-bolt"></i>
                    </div>
                    <div>
                        <h1 class="text-lg font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400">OMNIFETCH PRO</h1>
                        <p class="text-[10px] text-cyan-400 font-bold tracking-widest uppercase">Engine V3.5 Core Unblocked</p>
                    </div>
                </div>

                <p class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-3 px-2">Isolated Channels</p>
                <div class="space-y-1" id="navGroup">
                    <button onclick="switchTab('youtube')" id="btn-youtube" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 text-cyan-400"><i class="fa-brands fa-youtube text-red-500 w-5"></i> YouTube Studio</button>
                    <button onclick="switchTab('tiktok')" id="btn-tiktok" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-tiktok text-pink-500 w-5"></i> TikTok Matrix</button>
                    <button onclick="switchTab('instagram')" id="btn-instagram" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-instagram text-pink-400 w-5"></i> Instagram Core</button>
                    <button onclick="switchTab('threads')" id="btn-threads" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-solid fa-threads text-white w-5"></i> Threads Channel</button>
                    <button onclick="switchTab('facebook')" id="btn-facebook" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-facebook text-blue-500 w-5"></i> Facebook Port</button>
                    <button onclick="switchTab('twitter')" id="btn-twitter" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-x-twitter text-slate-200 w-5"></i> Twitter X Module</button>
                    <button onclick="switchTab('expansion')" id="btn-expansion" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-solid fa-globe text-emerald-400 w-5"></i> Global Networks</button>
                </div>
            </div>
            
            <div class="pt-4 border-t border-slate-800 text-center space-x-2 text-[11px] text-slate-500 font-bold">
                <button onclick="openModal('privacy')" class="hover:text-cyan-400 transition-colors">Privacy Policy</button>
                <span>•</span>
                <button onclick="openModal('terms')" class="hover:text-cyan-400 transition-colors">Terms of Use</button>
            </div>
        </nav>

        <main class="flex-1 p-6 md:p-12 max-w-4xl mx-auto w-full relative">
            <div class="absolute top-0 right-1/4 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none"></div>

            <div id="panel-youtube" class="platform-panel active space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-youtube text-red-500 mr-2"></i> YouTube & YouTube Music Engine</h2>
                    <p class="text-slate-400 text-sm mt-1">Extract high-resolution MP4 videos, track extractions, or YouTube Music audio streams.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4 shadow-2xl">
                    <input type="text" id="url-youtube" placeholder="Paste YouTube or YT Music URL here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <button onclick="executeFetch('youtube', 'mp4_high')" class="bg-slate-950 border border-slate-800 hover:border-red-500/50 py-3 rounded-xl text-xs font-bold transition-all"><i class="fa-solid fa-video text-red-500 mr-1"></i> Download MP4 Video</button>
                        <button onclick="executeFetch('youtube', 'mp3')" class="bg-slate-950 border border-slate-800 hover:border-red-500/50 py-3 rounded-xl text-xs font-bold transition-all"><i class="fa-solid fa-music text-amber-400 mr-1"></i> Extract MP3 Audio</button>
                        <button onclick="executeFetch('youtube', 'music')" class="bg-gradient-to-r from-red-600 to-amber-600 text-white py-3 rounded-xl text-xs font-bold transition-all"><i class="fa-solid fa-radio mr-1"></i> YT Music Downloader</button>
                    </div>
                </div>
            </div>

            <div id="panel-tiktok" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-tiktok text-pink-500 mr-2"></i> TikTok Engine</h2>
                    <p class="text-slate-400 text-sm mt-1">Bypass tracking locks to save standard video feeds or standalone photo sliders cleanly.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-tiktok" placeholder="Paste TikTok link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-pink-500 text-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <button onclick="executeFetch('tiktok', 'standard')" class="bg-gradient-to-r from-pink-500 to-purple-600 py-3 rounded-xl text-xs font-bold"><i class="fa-solid fa-video mr-1"></i> Download TikTok Video</button>
                        <button onclick="executeFetch('tiktok', 'photo')" class="bg-slate-950 border border-slate-800 hover:border-pink-500/50 py-3 rounded-xl text-xs font-bold"><i class="fa-solid fa-images text-pink-400 mr-1"></i> Download TikTok Photos</button>
                    </div>
                </div>
            </div>

            <div id="panel-instagram" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-instagram text-pink-400 mr-2"></i> Instagram Matrix Channel</h2>
                    <p class="text-slate-400 text-sm mt-1">Extract high-definition Reels, frame videos, or individual carousel images.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-instagram" placeholder="Paste Instagram link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <button onclick="executeFetch('instagram', 'standard')" class="bg-gradient-to-r from-purple-600 via-pink-500 to-orange-500 py-3 rounded-xl text-xs font-bold"><i class="fa-solid fa-circle-down mr-1"></i> Download Instagram Video</button>
                        <button onclick="executeFetch('instagram', 'photo')" class="bg-slate-950 border border-slate-800 hover:border-pink-400/50 py-3 rounded-xl text-xs font-bold"><i class="fa-solid fa-image text-orange-400 mr-1"></i> Download Instagram Photos</button>
                    </div>
                </div>
            </div>

            <div id="panel-threads" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-solid fa-threads mr-2"></i> Threads Multi-Media Port</h2>
                    <p class="text-slate-400 text-sm mt-1">Advanced unblocker targeting standalone Threads video elements.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-threads" placeholder="Paste Threads link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('threads', 'standard')" class="w-full bg-white text-slate-950 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-play mr-1"></i> Download Threads Video</button>
                </div>
            </div>

            <div id="panel-facebook" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-facebook text-blue-500 mr-2"></i> Facebook Media Port</h2>
                    <p class="text-slate-400 text-sm mt-1">Parses public Watch segments, high-definition videos, and profile clips.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-facebook" placeholder="Paste Facebook link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('facebook', 'standard')" class="w-full bg-blue-600 hover:bg-blue-500 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-download mr-1"></i> Download Facebook Video</button>
                </div>
            </div>

            <div id="panel-twitter" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-x-twitter mr-2"></i> Twitter X Media Core</h2>
                    <p class="text-slate-400 text-sm mt-1">Decrypts timeline status configurations to extract clean media video payloads.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-twitter" placeholder="Paste Twitter X link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('twitter', 'standard')" class="w-full bg-slate-200 text-slate-950 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-arrow-down-long mr-1"></i> Download X Video</button>
                </div>
            </div>

            <div id="panel-expansion" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-solid fa-globe text-emerald-400 mr-2"></i> Global Expansion Network Pack</h2>
                    <p class="text-slate-400 text-sm mt-1">High-speed unblocking extraction channel tailored for secondary social targets.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-expansion" placeholder="Paste Pinterest, LinkedIn, Snapchat, Twitch, Reddit, Rednote links..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('expansion', 'standard')" class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 py-3.5 rounded-xl text-sm font-bold"><i class="fa-solid fa-satellite-dish mr-1"></i> Extract Global Asset Stream</button>
                    
                    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-2 text-[11px] text-slate-400 text-center font-bold">
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-pinterest text-red-500 mr-1"></i> Pinterest Video</div>
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-linkedin text-blue-400 mr-1"></i> LinkedIn Video</div>
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-snapchat text-yellow-400 mr-1"></i> Snapchat Video</div>
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-twitch text-purple-400 mr-1"></i> Twitch Video</div>
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-reddit text-orange-500 mr-1"></i> Reddit Video</div>
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-solid fa-note-sticky text-red-400 mr-1"></i> Rednote Video</div>
                    </div>
                </div>
            </div>

            <div id="monitorBox" class="mt-6 hidden bg-slate-950 border border-slate-800 rounded-2xl p-4 font-mono text-xs text-slate-400 shadow-inner">
                <div id="monitorContent" class="flex items-center gap-2">
                    <i class="fa-solid fa-circle-notch animate-spin text-cyan-400"></i> Linking extraction matrix lines...
                </div>
            </div>
        </main>

        <div class="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3 floating-btn">
            <div class="floating-menu hidden flex-col items-end gap-2 transition-all duration-300">
                <a href="https://www.facebook.com/profile.php?id=61564719578112" target="_blank" class="flex items-center gap-2 bg-blue-600/90 text-white px-4 py-2 rounded-xl text-xs font-bold shadow-lg border border-blue-500/30"><i class="fa-brands fa-facebook text-sm"></i> Tech Hub Facebook</a>
                <a href="https://www.instagram.com/bestlifetechhub" target="_blank" class="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-pink-500 text-white px-4 py-2 rounded-xl text-xs font-bold shadow-lg border border-pink-500/30"><i class="fa-brands fa-instagram text-sm"></i> Tech Hub Instagram</a>
                <a href="https://x.com/BestlifeTechHub" target="_blank" class="flex items-center gap-2 bg-slate-900/90 text-white px-4 py-2 rounded-xl text-xs font-bold shadow-lg border border-slate-700"><i class="fa-brands fa-x-twitter text-sm"></i> Twitter X Profile</a>
                <a href="https://www.tiktok.com/@bestlife1_1" target="_blank" class="flex items-center gap-2 bg-slate-950/90 text-white px-4 py-2 rounded-xl text-xs font-bold shadow-lg border border-pink-500/20"><i class="fa-brands fa-tiktok text-sm"></i> TikTok Account</a>
                <a href="https://bestlifetechhub1.blogspot.com/" target="_blank" class="flex items-center gap-2 bg-orange-600/90 text-white px-4 py-2 rounded-xl text-xs font-bold shadow-lg border border-orange-500/30"><i class="fa-solid fa-blog text-sm"></i> Tech Hub Blog Site</a>
            </div>
            <button class="w-14 h-14 rounded-full bg-gradient-to-tr from-cyan-500 to-blue-600 text-white flex items-center justify-center text-xl shadow-2xl animate-pulse border border-cyan-400/40 relative group">
                <i class="fa-solid fa-headset transition-transform group-hover:rotate-12"></i>
            </button>
        </div>

        <div id="legalModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md hidden items-center justify-center z-50 p-4">
            <div class="bg-slate-900 border border-slate-800 rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl max-h-[80vh] overflow-y-auto">
                <h3 id="modalTitle" class="text-xl font-black text-cyan-400 uppercase tracking-wide"></h3>
                <div id="modalContent" class="text-slate-400 text-xs leading-relaxed space-y-2 font-mono"></div>
                <button onclick="closeModal()" class="w-full py-2.5 bg-slate-800 hover:bg-slate-700 font-bold rounded-xl text-sm transition-all">Dismiss Policy Terms</button>
            </div>
        </div>

        <script>
            function switchTab(tabId) {
                document.querySelectorAll('.platform-panel').forEach(p => p.classList.remove('active'));
                document.getElementById('panel-' + tabId).classList.add('active');
                document.querySelectorAll('#navGroup button').forEach(b => {
                    b.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40";
                });
                const activeBtn = document.getElementById('btn-' + tabId);
                activeBtn.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 text-cyan-400";
            }

            function executeFetch(platform, mode) {
                const urlInput = document.getElementById('url-' + platform).value.trim();
                const monitorBox = document.getElementById('monitorBox');
                const monitorContent = document.getElementById('monitorContent');

                if(!urlInput) { alert('Please supply an active data link path parameter!'); return; }
                const cleanedUrl = urlInput.match(/(https?:\\/\\/[^\\s]+)/);
                if(!cleanedUrl) { alert('Invalid Web Address URL Parameter Matching Schema.'); return; }

                monitorBox.classList.remove('hidden');
                monitorContent.innerHTML = `<div class="space-y-1">
                    <p class="text-cyan-400 font-bold"><i class="fa-solid fa-fingerprint animate-pulse"></i> Handshake Spoofing Engaged [${platform.toUpperCase()}]</p>
                    <p class="text-slate-500">→ Emulating mobile client data tokens to bypass anti-bot locks...</p>
                </div>`;

                window.location.href = `/extract?url=${encodeURIComponent(cleanedUrl[0])}&mode=${mode}`;
            }

            function openModal(type) {
                const modal = document.getElementById('legalModal');
                const title = document.getElementById('modalTitle');
                const content = document.getElementById('modalContent');
                modal.classList.remove('hidden');
                modal.classList.add('flex');

                if(type === 'privacy') {
                    title.innerText = "Privacy Policy - OmniFetch Pro";
                    content.innerHTML = `<p><strong>Effective Deployment Date: May 2026</strong></p>
                    <p>OmniFetch Pro ("we," "our," "us") operates as an automated web-stream decoding utility engine. We protect data integrity completely.</p>
                    <p>1. Storage Handling: Input link protocols and raw media files are never compiled into structured data registries. Processing occurs statelessly inside secure virtual memory arrays.</p>
                    <p>2. Complete Destruction Cycle: File assets are permanently erased via automated pipeline deletion loops precisely 300 seconds post-creation.</p>
                    <p>3. Compliance: This platform does not request, hook, or track local tracking profiles or telemetry identifiers, meeting global App Store distribution laws.</p>`;
                } else {
                    title.innerText = "Terms of Use - OmniFetch Pro";
                    content.innerHTML = `<p><strong>Terms and Conditions Agreement Matrix</strong></p>
                    <p>By executing actions inside OmniFetch Pro, you bind to the legal parameters below:</p>
                    <p>1. Scope of Use: This system operates purely as an internet data transceiver framework. Users hold full and exclusive accountability for assets processed via their sessions.</p>
                    <p>2. Property Boundaries: All rights relating to system handshake formatting layouts belong strictly to Bestlife Tech Hub.</p>`;
                }
            }

            function closeModal() {
                const modal = document.getElementById('legalModal');
                modal.classList.remove('flex');
                modal.classList.add('hidden');
            }
        </script>
    </body>
    </html>
    """

# --- HARDENED ANTI-BLOCK EXTRACTION PIPELINE MOTOR ---
@app.get("/extract")
async def process_extraction_pipeline(url: str = Query(...), mode: str = Query(...)):
    # Advanced client parameters emulating native iOS and Android handshakes
    base_opts = {
        'outtmpl': f'{VAULT_DIR}/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        'referer': 'https://www.google.com/',
        'extractor_args': {
            # Forces YouTube to see a combination of a signed-in native android application and standard safari browser signatures
            'youtube': ['player_client=android,web', 'skip=dash,hls'],
            'instagram': ['skip_api_user=true']
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    # Format conditioning routes
    if mode == 'mp3' or mode == 'music':
        base_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    elif mode == 'photo':
        # Forces engine to capture primary graphical storage instead of video streams
        base_opts.update({'format': 'bestimage/best/best'})
    else:
        # Standard video streaming pipeline tracking
        base_opts.update({'format': 'best[ext=mp4]/best'})

    try:
        loop = asyncio.get_event_loop()
        extractor = yt_dlp.YoutubeDL(base_opts)
        metadata = await loop.run_in_executor(None, lambda: extractor.extract_info(url, download=True))
        target_file = extractor.prepare_filename(metadata)

        # Fallback names fixing audio tracks extensions matching signatures
        if (mode == 'mp3' or mode == 'music') and not target_file.endswith('.mp3'):
            fallback_base = target_file.rsplit('.', 1)[0] + '.mp3'
            if os.path.exists(fallback_base):
                target_file = fallback_base

        auto_clear_vault(target_file, delay=300)

        return FileResponse(
            path=target_file,
            media_type='application/octet-stream',
            filename=os.path.basename(target_file)
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Engine bypass blocked by destination server. Details: {str(err)}")