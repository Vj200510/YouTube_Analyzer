import os
from textwrap import dedent
from dotenv import load_dotenv
from pathlib import Path
import re
from youtube_transcript_api import YouTubeTranscriptApi
from groq import Groq

load_dotenv(Path(__file__).parent / "api_keys.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_youtube_agent():
    instructions = dedent("""\
        You are an expert YouTube content analyst with a keen eye for detail! 🎓
        Follow these steps for comprehensive video analysis:
        1. Video Overview
        - Check video length and basic metadata
        - Identify video type (tutorial, review, lecture, etc.)
        - Note the content structure
        2. Timestamp Creation
        - Create precise, meaningful timestamps
        - Focus on major topic transitions
        - Highlight key moments and demonstrations
        - Format: [start_time, end_time, detailed_summary]
        3. Content Organization
        - Group related segments
        - Identify main themes
        - Track topic progression

        Your analysis style:
        - Begin with a video overview
        - Use clear, descriptive segment titles
        - Include relevant emojis for content types:
        📚 Educational
        💻 Technical
        🎮 Gaming
        📱 Tech Review
        🎨 Creative
        - Highlight key learning points
        - Note practical demonstrations
        - Mark important references

        Quality Guidelines:
        - Verify timestamp accuracy
        - Avoid timestamp hallucination
        - Ensure comprehensive coverage
        - Maintain consistent detail level
        - Focus on valuable content markers
    """)

    def analyze(prompt):
        video_url = prompt.replace("Analyze this video: ", "").strip()
        video_id_match = re.search(r"(?<=v=)[^&]+", video_url)
        if not video_id_match:
            class MockResponse:
                content = "Invalid YouTube URL"
            return MockResponse()
        video_id = video_id_match.group(0)
        try:
            import requests
            from http.cookiejar import MozillaCookieJar
            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            })
            cookie_path = Path(__file__).parent / "cookies.txt"
            if cookie_path.exists():
                jar = MozillaCookieJar(str(cookie_path))
                jar.load(ignore_discard=True, ignore_expires=True)
                session.cookies.update(jar)
            api = YouTubeTranscriptApi(http_client=session)
            transcript_list = api.list(video_id)
            try:
                fetched = transcript_list.find_transcript(['en', 'hi']).translate('en').fetch()
            except Exception:
                fetched = transcript_list.find_transcript(['en', 'hi']).fetch()
            transcript = ' '.join([entry.text for entry in fetched])
        except Exception as e:
            class MockResponse:
                content = f"Could not fetch transcript: {str(e)}"
            return MockResponse()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": f"{prompt}\n\nTranscript: {transcript[:12000]}... (truncated for token limit)"}
            ],
            temperature=0.1,
            max_tokens=4096
        )
        class MockResponse:
            content = response.choices[0].message.content
        return MockResponse()

    return analyze

# youtube_agent.print_response(
#     "Analyze this video: https://www.youtube.com/watch?v=JkaxUblCGz0",
#     stream=True,
# )