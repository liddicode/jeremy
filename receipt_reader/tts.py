import subprocess

ipa_text = "ˈpɪθən ˈsɪmbəlz tuː spiːtʃ"
output_file = "file.wav"

# Call espeak-ng to synthesize speech from IPA and save to a WAV file
subprocess.run(["espeak-ng", "-q", "-v", "en-us", "--ipa", ipa_text, "-w", output_file])

print(f"Speech saved to {output_file}")

# You can then play this WAV file using libraries like `pydub` or `soundfile`
# For example, using pydub:
from pydub import AudioSegment
from pydub.playback import play
song = AudioSegment.from_wav(output_file)
play(song)