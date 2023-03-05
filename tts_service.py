from flask import Flask, jsonify, request
from tts_converter import TtsConverter

app = Flask(__name__)


@app.route('/tts_converter/', methods=['POST'])
def tts_convert():
    data = request.json
    print(f"!!! json = {data}")

    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400

    # mp3_bytes_obj = TtsConverter(**data)

    mp3_bytes_obj = TtsConverter({
        "repeat_request_count": data.get("repeat_request_count"),
        "buffer_size": data.get("buffer_size"),
        "first_strings_len": data.get("first_strings_len"),
        "last_strings_len": data.get("last_strings_len"),
        "voice": data.get("voice"),
        "voice_rate": data.get("voice_rate"),
        "voice_volume": data.get("voice_volume"),
        "text": data.get("text")
    }).convert()
    return jsonify({'status': 'success', 'result': mp3_bytes_obj}), 200


if __name__ == '__main__':
    app.run()