import yt_dlp

# A URL do vídeo
url = "https://www.youtube.com/watch?v=5v1xqBnGg5I"

# As opções de download (equivalente a -x --audio-format mp3)
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Executa o download
try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Download concluído com sucesso!")
except Exception as e:
    print(f"Ocorreu um erro: {e}")