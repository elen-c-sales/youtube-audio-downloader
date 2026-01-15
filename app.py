import os
import time
from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp
from pydub import AudioSegment

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"

# Cria a pasta de downloads se nao existir
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)


def time_to_ms(time_str):
    """Converte 'MM:SS' ou 'SS' para milissegundos"""
    if ":" in time_str:
        m, s = map(int, time_str.split(":"))
        return (m * 60 * 1000) + (s * 1000)
    return int(time_str) * 1000


@app.route("/", methods=["GET", "POST"])
def index():
    filename = None
    error = None

    if request.method == "POST":
        url = request.form.get("url")
        action = request.form.get("action", "cut")
        if url:
            # Opcoes do yt-dlp
            # Usamos um timestamp no nome para evitar arquivos duplicados
            timestamp = int(time.time())
            output_template = os.path.join(
                DOWNLOAD_FOLDER, f"audio_{timestamp}.%(ext)s"
            )

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": output_template,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    # O nome final do arquivo (com extensao mp3)
                    filename = f"audio_{timestamp}.mp3"

                if action == "download":
                    file_path = os.path.join(DOWNLOAD_FOLDER, filename)

                    @after_this_request
                    def remove_file(response):
                        try:
                            os.remove(file_path)
                        except Exception as e:
                            print(f"Erro ao limpar arquivos: {e}")
                        return response

                    return send_file(file_path, as_attachment=True)
            except Exception as e:
                error = f"Erro ao baixar: {str(e)}"

    return render_template("index.html", filename=filename, error=error)


@app.route("/cut", methods=["POST"])
def cut_audio():
    try:
        filename = request.form.get("filename")
        start_str = request.form.get("start")  # ex: 00:10
        end_str = request.form.get("end")  # ex: 02:30

        file_path = os.path.join(DOWNLOAD_FOLDER, filename)

        # Carrega o audio
        audio = AudioSegment.from_file(file_path)

        # Converte tempos e corta
        start_ms = time_to_ms(start_str)
        end_ms = time_to_ms(end_str) if end_str else len(audio)

        cut_audio = audio[start_ms:end_ms]

        # Salva o corte
        cut_filename = f"corte_{filename}"
        cut_path = os.path.join(DOWNLOAD_FOLDER, cut_filename)
        cut_audio.export(cut_path, format="mp3")

        # Envia o arquivo para o usuario e deleta depois (opcional)
        @after_this_request
        def remove_file(response):
            try:
                # Removemos o original e o corte para nao encher o disco
                os.remove(file_path)
                os.remove(cut_path)
            except Exception as e:
                print(f"Erro ao limpar arquivos: {e}")
            return response

        return send_file(cut_path, as_attachment=True)

    except Exception as e:
        return f"Erro ao processar audio: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)
