from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
import yt_dlp
import os
import asyncio
import time

app = FastAPI(title="OmniFetch Cloud Engine")

DOWNLOAD_FOLDER = "omnifetch_vault"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 🧹 AUTOMATIC STORAGE PURGE SYSTEM
def schedule_file_deletion(file_path: str, delay_seconds: int = 600):
    """
    Background Task: Wait 10 minutes, then safely wipe the file from the
    server disk to ensure free storage space remains constant.
    """
    def delete_task():
        time.sleep(delay_seconds)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"[Engine Vault Cleanup] Safely purged: {file_path}")
        except Exception as e:
            print(f"[Engine Vault Error] Cleanup failed for {file_path}: {e}")
            
    # Run the countdown clock on a completely separate background thread
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
        <title>OmniFetch - Global Media Archive</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    </head>
    <body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col justify-center items-center font-sans px-4">
        <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl pointer-events-none"></div>

        <div class="w-full max-w-2xl bg-slate-900/60 border border-slate-800/80 rounded-3xl p-8 backdrop-blur-xl shadow-2xl relative z-10 text-center">
            <div class="mb-8">
                <div class="inline-flex items-center justify-center bg-cyan-500/10 border border-cyan-500/30 w-16 h-16 rounded-2xl text-cyan-400 text-3xl mb-4 shadow-lg shadow-cyan-500/5">
                    <i class="fa-solid fa-earth-americas"></i>
                </div>
                <h1 class="text-4xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white via-slate-200 to-slate-400">OmniFetch</h1>
                <p class="text-slate-400 mt-2 text-sm md:text-base font-medium">Securing global media access. Archiving information without boundaries.</p>
            </div>

            <div class="space-y-6 text-left">
                <div class="relative">
                    <span class="absolute inset-y-0 left-0 flex items-center pl-4 text-slate-500"><i class="fa-solid fa-link"></i></span>
                    <input type="text" id="videoUrl" placeholder="Paste social media or data link here..." class="w-full pl-11 pr-4 py-4 bg-slate-950 border border-slate-800 rounded-2xl text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500/50 transition-colors shadow-inner text-sm md:text-base">
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <label class="flex items-center justify-between p-4 bg-slate-950 border border-slate-800 rounded-2xl cursor-pointer hover:border-slate-700 transition-all select-none">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center text-purple-400"><i class="fa-solid fa-music"></i></div>
                            <div>
                                <p class="text-sm font-semibold">Extract Studio Audio</p>
                                <p class="text-xs text-slate-500">Isolate vocals to 320kbps MP3</p>
                            </div>
                        </div>
                        <input type="checkbox" id="soundOnly" class="w-5 h-5 accent-cyan-500 rounded border-slate-800 bg-slate-900">
                    </label>

                    <label class="flex items-center justify-between p-4 bg-slate-950 border border-slate-800 rounded-2xl cursor-pointer hover:border-slate-700 transition-all select-none">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center text-amber-400"><i class="fa-solid fa-compress"></i></div>
                            <div>
                                <p class="text-sm font-semibold">Optimize Resolution</p>
                                <p class="text-xs text-slate-500">Compress file size for mobile networks</p>
                            </div>
                        </div>
                        <input type="checkbox" id="compressVideo" class="w-5 h-5 accent-cyan-500 rounded border-slate-800 bg-slate-900">
                    </label>
                </div>

                <button onclick="startDownload()" class="w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 font-bold rounded-2xl text-white shadow-xl shadow-cyan-500/10 transform active:scale-[0.99] transition-all flex items-center justify-center gap-2 tracking-wide">
                    <i class="fa-solid fa-circle-down"></i> Process & Fetch Asset
                </button>
            </div>

            <div id="statusContainer" class="mt-6 hidden bg-slate-950/80 border border-slate-800 rounded-2xl p-4 text-left font-mono text-xs text-slate-400">
                <div id="statusText" class="flex items-center gap-2">
                    <i class="fa-solid fa-circle-notch animate-spin text-cyan-400"></i> Initializing global fetch routine...
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
                    alert('Please paste a link first!');
                    return;
                }

                const urlMatch = rawInput.match(/(https?:\\/\\/[^\\s]+)/);
                if (!urlMatch) {
                    alert('Could not find a valid link!');
                    return;
                }
                
                const cleanUrl = urlMatch[0];
                statusContainer.classList.remove('hidden');
                statusText.innerHTML = `<i class="fa-solid fa-circle-notch animate-spin text-cyan-400"></i> Packaging pipeline options & connecting to stream...`;

                window.location.href = `/download?url=${encodeURIComponent(cleanUrl)}&sound_only=${soundOnly}&compress=${compressVideo}`;
                
                setTimeout(() => {
                    statusText.innerHTML = `<i class="fa-solid fa-circle-check text-green-400"></i> Delivery initiated! Auto-purging server copy in 10 minutes.`;
                }, 6000);
            }
        </script>
    </body>
    </html>
    """

@app.get("/download")
async def download_media(url: str, sound_only: bool = False, compress: bool = False):
    if not url:
        raise HTTPException(status_code=400, detail="Please provide a valid link!")

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'restrictfilenames': True,
    }

    if sound_only:
        ydl_opts.update({'format': 'bestaudio/best'})
    elif compress:
        ydl_opts.update({'format': 'worstvideo+bestaudio/best'})
    else:
        ydl_opts.update({'format': 'best'})

    try:
        # Runs the extraction asynchronously so multiple requests don't choke the server
        loop = asyncio.get_event_loop()
        file_info = await loop.run_in_executor(
            None, lambda: yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=True)
        )
        saved_filename = yt_dlp.YoutubeDL(ydl_opts).prepare_filename(file_info)

        # 🚀 TRIGGER STORAGE SAFETY PROTECTION TRIGGER
        schedule_file_deletion(saved_filename, delay_seconds=600)

        return FileResponse(
            path=saved_filename, 
            media_type='application/octet-stream', 
            filename=os.path.basename(saved_filename)
        )

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Engine error: {str(error)}")