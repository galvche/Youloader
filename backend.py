from flask import Flask, request, jsonify, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

def search_youtube(query):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,
        'force_generic_extractor': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch10:{query}", download=False)
        videos = search_results.get('entries', [])
        
        formatted_results = []
        for video in videos:
            formatted_results.append({
                'id': video.get('id'),
                'title': video.get('title'),
                'url': f"https://www.youtube.com/watch?v={video.get('id')}",
                'thumbnails': video.get('thumbnails', [{'url': ''}])  # Manejo seguro
            })
        return formatted_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    results = search_youtube(query)
    return jsonify(results)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url', '')
    format_type = request.args.get('format', 'mp3')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': False
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = f"downloads/{info['title']}.mp3"
    
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs('downloads', exist_ok=True)
    app.run(debug=True)
