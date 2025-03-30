import openai
import json
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import requests
import os


# ✅ OpenAI API Key (Do not expose in production)
openai.api_key = os.getenv(
    "OPENAI_API_KEY"
)  # Ensure you have set this in your environment


def extract_youtube_video_id(video_url):
    """Extracts video ID from various YouTube URL formats."""
    try:
        parsed_url = urlparse(video_url)
        if parsed_url.netloc in ["youtu.be", "www.youtu.be"]:
            return parsed_url.path[1:]  # Extracts after "/"
        elif parsed_url.netloc in ["www.youtube.com", "youtube.com"]:
            return parse_qs(parsed_url.query).get("v", [None])[0]
        return None
    except Exception as e:
        return None


def get_youtube_transcript(video_url):
    """Fetches the YouTube video transcript."""
    video_id = extract_youtube_video_id(video_url)
    if not video_id:
        return None, "Invalid YouTube URL"

    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([t["text"] for t in transcript_data])
        return transcript, None
    except Exception as e:
        return None, str(e)


# def generate_questions(transcript, difficulty):
#     """Generates 25 quiz questions using GPT API with difficulty levels."""
#     prompt = (
#         f"Generate 5 {difficulty} level multiple-choice questions from this transcript:\n{transcript}\n"
#         "Each question should have 4 options and one correct answer."
#     )

#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are an AI that generates quiz questions.",
#                 },
#                 {"role": "user", "content": prompt},
#             ],
#             max_tokens=2000,
#             temperature=1.0,  # Higher temperature generates diverse questions
#         )
#         return response["choices"][0]["message"]["content"]
#     except Exception as e:
#         return f"Error generating questions: {str(e)}"


def generate_questions(transcript, difficulty="easy"):
    """Generate questions using DeepSeek model via Ollama."""
    url = "http://127.0.0.1:11435/api/generate"  # Assuming Ollama is running on this address
    headers = {"Content-Type": "application/json"}

    # Custom prompt to generate questions
    prompt = (
        f"Generate 5 {difficulty} level multiple-choice questions from the following transcript:\n{transcript}\n"
        "Each question should have 4 options and one correct answer."
    )

    payload = {
        "model": "deepseek-r1",  # Specify the model here
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.0,
        "max_tokens": 500,
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error generating questions: {response.status_code}"


def main(video_url):
    """Main function to generate quiz questions based on YouTube video link."""
    transcript, error = get_youtube_transcript(video_url)
    if error:
        return json.dumps({"error": error}), 400

    questions_easy = generate_questions(transcript, "easy")
    questions_medium = generate_questions(transcript, "medium")
    questions_hard = generate_questions(transcript, "hard")

    # Creating a dictionary to store questions
    result = {
        "easy": questions_easy,
        "medium": questions_medium,
        "hard": questions_hard,
    }

    return json.dumps(result, indent=4)  # Return JSON formatted output


# Example usage
if __name__ == "__main__":
    # Example: Replace with any valid YouTube video URL
    video_url = "https://youtu.be/M576WGiDBdQ?si=Ay35GL8rBHQzI4cy"
    print(main(video_url))
