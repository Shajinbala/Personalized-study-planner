import streamlit as st
import cohere
import datetime
import pandas as pd

# Fetch API key from Streamlit secrets
try:
    cohere_api_key = st.secrets["cohere"]["api_key"]
except KeyError as e:
    st.error(f"Missing secret: {e}. Please make sure your Streamlit secrets are configured correctly.")
    st.stop()

# Initialize Cohere client
cohere_client = cohere.Client(cohere_api_key)

# Function to generate study plan
def generate_study_plan(course_load, deadlines, preferences, start_date):
    prompt = f"Generate a detailed study plan for the following courses: {course_load}. " \
             f"The deadlines are: {deadlines}. The study preferences are: {preferences}. " \
             f"The study should start from {start_date}."

    try:
        response = cohere_client.chat(
            model="command-r-plus",  # ✅ Ensure this model is supported in your Cohere API plan
            message=prompt  # ✅ Fixed argument
        )
        return response.text  # ✅ Extracts response text correctly
    except Exception as e:
        st.error(f"Error generating study plan: {e}")
        return None

# Function to parse deadlines
def parse_deadlines(deadlines):
    parsed_deadlines = []
    for deadline in deadlines:
        parsed_deadlines.append({'course': deadline['course'], 'date': deadline['date'].strftime('%Y-%m-%d')})
    return parsed_deadlines

# Function to send notification (Placeholder for actual notifications)
def send_notification(message):
    st.write(message)

# Layout: Dashboard
def dashboard_view(course_load, deadlines, preferences, study_plan, deadlines_data):
    st.subheader('📅 Weekly Calendar View')
    df = pd.DataFrame(deadlines_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    st.write(df)

    st.subheader('📝 Study Plan Summary')
    st.write(study_plan)

# Main app layout
st.title('📚 Personalized Study Planner')
st.write('Generate a personalized study plan based on your courses, deadlines, and personal preferences.')

# Adding courses and deadlines dynamically
st.header('🗓 Add Your Courses and Deadlines')

if 'deadlines' not in st.session_state:
    st.session_state.deadlines = []

def add_course():
    st.session_state.deadlines.append({'course': '', 'date': datetime.date.today()})

st.button('Add Course', on_click=add_course)

for idx, deadline in enumerate(st.session_state.deadlines):
    with st.expander(f'Course {idx+1}'):
        course = st.text_input(f'Course Name {idx+1}', key=f'course_{idx}', value=deadline['course'])
        date = st.date_input(f'Deadline Date {idx+1}', key=f'date_{idx}', value=deadline['date'])
        st.session_state.deadlines[idx]['course'] = course
        st.session_state.deadlines[idx]['date'] = date

# Input fields
st.header('📝 Input Your Study Preferences')
preferences = st.text_area('Personal Preferences (e.g., study in the morning, prefer short sessions)', placeholder='Enter any study preferences')

st.header('📆 Choose Study Start Date')
start_date = st.date_input('Start Date', value=datetime.date.today())

if st.button('Generate Study Plan'):
    if st.session_state.deadlines and preferences:
        course_load = [item['course'] for item in st.session_state.deadlines]
        parsed_deadlines = parse_deadlines(st.session_state.deadlines)
        deadlines_text = "; ".join([f"{item['course']} by {item['date']}" for item in parsed_deadlines])
        study_plan = generate_study_plan(", ".join(course_load), deadlines_text, preferences, start_date)
        
        if study_plan:
            dashboard_view(course_load, parsed_deadlines, preferences, study_plan, parsed_deadlines)
    else:
        st.error('Please fill in all the fields.')

# Footer with more info
st.markdown('---')