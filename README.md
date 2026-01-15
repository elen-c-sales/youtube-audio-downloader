# YouTube Audio Downloader e Cutter

Pequeno app em Flask para baixar o audio de videos do YouTube e cortar trechos em MP3. Precisei de uma trilha para o desenvolvimento do meu jogo [dino-run-vecna-edition](https://github.com/elen-c-sales/dino-run-vecna-edition) e resolvi fazer este app como apoio para meus projetos.

https://github.com/user-attachments/assets/235f6815-2662-4870-a254-d25782ea3390

## Funcionalidades
- Download de audio via link do YouTube
- Conversao automatica para MP3
- Corte por intervalo de tempo (MM:SS)
- Download do trecho final com limpeza dos arquivos temporarios

## Requisitos
- Python 3.10+
- ffmpeg instalado e acessivel no PATH

## Instalacao
```bash
python -m venv .venv
```

Ative o ambiente virtual e instale as dependencias:
```bash
pip install flask yt-dlp pydub
```

## Uso
```bash
python app.py
```

Abra o navegador em `http://localhost:5000`.

## Estrutura basica
- `app.py`: servidor Flask e rotas
- `downloader.py`: utilitarios de download (se houver)
- `templates/index.html`: interface web
- `downloads/`: arquivos temporarios

## Links
- GitHub: https://github.com/elen-c-sales
- Site: https://elen-c-sales.github.io/
