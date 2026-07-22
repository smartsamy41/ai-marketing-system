from google.cloud import texttospeech


client = texttospeech.TextToSpeechClient()


text = """
Du möchtest deinen Stromtarif prüfen?
Bei Free Basics findest du Informationen zu verschiedenen Angeboten und Möglichkeiten.
"""


synthesis_input = texttospeech.SynthesisInput(
    text=text
)


voice = texttospeech.VoiceSelectionParams(
    language_code="de-DE",
    name="de-DE-Neural2-F",
)


audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)


response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)


with open(
    "generated_videos/voice_test.mp3",
    "wb"
) as out:
    out.write(response.audio_content)


print("VOICE OK")
print("generated_videos/voice_test.mp3")
