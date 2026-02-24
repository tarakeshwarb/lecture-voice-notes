import streamlit as st
import os
from utils import init_db, transcribe_audio, generate_study_materials, save_to_db, fetch_all

# Initialize database
init_db()

# Streamlit UI
st.set_page_config(page_title="Lecture Voice-to-Notes Generator", page_icon="🎓", layout="wide")

st.title("🎓 Lecture Voice-to-Notes Generator")
st.markdown("Convert your lecture audio into structured study notes, quizzes, and flashcards using AI.")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page:", ["Upload Lecture", "View History"])

if page == "Upload Lecture":
    st.header("📤 Upload Lecture Audio")
    
    # File upload
    audio_file = st.file_uploader(
        "Upload your lecture audio file (MP3, WAV, M4A, MP4)",
        type=['mp3', 'wav', 'm4a', 'mp4']
    )
    
    if audio_file is not None:
        # Determine audio format for player
        file_ext = audio_file.name.split('.')[-1].lower()
        audio_format = f'audio/{file_ext}' if file_ext != 'mp4' else 'video/mp4'
        st.audio(audio_file, format=audio_format)
        
        # Process button
        if st.button("🚀 Generate Study Materials", type="primary"):
            with st.spinner("Processing your lecture... This may take a few minutes."):
                try:
                    # Transcribe audio
                    st.info("🎙️ Transcribing audio...")
                    transcript = transcribe_audio(audio_file)
                    
                    # Generate study materials
                    st.info("🤖 Generating study materials...")
                    study_materials = generate_study_materials(transcript)
                    
                    # Store in database
                    save_to_db(
                        audio_file.name,
                        transcript,
                        study_materials['summary'],
                        study_materials['quiz'],
                        study_materials['flashcards']
                    )
                    
                    # Display results
                    st.success("✅ Study materials generated successfully!")
                    
                    # Results in tabs
                    tab1, tab2, tab3, tab4 = st.tabs(["📝 Transcript", "📋 Summary", "📝 Quiz", "🎴 Flashcards"])
                    
                    with tab1:
                        st.subheader("Full Transcript")
                        st.text_area("Transcript", transcript, height=300)
                    
                    with tab2:
                        st.subheader("AI-Generated Summary")
                        st.markdown(study_materials['summary'])
                    
                    with tab3:
                        st.subheader("Quiz Questions")
                        st.markdown(study_materials['quiz'])
                    
                    with tab4:
                        st.subheader("Flashcards")
                        st.markdown(study_materials['flashcards'])
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

elif page == "View History":
    st.header("📚 Lecture History")
    
    # Fetch all lectures
    lectures = fetch_all()
    
    if not lectures:
        st.info("No lectures found. Upload your first lecture to get started!")
    else:
        for lecture in lectures:
            with st.expander(f"📁 {lecture[1]} - {lecture[6][:10]}"):
                st.markdown("**📋 Summary:**")
                st.markdown(lecture[3])
                
                st.markdown("**📝 Quiz:**")
                st.markdown(lecture[4])
                
                st.markdown("**🎴 Flashcards:**")
                st.markdown(lecture[5])

# Footer
st.markdown("---")
st.markdown("🎓 Lecture Voice-to-Notes Generator | Powered by AI")
