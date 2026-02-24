# 🎓 Lecture Voice-to-Notes Generator

An AI-powered web application that converts lecture audio into structured study materials including summaries, quizzes, and flashcards.

## 🚀 Features

- **Audio Transcription**: Convert lecture audio (MP3, WAV, M4A) to text using OpenAI Whisper
- **AI-Powered Summarization**: Generate concise summaries of lecture content
- **Quiz Generation**: Automatically create relevant quiz questions with answers
- **Flashcard Creation**: Generate study flashcards in Q&A format
- **Persistent Storage**: Store and retrieve all lecture materials using SQLite
- **User-Friendly Interface**: Simple and intuitive Streamlit interface

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Speech-to-Text**: OpenAI Whisper
- **AI Generation**: OpenAI GPT-3.5-turbo
- **Database**: SQLite
- **Deployment**: Streamlit Cloud / Render

## 📋 Prerequisites

- Python 3.8+
- OpenAI API Key

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd lecture-voice-notes
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

## 🚀 Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   Navigate to `http://localhost:8501`

## 📁 Project Structure

```
lecture-voice-notes/
│
├── app.py              # Main Streamlit application
├── utils.py            # Utility functions for AI processing
├── database.db         # SQLite database (auto-created)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env               # Your environment variables (create this)
└── README.md          # Project documentation
```

## 🔧 Database Schema

The application uses SQLite with a single table `lectures`:

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER (PK) | Unique lecture ID |
| filename | TEXT | Uploaded audio file name |
| transcript | TEXT | Full lecture transcript |
| summary | TEXT | AI-generated summary |
| quiz | TEXT | Generated quiz questions |
| flashcards | TEXT | Flashcards content |
| created_at | DATETIME | Upload timestamp |

## 🌐 Deployment

### Option 1: Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Add your OpenAI API key in the deployment settings
4. Deploy!

### Option 2: Render
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. Add environment variables

## 📝 Usage

1. **Upload Lecture Audio**: Use the upload button to select your audio file
2. **Generate Materials**: Click the "Generate Study Materials" button
3. **View Results**: Access transcript, summary, quiz, and flashcards in organized tabs
4. **Browse History**: View all previously processed lectures in the History section

## 🎯 Key Features

- **Fast Processing**: Quick transcription and AI generation
- **High Accuracy**: Uses state-of-the-art AI models
- **Organized Output**: Clean, structured study materials
- **Data Persistence**: All materials stored for future reference
- **Responsive Design**: Works on desktop and mobile devices

## 🔒 Security Notes

- API keys are stored securely using environment variables
- Audio files are processed temporarily and deleted after use
- Database is stored locally and contains only lecture content

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

**Common Issues:**

1. **OpenAI API Error**: Ensure your API key is valid and has sufficient credits
2. **Audio Processing Error**: Check that your audio file is in a supported format (MP3, WAV, M4A)
3. **Database Error**: Ensure write permissions in the project directory

**Support:**
For issues and questions, please create an issue in the GitHub repository.

---

🎓 **Made with ❤️ for students and educators**
