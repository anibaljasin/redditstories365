import logging

from google.cloud import texttospeech

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Instantiates a client
client = texttospeech.TextToSpeechClient()
# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)
# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)


def generate_audio_from_text(text: str, output_file: str = "output.mp3"):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_file, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        logging.info(f'Audio content written to file {output_file}')

