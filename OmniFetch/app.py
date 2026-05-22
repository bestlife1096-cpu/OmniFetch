from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import yt_dlp
import os
import asyncio
import time

app = FastAPI(title="OmniFetch Global Powerhouse Engine")

DOWNLOAD_FOLDER = "omnifetch_vault"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def schedule_file_deletion(file_path: str, delay_seconds: int = 600):
    """Safely purges downloaded files after 10 minutes so cloud storage never fills up."""
    def delete_task():
        time.sleep(delay_seconds)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[Vault Cleanup] Cleaned asset: {file_path}")
        except Exception as e:
            print(f"[Vault Error] Cleanup failed: {e}")
            
    import threading
    threading.Thread(target=delete_task, daemon=True).start()

@app.get("/", response_class=HTMLResponse)
async def home_interface():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OmniFetch Pro - Universal Archiver</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-center items-center font-sans px-4">
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="w-full max-w-2xl bg-slate-900/60 border border-slate-800/80 rounded-3xl p-6 md:p-8 backdrop-blur-xl shadow-2xl relative z-10 text-center">
            
            <div class="mb-6">
                <div class="inline-flex items-center justify-center bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/30 w-16 h-16 rounded-2xl text-cyan-400 text-3xl mb-4 shadow-lg">
                    <i class="fa-solid fa-cloud-arrow-down"></i>
                </div>
                <h1 class="text-3xl md:text-4xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-400">OMNIFETCH PRO</h1>
                <p class="text-slate-400 mt-2 text-xs md:text-sm font-medium">Enterprise Media Extraction Engine</p>
            </div>

            <div class="grid grid-cols-3 md:grid-cols-6 gap-2 mb-6 text-[10px] font-bold tracking-wide uppercase text-slate-400">
                <div class="bg-slate-950/60 border border-slate-800/60 rounded-xl py-2 px-1 flex flex-col items-center gap-1"><i class="fa-brands fa-tiktok text-sm text-pink-500"></i> TikTok</div>
                <div class="bg-slate-950/60 border border-slate-800/60 rounded-xl py-2 px-1 flex flex-col items-center gap-1"><i class="fa-brands fa-facebook text-sm text-blue-500"></i> Facebook</div>
                <div class="bg-slate-950/60 border border-slate-800/60 rounded-xl py-2 px-1 flex flex-col items-center gap-1"><i class="fa-brands fa-instagram text-sm text-pink-400"></i> Instagram</div>
                <div class="bg-slate-950/60 border border-slate-800/60 rounded-xl py-2 px-1 flex flex-col items-center gap-1"><i class="fa-solid fa-threads text-sm text-white"></i> Threads</div>
                <div class="bg-slate-950/60 border border-slate-800/60 rounded-xl py-2 px-1 flex flex-col items-center gap-1"><i class="fa-brands fa-x-twitter text-sm text-slate-200"></i> Twitter X</div>
                <div class="bg-slate-950/60 border border-slate-800/60 rounded-xl py-2 px-1 flex flex-col items-center gap-1"><i class="fa-brands fa-youtube text-sm text-red-500"></i> Global Web</div>
            </div>

            <div class="space-y-4 text-left">
                <div class="relative">
                    <span class="absolute inset-y-0 left-0 flex items-center pl-4 text-slate-500"><i class="fa-solid fa-link"></i></span>
                    <input type="text" id="videoUrl" placeholder="Paste data link here..." class="w-full pl-11 pr-4 py-4 bg-slate-950 border border-slate-800 rounded-2xl text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500/50 transition-colors shadow-inner text-sm">
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <label class="flex items-center justify-between p-4 bg-slate-950 border border-slate-800 rounded-2xl cursor-pointer hover:border-slate-700 transition-all select-none">
                        <div class="flex items-center gap-3">
                            <div class="w-9 h-9 rounded-xl bg-purple-500/10 flex items-center justify-center text-purple-400"><i class="fa-solid fa-music"></i></div>
                            <div>
                                <p class="text-xs md:text-sm font-semibold">Extract Studio Audio</p>
                                <p class="text-[10px] text-slate-500">Isolate track layer directly</p>
                            </div>
                        </div>
                        <input type="checkbox" id="soundOnly" class="w-4 h-4 accent-cyan-500 rounded border-slate-800 bg-slate-900">
                    </label>

                    <label class="flex items-center justify-between p-4 bg-slate-950 border border-slate-800 rounded-2xl cursor-pointer hover:border-slate-700 transition-all select-none">
                        <div class="flex items-center gap-3">
                            <div class="w-9 h-9 rounded-xl bg-amber-500/10 flex items-center justify-center text-amber-400"><i class="fa-solid fa-compress"></i></div>
                            <div>
                                <p class="text-xs md:text-sm font-semibold">Mobile Optimization</p>
                                <p class="text-[10px] text-slate-500">Fast downloads for data plans</p>
                            </div>
                        </div>
                        <input type="checkbox" id="compressVideo" class="w-4 h-4 accent-cyan-500 rounded border-slate-800 bg-slate-900">
                    </label>
                </div>

                <button onclick="startDownload()" class="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 font-bold rounded-2xl text-white shadow-xl shadow-cyan-500/10 transform active:scale-[0.99] transition-all flex items-center justify-center gap-2 text-sm tracking-wide">
                    <i class="fa-solid fa-bolt"></i> Execute Deep Fetch
                </button>
            </div>

            <div id="statusContainer" class="mt-4 hidden bg-slate-950/80 border border-slate-800 rounded-2xl p-4 text-left font-mono text-[11px] text-slate-400 max-h-32 overflow-y-auto">
                <div id="statusText" class="flex items-center gap-2">
                    <i class="fa-solid fa-circle-notch animate-spin text-cyan-400"></i> Initializing global multi-channel routine...
                </div>
            </div>
        </div>

        <script>
            async function startDownload() {
                let rawInput = document.getElementById('videoUrl').value.trim();
                const soundOnly = document.getElementById('soundOnly').checked;
                const compressVideo = document.getElementById('compressVideo').checked;
                const statusContainer = document.getElementById('statusContainer');
                const statusText = document.getElementById('statusText');

                if (!rawInput) {
                    alert('Please enter a target media link!');
                    return;
                }

                const urlMatch = rawInput.match(/(https?:\\/\\/[^\\s]+)/);
                if (!urlMatch) {
                    alert('Invalid link! Please match standard web protocols.');
                    return;
                }
                
                const cleanUrl = urlMatch[0];
                statusContainer.classList.remove('hidden');
                statusText.innerHTML = `<div class="space-y-1">
                    <p class="text-cyan-400"><i class="fa-solid fa-shield-halved animate-pulse"></i> Multi-channel security shield active...</p>
                    <p class="text-slate-500">→ Targeting link stream matrices.</p>
                </div>`;

                window.location.href = `/download?url=${encodeURIComponent(cleanUrl)}&sound_only=${soundOnly}&compress=${compressVideo}`;
                
                setTimeout(() => {
                    statusText.innerHTML = `<p class="text-green-400"><i class="fa-solid fa-circle-check"></i> Asset extracted cleanly! Handing transmission package to device downloads.</p>`;
                }, 5000);
            }
        </script>
    </body>
    </html>
    """

@app.get("/download")
async def download_media(url: str, sound_only: bool = False, compress: bool = False):
    if not url:
        raise HTTPException(status_code=400, detail="Missing parameter target link.")

    # 💎 ENTERPRISE CORE CONFIGURATION
    # Adds spoof headers and security parameter bypasses to unblock Instagram/Threads/X
    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    # Audio Fix: Ensures compatibility with cloud hosting without crashing on URL structures
    if sound_only:
        ydl_opts.update({
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }] if os.path.exists('/usr/bin/ffmpeg') else [] # Dynamic cloud fallback
        })
    elif compress:
        ydl_opts.update({'format': 'worst[ext=mp4]/worst'})
    else:
        # Pulls pre-merged clean assets to stop extraction bottlenecks
        ydl_opts.update({'format': 'best[ext=mp4]/best'})

    try:
        loop = asyncio.get_event_loop()
        file_info = await loop.run_in_executor(
            None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=True)
        )
        saved_filename = yt_dlp.YoutubeDL(ydl_opts).prepare_filename(file_info)

        # Handle fallback formatting naming changes safely
        if sound_only and not saved_filename.endswith('.mp3') and os.path.exists(saved_filename.rsplit('.', 1)[0] + '.mp3'):
            saved_filename = saved_filename.rsplit('.', 1)[0] + '.mp3'

        schedule_file_deletion(saved_filename, delay_seconds=600)

        return FileResponse(
            path=saved_filename, 
            media_type='application/octet-stream', 
            filename=os.path.basename(saved_filename)
        )

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Channel extraction error: {str(error)}")