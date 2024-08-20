import whisper
from pydub import AudioSegment
import os
import subprocess

# Set environment variables for ffmpeg and ffprobe
os.environ["FFMPEG_BINARY"] = r"C:\Users\hubij\OneDrive\Pulpit\ffmpeg-7.0.2-essentials_build\bin\ffmpeg.exe"
os.environ["FFPROBE_BINARY"] = r"C:\Users\hubij\OneDrive\Pulpit\ffmpeg-7.0.2-essentials_build\bin\ffprobe.exe"

# Test FFmpeg and FFprobe access
ffmpeg_path = os.environ["FFMPEG_BINARY"]
ffprobe_path = os.environ["FFPROBE_BINARY"]

print(f"Testing FFmpeg at: {ffmpeg_path}")
print(f"Testing FFprobe at: {ffprobe_path}")

try:
    subprocess.run([ffmpeg_path, "-version"], check=True)
    subprocess.run([ffprobe_path, "-version"], check=True)
except Exception as e:
    print(f"Error: {e}")

def convert_to_wav(file_path):  
    try:
        audio = AudioSegment.from_file(file_path, format="m4a")
        wav_path = file_path.replace(".m4a", ".wav")  
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception as e:
        print(f"Error converting {file_path} to WAV: {e}")
        return None

def transcribe_audio(file_path):
    try:
        model = whisper.load_model("medium")
        res = model.transcribe(file_path, language='pl')
        return res['text']
    except Exception as e:
        print(f"Error transcribing {file_path}: {e}")
        return None

if __name__ == '__main__':
    file_paths = [
        r"C:\Users\hubij\grodkowska\a.m4a",
        r"C:\Users\hubij\grodkowska\b.m4a",
        r"C:\Users\hubij\grodkowska\c.m4a",
        r"C:\Users\hubij\grodkowska\d.m4a"
    ]
    
    for file_path in file_paths:
        wav_file_path = convert_to_wav(file_path)
        if wav_file_path:
            trans = transcribe_audio(wav_file_path)
            if trans:
                print(f"Transcription for {file_path}:")
                print(trans)
                output_file = file_path.replace(".m4a", "_trans.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(trans)
            os.remove(wav_file_path)
