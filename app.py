import os
from dotenv import load_dotenv

from datetime import datetime
import io

from PIL import Image
from PyPDF2 import PdfReader
from docxtpl import DocxTemplate
import streamlit as st
from streamlit_option_menu import option_menu
import google.generativeai as genai
from gemini_utility import (
    load_gemini_pro_model,
    gemini_pro_response,
    gemini_pro_vision_response,
    embeddings_model_response
)

# Load environment variables
load_dotenv()

current_datetime = datetime.now()
filename = f"generated_doc_{current_datetime.strftime('%Y%m%d_%H%M%S')}.docx"

# Function to initialize and configure Gemini Pro model
def get_gemini_pro():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel('gemini-pro')

# Function to extract text from PDF files
def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Functions to construct prompts for different functionalities
def construct_skills_prompt(resume, job_description):
    skill_prompt = f'''Act as a HR Manager with 20 years of experience.
    Compare the resume provided below with the job description given below.
    Check for key skills in the resume that are related to the job description.
    List the missing key skillset from the resume.
    I just need the extracted missing skillset.
    Here is the Resume text: {resume}
    Here is the Job Description: {job_description}
    I want the response as a list of missing skill words.'''
    return skill_prompt

def construct_resume_score_prompt(resume, job_description):
    resume_score_prompt = f'''Act as a HR Manager with 20 years of experience.
    Compare the resume provided below with the job description given below.
    Check for key skills in the resume that are related to the job description.
    Rate the resume out of 100 based on the matching skill set.
    Assess the score with high accuracy.
    Here is the Resume text: {resume}
    Here is the Job Description: {job_description}
    I want the response as a single string in the following structure: score:%'''
    return resume_score_prompt

# Function to interact with Gemini Pro model and get response
def get_result(input):
    model = get_gemini_pro()
    response = model.generate_content(input)
    return response.text

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Function to initialize and configure Gemini Pro model
def get_gemini_pro():
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel('gemini-pro')

# Function to extract text from PDF files
def pdf_to_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += str(page.extract_text())
    return text

# Functions to construct prompts for different functionalities
def construct_skills_prompt(resume, job_description):
    skill_prompt = f'''Act as a HR Manager with 20 years of experience.
    Compare the resume provided below with the job description given below.
    Check for key skills in the resume that are related to the job description.
    List the missing key skillset from the resume.
    I just need the extracted missing skillset.
    Here is the Resume text: {resume}
    Here is the Job Description: {job_description}
    I want the response as a list of missing skill words.'''
    return skill_prompt

def construct_resume_score_prompt(resume, job_description):
    resume_score_prompt = f'''Act as a HR Manager with 20 years of experience.
    Compare the resume provided below with the job description given below.
    Check for key skills in the resume that are related to the job description.
    Rate the resume out of 100 based on the matching skill set.
    Assess the score with high accuracy.
    Here is the Resume text: {resume}
    Here is the Job Description: {job_description}
    I want the response as a single string in the following structure: score:%'''
    return resume_score_prompt

# Function to interact with Gemini Pro model and get response
def get_result(input):
    model = get_gemini_pro()
    response = model.generate_content(input)
    return response.text

# Function to build a resume using a template
def build_resume(first_name, last_name, aspiring_role, email, mob_prefix, mobile,
                 city, country, linkedin, about_me, skill_1, skill_2, skill_3, skill_4, skill_5, company_name, job_role, job_details, lang_1, lang_2, lang_3,
                 ed_12_perc, ed_12_school, pre_degree, pre_degree_cpi, pre_degree_uni, post_degree, post_degree_cpi, post_degree_uni, temp_option):

    # Load the template
    doc = DocxTemplate(f'{temp_option}.docx')
 
    # Define the context with dynamic values
    context = {
        'first_name': first_name,
        'last_name': last_name, 
        'aspiring_role': aspiring_role,
        'email': email,
        'mob_prefix': mob_prefix,
        'mobile': mobile,
        'city': city,
        'country': country,
        'linkedin': linkedin,
        'about_me': about_me,
        'skill_1' : skill_1,
        'skill_2' : skill_2,
        'skill_3' : skill_3,
        'skill_4' : skill_4,
        'skill_5' : skill_5,
        'company_name': company_name,
        'job_role': job_role,
        'job_details': job_details,
        'lang_1': lang_1,
        'lang_2': lang_2,
        'lang_3': lang_3,
        'ed_12_perc': ed_12_perc,
        'ed_12_school': ed_12_school,
        'pre_degree': pre_degree,
        'pre_degree_cpi': pre_degree_cpi,
        'pre_degree_uni': pre_degree_uni,
        'post_degree': post_degree,
        'post_degree_cpi': post_degree_cpi,
        'post_degree_uni': post_degree_uni
    }

    # Render the document with the dynamic content
    doc.render(context)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
            label="Download Resume",
            key="download_resume",
            data=buffer.read(),  # Read the content of the buffer
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


def main():
    st.set_page_config(page_title="Resume Builder")

    first_name = st.text_input('Enter first name')
    last_name = st.text_input('Enter last name')
    aspiring_role = st.text_input('Enter the job you want to do')
    email = st.text_input('Enter your email')

    mobile_prefix_options = ['+91', '+1', '+44', '+81']  # Add your desired prefixes

    col1, col2 = st.columns(2)

    with col1:
        mob_prefix = st.selectbox('Select Mobile Prefix', mobile_prefix_options)

    with col2:
        mobile = st.text_input('Enter your mobile number')

    col3, col4 = st.columns(2)

    with col3:
        city = st.text_input('Enter your city')

    with col4:
        country = st.text_input('Enter your country')

    linkedin = st.text_input('Enter your LinkedIn link')
    about_me = st.text_area('Enter something about you')

    with st.container():
        st.subheader('Enter any 5 relevant skills')
        skill_1 = st.text_input('Skill 1')
        skill_2 = st.text_input('Skill 2')
        skill_3 = st.text_input('Skill 3')
        skill_4 = st.text_input('Skill 4')
        skill_5 = st.text_input('Skill 5')

    with st.container():
        st.subheader('Enter your most recent work experience or any other relevant experience')
        company_name = st.text_input('Company name')
        job_role = st.text_input('Job Role')
        job_details = st.text_input('Job Details')

    with st.container():
        st.subheader('Enter any 3 languages you are fluent in (Leave blank if fewer languages known)')
        lang_1 = st.text_input('Language 1')
        lang_2 = st.text_input('Language 2')
        lang_3 = st.text_input('Language 3')

    with st.container():
        st.subheader('Enter your education degrees')

        col5, col6 = st.columns(2)

        with col5:
            ed_12_perc = st.text_input('Enter your 12th percentage')

        with col6:
            ed_12_school = st.text_input('Enter your 12th school')

        col7, col8, col9 = st.columns(3)

        with col7:
            pre_degree = st.text_input('Enter your pre-degree')
        with col8:
            pre_degree_cpi = st.text_input('Enter your university CPI')
        with col9:
            pre_degree_uni = st.text_input('Enter your university')

        col10, col11, col12 = st.columns(3)

        with col10:
            post_degree = st.text_input('Enter your post-degree')
        with col11:
            post_degree_cpi = st.text_input('Enter your post-degree university CPI')
        with col12:
            post_degree_uni = st.text_input('Enter your post-degree university')

    st.header('View the template to choose your resume format')

    col13, col14 = st.columns(2)

    with col13:
        image = Image.open('images/blue_d1.png')
        st.image(image, caption='Template blue_d1', width=200)

    with col14:
        image = Image.open('images/orange_d1.png')
        st.image(image, caption='Template orange_d1', width=200)

    col15, col16 = st.columns(2)

    with col15:
        image = Image.open('images/green_d3.png')
        st.image(image, caption='Template green_d3', width=200)

    with col16:
        image = Image.open('images/blue_d2.png')
        st.image(image, caption='Template blue_d2', width=200)

    temp_option = st.selectbox(
        'Choose your resume template',
        ('blue_d1', 'blue_d2', 'orange_d1', 'green_d3'))

    if st.button("Build Resume"):
        build_resume(first_name, last_name, aspiring_role, email, mob_prefix, mobile,
                     city, country, linkedin, about_me, skill_1, skill_2, skill_3, skill_4, skill_5,
                     company_name, job_role, job_details, lang_1, lang_2, lang_3, ed_12_perc, ed_12_school,
                     pre_degree, pre_degree_cpi, pre_degree_uni, post_degree, post_degree_cpi, post_degree_uni,
                     temp_option)


if __name__ == '__main__':
    st.set_page_config(
        page_title="Gemini AI",
        page_icon="🧠",
        layout="centered",
    )

    with st.sidebar:
        selected = option_menu(
            'AI-Powered Resume Screening and Assistance Tool',
            ['🧑‍💻Score Checker', '🕵Skill Checker', 'ChatBot', 'Image Captioning', 'Embed text', 'Ask me anything'],
            menu_icon='robot',
            icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill', 'bi-clipboard2-data', 'hash'],
            default_index=0
        )

    # Function to translate roles between Gemini-Pro and Streamlit terminology
    def translate_role_for_streamlit(user_role):
        if user_role == "model":
            return "assistant"
        else:
            return user_role

    # ChatBot page
    if selected == 'ChatBot':
        model = load_gemini_pro_model()

        # Initialize chat session in Streamlit if not already present
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])

        # Display the chatbot's title on the page
        st.title("🤖 ChatBot")

        # Display the chat history
        for message in st.session_state.chat_session.history:
            with st.chat_message(translate_role_for_streamlit(message.role)):
                st.markdown(message.parts[0].text)

        # Input field for user's message
        user_prompt = st.chat_input("Ask Gemini-Pro...")
        if user_prompt:
            # Add user's message to chat and display it
            st.chat_message("user").markdown(user_prompt)

            # Send user's message to Gemini-Pro and get the response
            gemini_response = st.session_state.chat_session.send_message(user_prompt)

            # Display Gemini-Pro's response
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)

    # Image captioning page
    if selected == "Image Captioning":
        st.title("📷 Snap Narrate")

        uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

        if st.button("Generate Caption"):
            image = Image.open(uploaded_image)

            col1, col2 = st.columns(2)

            with col1:
                resized_img = image.resize((800, 500))
                st.image(resized_img)

            default_prompt = "write a short caption for this image"  # change this prompt as per your requirement

            # get the caption of the image from the gemini-pro-vision LLM
            caption = gemini_pro_vision_response(default_prompt, image)

            with col2:
                st.info(caption)

    # Embed text page
    if selected == "Embed text":
        st.title("🔡 Embed Text")

        # text box to enter prompt
        user_prompt = st.text_area(label='', placeholder="Enter the text to get embeddings")

        if st.button("Get Response"):
            response = embeddings_model_response(user_prompt)
            st.markdown(response)

    # Ask me anything page
    if selected == "Ask me anything":
        st.title("❓ Ask me a question")

        # text box to enter prompt
        user_prompt = st.text_area(label='', placeholder="Ask me anything...")

        if st.button("Get Response"):
            response = gemini_pro_response(user_prompt)
            st.markdown(response)

    # Resume Score Checker page
    if selected == '🧑‍💻Score Checker':
        st.title("🧑‍💻 Resume Score Checker")

        job_description = st.text_area('Enter the Job Description')
        uploaded_file = st.file_uploader('Upload Your Resume', type=['pdf'])

        if st.button('Get Score'):
            if job_description == '':
                st.error('Enter Job Description')
            elif uploaded_file is None:
                st.error('Upload your Resume')
            else:
                try:
                    resume = pdf_to_text(uploaded_file)
                    score_prompt = construct_resume_score_prompt(resume, job_description)
                    result = get_result(score_prompt)
                    final_result = result.split(":")[1]
                    if '%' not in final_result:
                        final_result = final_result + '%'
                    result_str = f"""
                    <style>
                    p.a {{
                      font: bold 25px Arial;
                    }}
                    </style>
                    <p class="a">Your Resume matches {final_result} with the Job Description</p>
                    """
                    st.markdown(result_str, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f'Error: {e}')

    # Skill Checker page
    if selected == '🕵Skill Checker':
        st.title("🕵 Skill Checker")

        job_description = st.text_area('Enter the Job Description')
        uploaded_file = st.file_uploader('Upload Your Resume', type=['pdf'])

        if st.button('Get Missing Skills'):
            if job_description == '':
                st.error('Enter Job Description')
            elif uploaded_file is None:
                st.error('Upload your Resume')
            else:
                try:
                    resume = pdf_to_text(uploaded_file)
                    skill_prompt = construct_skills_prompt(resume, job_description)
                    result = get_result(skill_prompt)
                    st.write('Your Resume misses the following keywords:')
                    st.markdown(result, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f'Error: {e}')

if __name__ == '__main__':
    main()
