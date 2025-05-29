from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_summary(text: str) -> str:
    """
    Generate a structured summary of the provided text using OpenAI's API.

    Args:
        text (str): The input text to summarize.

    Returns:
        str: The generated summary.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that generates concise, "
                        "structured summaries of meeting transcripts."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Summarize the following meeting transcript in a "
                        "structured format (e.g., key points, decisions, "
                        f"action items):\n\n{text}"
                    ),
                },
            ],
            temperature=0.3,
            max_tokens=500,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")


def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file using OpenAI's Whisper API.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        str: The transcribed text.
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", file=audio_file
            )
        return transcription.text
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")
