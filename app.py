
# from flask_cors import CORS
# from flask import Flask, request, jsonify, send_file
# from audiocraft.models import MusicGen
# import torchaudio

# from pydub import AudioSegment
# import os

# app = Flask(__name__)

# @app.route('/generate', methods=['POST'])
# def generate_music():
#     data = request.get_json()
#     prompt = data.get('prompt')

#     if not prompt:
#         return {'error': 'Prompt is required'}, 400

#     # Dummy logic to generate audio. Replace with your AI model later.
#     print(f"Generating music for prompt: {prompt}")

#     # Simulate a .mp3 creation
#     audio = AudioSegment.silent(duration=3000)  # 3 seconds silence
#     output_path = 'output.mp3'
#     audio.export(output_path, format="mp3")

#     return {'message': 'Music generated successfully'}, 200

# @app.route('/download', methods=['GET'])
# def download_music():
#     path = 'output.mp3'
#     if not os.path.exists(path):
#         return {'error': 'File not found'}, 404
#     return send_file(path, mimetype='audio/mpeg')
# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from audiocraft.models import MusicGen
from pydub import AudioSegment
import torchaudio
import os

app = Flask(__name__)
CORS(app)

# Load MusicGen model once when server starts
model = MusicGen.get_pretrained('facebook/musicgen-small')  # or medium/large

@app.route('/generate', methods=['POST'])
def generate_music():
    data = request.get_json()
    prompt = data.get('prompt')
    duration = data.get('duration', 10)  # default 10s

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    if not (1 <= duration <= 240):
        return jsonify({'error': 'Duration must be between 1 and 240 seconds'}), 400

    try:
        print(f"Generating music for prompt: {prompt}, duration: {duration}s")
        model.set_generation_params(duration=duration)
        output = model.generate([prompt])

        torchaudio.save("output.wav", output[0].cpu(), sample_rate=32000)

        audio = AudioSegment.from_wav("output.wav")
        audio.export("output.mp3", format="mp3")

        return jsonify({'message': 'Music generated'}), 200

    except Exception as e:
        print("Generation error:", str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['GET'])
def download_music():
    if not os.path.exists("output.mp3"):
        return jsonify({'error': 'File not found'}), 404

    return send_file("output.mp3", mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(debug=True)
