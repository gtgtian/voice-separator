from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from voice_separation import separate_voices
from spectrogram_analysis import analyze_spectrogram  # Import the analyze_spectrogram function

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mpeg', 'wmv', 'mov', 'flv', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/separate', methods=['POST'])
def separate():
    try:
        if 'input_audio' not in request.files:
            return "No file part"
        
        file = request.files['input_audio']
        
        if file.filename == '':
            return "No selected file"
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_audio = 'uploads/' + filename
            output_audio = 'output_audio.wav'
            
            file.save(input_audio)
            separate_voices(input_audio, output_audio)
            
            # Perform spectrogram analysis and create chart
            analyze_spectrogram(input_audio)
            
            return send_file(output_audio, as_attachment=True)
        else:
            return "Invalid file format. Please upload a video file."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    app.run(debug=False)
