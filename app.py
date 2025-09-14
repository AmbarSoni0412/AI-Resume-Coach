from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
import time
import logging
from PIL import Image
import pdf2image
import google.generativeai as genai
from google.api_core import exceptions as gcp_exceptions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    max_retries = 3
    retry_delay = 60
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content([input, pdf_content[0], prompt])
            return response.text
            
        except gcp_exceptions.ResourceExhausted:
            if attempt < max_retries - 1:
                st.warning(f"⚠️ API quota exceeded. Retrying in {retry_delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                st.error("🚫 API quota exceeded. Please try again later.")
                st.info("💡 **Free Tier Limits:**\n- 15 requests per minute\n- 1,500 requests per day\n- 32,000 tokens per minute")
                return "Sorry, I've reached the API quota limit. Please try again in a few minutes."
                
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            return "Sorry, an error occurred while processing your request. Please try again."

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            # Check file size (limit to 10MB)
            if uploaded_file.size > 10 * 1024 * 1024:
                raise ValueError("File size too large. Please upload a file smaller than 10MB.")
            
            # Configure poppler path based on environment
            poppler_path = None
            
            # For cloud deployment, poppler is usually in PATH
            if os.name == 'nt':  # Windows
                possible_paths = [
                    r'C:\poppler\poppler-23.08.0\Library\bin',
                    r'C:\poppler\bin',
                    r'C:\Program Files\poppler\bin',
                    r'C:\Program Files (x86)\poppler\bin',
                    r'C:\tools\poppler\bin'
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        poppler_path = path
                        break
            
            # Convert PDF to image
            images = pdf2image.convert_from_bytes(
                uploaded_file.getvalue(),
                poppler_path=poppler_path,
                dpi=200,  # Good quality for analysis
                first_page=1,
                last_page=1  # Only process first page for efficiency
            )

            if not images:
                raise ValueError("Could not extract images from PDF")

            first_page = images[0]
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG', quality=85)
            img_byte_arr = img_byte_arr.getvalue()

            pdf_parts = [{
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }]
            
            logger.info(f"Successfully processed PDF: {uploaded_file.name}")
            return pdf_parts
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise ValueError(f"Error processing PDF: {str(e)}")
    else:
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title="Resume Tracker")
st.header("Career Honors Resume Coach")

with st.expander("ℹ️ Free Tier Information"):
    st.info("""
    **Google AI Free Tier Limits:**
    - 15 requests per minute
    - 1,500 requests per day  
    - 32,000 tokens per minute
    
    💡 **Tips to stay within limits:**
    - Use concise descriptions
    - Avoid multiple rapid requests
    - The app will automatically retry if quota is exceeded
    """)

input_text = st.text_area("Job Description (optional): ", key="input", placeholder="Paste the job description here for better analysis...")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Analyze Resume")

input_prompt1 = """You are a professional resume coach. I will provide you with a resume, and your task is to analyze it carefully. 

Give me specific, actionable suggestions on how to improve the CV in the following areas:
1. **Formatting & Structure** - readability, layout, sections, bullet points.
2. **Content Quality** - clarity of job roles, use of action verbs, avoiding generic phrases.
3. **Skills Section** - whether the skills match the targeted role, and suggestions for better technical/soft skills presentation.
4. **Achievements & Impact** - check if the resume shows measurable results (e.g., numbers, percentages, outcomes) and suggest improvements.
5. **ATS Friendliness** - identify if the CV will pass through Applicant Tracking Systems and suggest missing keywords or optimizations.
6. **Overall Strengths & Weaknesses** - highlight what's good and what needs change.

End with a short, prioritized checklist: "Top 3 improvements to make right now."
"""

if submit1:
    if uploaded_file is not None:
        # Validate API key
        if not os.getenv("GOOGLE_API_KEY"):
            st.error("❌ Google API key not configured. Please set GOOGLE_API_KEY environment variable.")
            st.stop()
        
        # Rate limiting
        if 'last_request_time' not in st.session_state:
            st.session_state.last_request_time = 0
        
        current_time = time.time()
        time_since_last_request = current_time - st.session_state.last_request_time
        
        if time_since_last_request < 5:
            st.warning("⏳ Please wait a few seconds before making another request to respect rate limits.")
        else:
            try:
                with st.spinner("🔄 Analyzing your resume..."):
                    # Process PDF
                    pdf_content = input_pdf_setup(uploaded_file)
                    
                    # Get AI response
                    response = get_gemini_response(input_prompt1, pdf_content, input_text)
                    st.session_state.last_request_time = current_time
                    
                    # Display results
                    st.subheader("📋 Resume Analysis")
                    st.write(response)
                    
            except ValueError as e:
                st.error(f"❌ {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                st.error("❌ An unexpected error occurred. Please try again.")
    else:
        st.warning("⚠️ Please upload a PDF resume file.")