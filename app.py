from flask import Flask, request, render_template, send_file
from google.cloud import translate_v2 as translate
import os
import pysrt
from io import BytesIO

app = Flask(__name__)

# Set up Google Cloud Translate
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\aseem\PycharmProjects\SubtitleTranslation\credentials.json"
translator = translate.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate_srt_preview', methods=['POST'])
def translate_srt_preview():
    # Check if an SRT file and target language are provided
    if 'srt_file' not in request.files or 'target_language' not in request.form:
        return 'Error: SRT file and target language are required.', 400

    # Get the uploaded SRT file and target language
    srt_file = request.files['srt_file']
    target_language = request.form.get('target_language')

    # Parse the SRT file using pysrt
    subtitles = pysrt.from_string(srt_file.read().decode('utf-8'))
    translated_subtitles = []

    # Translate each subtitle block
    for subtitle in subtitles:
        translated_text = translator.translate(subtitle.text, target_language=target_language)['translatedText']
        translated_subtitles.append(f"{subtitle.index}\n{subtitle.start} --> {subtitle.end}\n{translated_text}\n")

    # Return translated subtitles as plain text for preview
    return '\n'.join(translated_subtitles)

@app.route('/download_srt', methods=['POST'])
def download_srt():
    # Check if an SRT file and target language are provided
    if 'srt_file' not in request.files or 'target_language' not in request.form:
        return 'Error: SRT file and target language are required.', 400

    # Get the uploaded SRT file and target language
    srt_file = request.files['srt_file']
    target_language = request.form.get('target_language')

    # Parse the SRT file using pysrt
    subtitles = pysrt.from_string(srt_file.read().decode('utf-8'))
    translated_subtitles = []

    # Translate each subtitle block
    for subtitle in subtitles:
        translated_text = translator.translate(subtitle.text, target_language=target_language)['translatedText']
        translated_subtitles.append(f"{subtitle.index}\n{subtitle.start} --> {subtitle.end}\n{translated_text}\n")

    # Convert the translated subtitles into a single string for SRT file
    translated_srt_content = '\n'.join(translated_subtitles)

    # Create a BytesIO object for the translated SRT file
    srt_io = BytesIO()
    srt_io.write(translated_srt_content.encode('utf-8'))
    srt_io.seek(0)

    # Return the SRT file as a download
    return send_file(srt_io, as_attachment=True, download_name='translated_subtitles.srt', mimetype='text/srt')

if __name__ == '__main__':
    app.run(debug=True)
