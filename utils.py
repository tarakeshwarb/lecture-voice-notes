import openai
import whisper
import os
from dotenv import load_dotenv
import sqlite3

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from .env or .env.example with absolute paths
env_path = os.path.join(script_dir, ".env")
env_example_path = os.path.join(script_dir, ".env.example")

if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv(env_example_path)

# Initialize OpenAI client lazily to ensure env vars are loaded
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here" or api_key == "sk-your-actual-api-key-here":
            raise ValueError("Please set a valid OPENAI_API_KEY in .env.example or .env")
        _client = openai.OpenAI(api_key=api_key)
    return _client

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lectures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        transcript TEXT,
        summary TEXT,
        quiz TEXT,
        flashcards TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

def transcribe_audio(audio_file):
    """
    Transcribe audio file using OpenAI Whisper API
    """
    try:
        transcript = get_client().audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcript.text
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

def generate_study_materials(transcript):
    """
    Generate study materials from transcript using OpenAI GPT
    """
    try:
        prompt = f"""
        Summarize the following lecture into structured notes.
        Then generate:
        1. 5 quiz questions with answers
        2. 5 flashcards (Q&A format)

        Lecture:
        {transcript}

        Format your response clearly with sections:
        SUMMARY: [content]
        QUIZ: [content]
        FLASHCARDS: [content]
        """
        
        response = get_client().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert educational assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        
        # Parse sections
        summary = ""
        quiz = ""
        flashcards = ""
        
        if "SUMMARY:" in content:
            summary_part = content.split("SUMMARY:")[1]
            if "QUIZ:" in summary_part:
                summary = summary_part.split("QUIZ:")[0].strip()
                quiz_part = summary_part.split("QUIZ:")[1]
                if "FLASHCARDS:" in quiz_part:
                    quiz = quiz_part.split("FLASHCARDS:")[0].strip()
                    flashcards = quiz_part.split("FLASHCARDS:")[1].strip()
                else:
                    quiz = quiz_part.strip()
            else:
                summary = summary_part.strip()
        
        return {
            'summary': summary,
            'quiz': quiz,
            'flashcards': flashcards
        }
    
    except Exception as e:
        raise Exception(f"Study materials generation failed: {str(e)}")

def save_to_db(filename, transcript, summary, quiz, flashcards):
    """Save lecture data to database"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO lectures (filename, transcript, summary, quiz, flashcards)
    VALUES (?, ?, ?, ?, ?)
    """, (filename, transcript, summary, quiz, flashcards))

    conn.commit()
    conn.close()

def fetch_all():
    """Retrieve all lectures from database"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM lectures ORDER BY created_at DESC")
    data = cursor.fetchall()
    conn.close()
    return data
