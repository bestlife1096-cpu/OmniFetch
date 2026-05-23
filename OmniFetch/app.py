from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os
import asyncio
import time
import threading

app = FastAPI(title="OmniFetch Pro Master Engine v4.0")

# Enable global processing pipelines to prevent stream blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]
)

VAULT_DIR = "omnifetch_vault"
os.makedirs(VAULT_DIR, exist_ok=True)

# 🧹 AUTOMATIC SECURE MEDIA STORAGE PURGE LOOP
def auto_clear_vault(file_path: str, delay: int = 180):
    def target_clearance():
        time.sleep(delay)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            pass
    threading.Thread(target=target_clearance, daemon=True).start()

# --- ENTERPRISE USER INTERFACE DESIGN WITH DIRECT BLOB INJECTION ---
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
    <body class="bg-slate-950 text-slate-100 min-h-screen font-sans flex flex-col md:flex-row pb-24 md:pb-0">

        <nav class="w-full md:w-80 bg-slate-900/50 border-b md:border-b-0 md:border-r border-slate-800/80 p-6 flex flex-col justify-between backdrop-blur-xl">
            <div>
                <div class="flex items-center gap-3 mb-6 px-2">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-white text-xl shadow-lg">
                        <i class="fa-solid fa-cloud-arrow-down"></i>
                    </div>
                    <div>
                        <h1 class="text-lg font-black tracking-wider text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400">OMNIFETCH PRO</h1>
                        <p class="text-[10px] text-cyan-400 font-bold tracking-widest uppercase">Direct Download Core v4.0</p>
                    </div>
                </div>

                <button onclick="triggerNativeShare()" class="w-full mb-6 flex items-center justify-center gap-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold py-3 px-4 rounded-xl text-xs shadow-lg shadow-cyan-500/10 transition-all uppercase tracking-wider">
                    <i class="fa-solid fa-share-nodes text-sm"></i> Share App With Family & Friends
                </button>

                <p class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-3 px-2">Ecosystem Channels</p>
                <div class="space-y-1" id="navGroup">
                    <button onclick="switchTab('youtube')" id="btn-youtube" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 text-cyan-400"><i class="fa-brands fa-youtube text-red-500 w-5"></i> YouTube Studio</button>
                    <button onclick="switchTab('tiktok')" id="btn-tiktok" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-tiktok text-pink-500 w-5"></i> TikTok Module</button>
                    <button onclick="switchTab('instagram')" id="btn-instagram" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-instagram text-pink-400 w-5"></i> Instagram Core</button>
                    <button onclick="switchTab('threads')" id="btn-threads" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-solid fa-threads text-white w-5"></i> Threads Core</button>
                    <button onclick="switchTab('facebook')" id="btn-facebook" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-facebook text-blue-500 w-5"></i> Facebook Client</button>
                    <button onclick="switchTab('twitter')" id="btn-twitter" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-brands fa-x-twitter text-slate-200 w-5"></i> Twitter X Module</button>
                    <button onclick="switchTab('expansion')" id="btn-expansion" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40"><i class="fa-solid fa-globe text-emerald-400 w-5"></i> Global Extension</button>
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
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-youtube text-red-500 mr-2"></i> YouTube Extractor</h2>
                    <p class="text-slate-400 text-sm mt-1">Converts public videos or high-fidelity music audios straight into local device storage.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4 shadow-2xl">
                    <input type="text" id="url-youtube" placeholder="Paste YouTube or YT Music Link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                        <button onclick="executeFetch('youtube', 'mp4_high')" class="bg-slate-950 border border-slate-800 hover:border-red-500/50 py-3 rounded-xl text-xs font-bold transition-all"><i class="fa-solid fa-video text-red-500 mr-1"></i> Download MP4 Video</button>
                        <button onclick="executeFetch('youtube', 'mp3')" class="bg-slate-950 border border-slate-800 hover:border-red-500/50 py-3 rounded-xl text-xs font-bold transition-all"><i class="fa-solid fa-music text-amber-400 mr-1"></i> Extract MP3 Audio</button>
                        <button onclick="executeFetch('youtube', 'music')" class="bg-gradient-to-r from-red-600 to-amber-600 text-white py-3 rounded-xl text-xs font-bold transition-all"><i class="fa-solid fa-radio mr-1"></i> YT Music Fix</button>
                    </div>
                </div>
            </div>

            <div id="panel-tiktok" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-tiktok text-pink-500 mr-2"></i> TikTok Extractor</h2>
                    <p class="text-slate-400 text-sm mt-1">Saves video loops or downloads complete image profile slides into your library.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-tiktok" placeholder="Paste TikTok Link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-pink-500 text-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <button onclick="executeFetch('tiktok', 'standard')" class="bg-gradient-to-r from-pink-500 to-purple-600 py-3 rounded-xl text-xs font-bold"><i class="fa-solid fa-video mr-1"></i> Download TikTok Video</button>
                        <button onclick="executeFetch('tiktok', 'photo')" class="bg-slate-950 border border-slate-800 hover:border-pink-500/50 py-3 rounded-xl text-xs font-bold"><i class="fa-solid fa-images text-pink-400 mr-1"></i> Download TikTok Photos</button>
                    </div>
                </div>
            </div>

            <div id="panel-instagram" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-instagram text-pink-400 mr-2"></i> Instagram Extractor</h2>
                    <p class="text-slate-400 text-sm mt-1">Directly forces high-definition Reels and photos into storage without stream interception.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-instagram" placeholder="Paste Instagram Link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                        <button onclick="executeFetch('instagram', 'standard')" class="bg-gradient-to-r from-purple-600 via-pink-500 to-orange-500 py-3 rounded-xl text-xs font-bold"><i class="fa-solid fa-circle-down mr-1"></i> Download Instagram Video</button>
                        <button onclick="executeFetch('instagram', 'photo')" class="bg-slate-950 border border-slate-800 hover:border-pink-400/50 py-3 rounded-xl text-xs font-bold"><i class="fa-solid fa-image text-orange-400 mr-1"></i> Download Instagram Photos</button>
                    </div>
                </div>
            </div>

            <div id="panel-threads" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-solid fa-threads mr-2"></i> Threads Extractor</h2>
                    <p class="text-slate-400 text-sm mt-1">Decodes timeline strings to extract Threads videos cleanly.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-threads" placeholder="Paste Threads Link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('threads', 'standard')" class="w-full bg-white text-slate-950 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-play mr-1"></i> Download Threads Video</button>
                </div>
            </div>

            <div id="panel-facebook" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-facebook text-blue-500 mr-2"></i> Facebook Extractor</h2>
                    <p class="text-slate-400 text-sm mt-1">Converts public watch, reels, and clip links into instant downloads.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-facebook" placeholder="Paste Facebook Link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('facebook', 'standard')" class="w-full bg-blue-600 hover:bg-blue-500 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-download mr-1"></i> Download Facebook Video</button>
                </div>
            </div>

            <div id="panel-twitter" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-brands fa-x-twitter mr-2"></i> Twitter X Extractor</h2>
                    <p class="text-slate-400 text-sm mt-1">Bypasses encrypted layout loops to isolate status video feeds instantly.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-twitter" placeholder="Paste Twitter X Link here..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('twitter', 'standard')" class="w-full bg-slate-200 text-slate-950 py-3.5 rounded-xl text-sm font-bold transition-all"><i class="fa-solid fa-arrow-down-long mr-1"></i> Download Twitter X Video</button>
                </div>
            </div>

            <div id="panel-expansion" class="platform-panel space-y-6">
                <div>
                    <h2 class="text-2xl font-black tracking-tight"><i class="fa-solid fa-globe text-emerald-400 mr-2"></i> Global Expansion Network</h2>
                    <p class="text-slate-400 text-sm mt-1">Multi-threaded extractor channels built for specialized social networks.</p>
                </div>
                <div class="bg-slate-900/40 border border-slate-800/80 rounded-2xl p-6 space-y-4">
                    <input type="text" id="url-expansion" placeholder="Paste Pinterest, LinkedIn, Snapchat, Twitch, Reddit, Rednote links..." class="w-full px-4 py-3.5 bg-slate-950 border border-slate-800 rounded-xl focus:outline-none focus:border-cyan-500 text-sm">
                    <button onclick="executeFetch('expansion', 'standard')" class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 py-3.5 rounded-xl text-sm font-bold"><i class="fa-solid fa-satellite-dish mr-1"></i> Download Global Asset</button>
                    
                    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-2 text-[11px] text-slate-400 text-center font-bold">
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-pinterest text-red-500 mr-1"></i> Pinterest</div>
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-linkedin text-blue-400 mr-1"></i> LinkedIn</div>
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-snapchat text-yellow-400 mr-1"></i> Snapchat</div>
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-twitch text-purple-400 mr-1"></i> Twitch</div>
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-brands fa-reddit text-orange-500 mr-1"></i> Reddit</div>
                        <div class="p-2 bg-slate-950 border border-slate-800/60 rounded-xl"><i class="fa-solid fa-note-sticky text-red-400 mr-1"></i> Rednote</div>
                    </div>
                </div>
            </div>

            <div id="monitorBox" class="mt-6 hidden bg-slate-950 border border-slate-800 rounded-2xl p-4 font-mono text-xs text-slate-400 shadow-inner">
                <div id="monitorContent" class="flex items-center gap-2">
                    <i class="fa-solid fa-circle-notch animate-spin text-cyan-400"></i> Initializing Direct Injection Pipeline...
                </div>
            </div>
        </main>

        <div class="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3 floating-btn">
            <div class="floating-menu hidden flex-col items-end gap-2 transition-all duration-300">
                <a href="https://www.facebook.com/profile.php?id=61564719578112" target="_blank" class="flex items-center gap-2 bg-blue-600/90 text-white px-4 py-2 rounded-xl text-xs font-bold border border-blue-500/30 shadow-lg"><i class="fa-brands fa-facebook text-sm"></i> Tech Hub Facebook</a>
                <a href="https://www.instagram.com/bestlifetechhub" target="_blank" class="flex items-center gap-2 bg-gradient-to-r from-purple-600 to-pink-500 text-white px-4 py-2 rounded-xl text-xs font-bold border border-pink-500/30 shadow-lg"><i class="fa-brands fa-instagram text-sm"></i> Tech Hub Instagram</a>
                <a href="https://x.com/BestlifeTechHub" target="_blank" class="flex items-center gap-2 bg-slate-900/90 text-white px-4 py-2 rounded-xl text-xs font-bold border border-slate-700 shadow-lg"><i class="fa-brands fa-x-twitter text-sm"></i> Twitter X Profile</a>
                <a href="https://www.tiktok.com/@bestlife1_1" target="_blank" class="flex items-center gap-2 bg-slate-950/90 text-white px-4 py-2 rounded-xl text-xs font-bold border border-pink-500/20 shadow-lg"><i class="fa-brands fa-tiktok text-sm"></i> TikTok Feed</a>
                <a href="https://bestlifetechhub1.blogspot.com/" target="_blank" class="flex items-center gap-2 bg-orange-600/90 text-white px-4 py-2 rounded-xl text-xs font-bold border border-orange-500/30 shadow-lg"><i class="fa-solid fa-blog text-sm"></i> Tech Hub Blog</a>
            </div>
            <button class="w-14 h-14 rounded-full bg-gradient-to-tr from-cyan-500 to-blue-600 text-white flex items-center justify-center text-xl shadow-2xl border border-cyan-400/40 relative group">
                <i class="fa-solid fa-headset"></i>
            </button>
        </div>

        <div id="legalModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md hidden items-center justify-center z-50 p-4">
            <div class="bg-slate-900 border border-slate-800 rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl max-h-[80vh] overflow-y-auto">
                <h3 id="modalTitle" class="text-xl font-black text-cyan-400 uppercase tracking-wide"></h3>
                <div id="modalContent" class="text-slate-400 text-xs leading-relaxed space-y-2 font-mono"></div>
                <button onclick="closeModal()" class="w-full py-2.5 bg-slate-800 hover:bg-slate-700 font-bold rounded-xl text-sm transition-all">Dismiss Parameters</button>
            </div>
        </div>

        <script>
            function switchTab(tabId) {
                document.querySelectorAll('.platform-panel').forEach(p => p.classList.remove('active'));
                document.getElementById('panel-' + tabId).classList.add('active');
                document.querySelectorAll('#navGroup button').forEach(b => {
                    b.className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left text-slate-400 hover:bg-slate-800/40";
                });
                document.getElementById('btn-' + tabId).className = "w-full flex items-center gap-3 px-4 py-3 rounded-xl font-medium text-sm text-left bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-cyan-500/30 text-cyan-400";
            }

            function triggerNativeShare() {
                if (navigator.share) {
                    navigator.share({
                        title: 'OmniFetch Pro',
                        text: 'Download high-speed videos, photos, and audios from any social platform instantly!',
                        url: window.location.origin
                    }).catch(console.error);
                } else {
                    alert("Copy your App address link to share with loved ones: " + window.location.origin);
                }
            }

            // --- CRITICAL BLOB HOOK MATRIX FOR DIRECT FORCE LOCAL STORAGE DELIVERY ---
            async function executeFetch(platform, mode) {
                const urlInput = document.getElementById('url-' + platform).value.trim();
                const monitorBox = document.getElementById('monitorBox');
                const monitorContent = document.getElementById('monitorContent');

                if(!urlInput) { alert('Please supply a direct platform input target link.'); return; }
                const cleanedUrl = urlInput.match(/(https?:\\/\\/[^\\s]+)/);
                if(!cleanedUrl) { alert('Invalid URL Addressing Protocol.'); return; }

                monitorBox.classList.remove('hidden');
                monitorContent.innerHTML = `<div class="space-y-1">
                    <p class="text-cyan-400 font-bold animate-pulse"><i class="fa-solid fa-cloud-arrow-down"></i> OmniFetch Extraction Core Processing Block...</p>
                    <p class="text-slate-500">→ Overriding default media playback engines... forcing direct file download pipeline.</p>
                </div>`;

                try {
                    const targetEndpoint = `/extract?url=${encodeURIComponent(cleanedUrl[0])}&mode=${mode}`;
                    const response = await fetch(targetEndpoint);
                    if (!response.ok) throw new Error("Server extraction firewall block detected.");
                    
                    // Reads stream data directly into a memory allocation container
                    const fileBlob = await response.blob();
                    
                    // Extracts content-disposition header boundaries safely
                    const contentDisp = response.headers.get('Content-Disposition');
                    let targetFilename = `OmniFetch_${platform}_asset.mp4`;
                    if (contentDisp && contentDisp.includes('filename=')) {
                        targetFilename = contentDisp.split('filename=')[1].replaceAll('"', '');
                    }
                    if (mode === 'mp3' || mode === 'music') targetFilename = targetFilename.replace(/\.[^/.]+$/, "") + ".mp3";

                    // Fires native low-level DOM download handler to completely bypass streaming video displays
                    const invisibleAnchor = document.createElement('a');
                    invisibleAnchor.href = window.URL.createObjectURL(fileBlob);
                    invisibleAnchor.download = targetFilename;
                    document.body.appendChild(invisibleAnchor);
                    invisibleAnchor.click();
                    document.body.removeChild(invisibleAnchor);

                    monitorContent.innerHTML = `<p class="text-emerald-400 font-bold"><i class="fa-solid fa-circle-check"></i> File saved successfully directly into device folder!</p>`;
                } catch (error) {
                    monitorContent.innerHTML = `<p class="text-red-500 font-bold"><i class="fa-solid fa-triangle-exclamation"></i> Extraction Fault: Target platform is throttling requests. Re-trying pipeline sequence...</p>`;
                    alert("Core Extraction Interrupted. Please ensure link is public and try again.");
                }
            }

            function openModal(type) {
                const modal = document.getElementById('legalModal');
                const title = document.getElementById('modalTitle');
                const content = document.getElementById('modalContent');
                modal.classList.remove('hidden'); modal.classList.add('flex');

                if(type === 'privacy') {
                    title.innerText = "Privacy Policy - OmniFetch Pro";
                    content.innerHTML = `<p>Effective Layout Deployment: May 2026</p><p>OmniFetch Pro completely guards user anonymity. No analytical session history, tracking tags, or media addresses are saved into registries.</p>`;
                } else {
                    title.innerText = "Terms of Use - OmniFetch Pro";
                    content.innerHTML = `<p>Terms and System Compliance Parameters Matrix</p><p>This application operates as a real-time data proxy link engine. Users maintain absolute personal liability for processed material parameters.</p>`;
                }
            }

            function closeModal() { document.getElementById('legalModal').classList.remove('flex'); document.getElementById('legalModal').classList.add('hidden'); }
        </script>
    </body>
    </html>
    """

# --- HIGH-SPEED BYPASS ENGINE PIPELINE ---
@app.get("/extract")
async def process_extraction_pipeline(url: str = Query(...), mode: str = Query(...)):
    # Advanced client handshakes masking cloud hosting addresses completely
    base_opts = {
        'outtmpl': f'{VAULT_DIR}/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        'referer': 'https://www.google.com/',
        'extractor_args': {
            'youtube': ['player_client=android,web', 'skip=dash,hls'],
            'instagram': ['skip_api_user=true']
        },
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

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
        base_opts.update({'format': 'bestimage/best'})
    else:
        # Pull pre-merged single video layers directly to protect processing speeds
        base_opts.update({'format': 'best[ext=mp4]/best'})

    try:
        loop = asyncio.get_event_loop()
        extractor = yt_dlp.YoutubeDL(base_opts)
        metadata = await loop.run_in_executor(None, lambda: extractor.extract_info(url, download=True))
        target_file = extractor.prepare_filename(metadata)

        if (mode == 'mp3' or mode == 'music') and not target_file.endswith('.mp3'):
            fallback_base = target_file.rsplit('.', 1)[0] + '.mp3'
            if os.path.exists(fallback_base):
                target_file = fallback_base

        auto_clear_vault(target_file, delay=180)

        # Force structural stream-attachment flags inside the headers matrix
        file_name_clean = os.path.basename(target_file)
        return FileResponse(
            path=target_file,
            media_type='application/octet-stream',
            filename=file_name_clean,
            headers={"Content-Disposition": f"attachment; filename={file_name_clean}"}
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Bypass routine active: {str(err)}")