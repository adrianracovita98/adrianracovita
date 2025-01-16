import random
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Path to the Excel file for logging
ANSWER_LOG_FILE = "answers_log.xlsx"

# Advanced clinician scenarios and questions for PNH, aHUS, and gMG
scenarios = {
    "PNH": [
        {
            "question": "A 35-year-old patient with PNH presents with worsening fatigue and hemoglobin levels of 8 g/dL despite treatment with a complement inhibitor. The clinician is concerned about breakthrough hemolysis. What is the best response?",
            "options": [
                "A. Suggest increasing the dose of the current complement inhibitor.",
                "B. Recommend a switch to a newer complement inhibitor with better C5 binding.",
                "C. Advise the clinician to focus on supportive care, such as transfusions.",
                "D. Suggest stopping complement inhibition therapy entirely."
            ],
            "answer": "B. Recommend a switch to a newer complement inhibitor with better C5 binding.",
            "feedback": "Correct! Breakthrough hemolysis can occur due to incomplete complement inhibition, and switching to a more potent complement inhibitor may improve outcomes."
        },
        {
            "question": "A clinician describes a 50-year-old patient with PNH who has recently developed a deep vein thrombosis (DVT) despite complement inhibition therapy. What is the most appropriate next step?",
            "options": [
                "A. Initiate anticoagulation therapy in addition to complement inhibition.",
                "B. Stop complement inhibition and focus solely on anticoagulation.",
                "C. Increase the dose of the complement inhibitor to prevent further thrombosis.",
                "D. Suggest splenectomy to reduce the risk of thrombosis."
            ],
            "answer": "A. Initiate anticoagulation therapy in addition to complement inhibition.",
            "feedback": "Correct! Complement inhibition reduces thrombotic risk but does not eliminate it entirely. Anticoagulation is recommended for patients with thrombotic events."
        },
        {
            "question": "A patient with PNH reports dark-colored urine in the mornings and mild fatigue. The clinician asks whether complement inhibition is necessary for this patient. What is the best advice?",
            "options": [
                "A. Recommend immediate initiation of complement inhibition to prevent complications.",
                "B. Suggest waiting until the patient develops life-threatening thrombosis.",
                "C. Focus on supportive care, such as iron and folate supplementation.",
                "D. Advise against complement inhibition in low-risk patients."
            ],
            "answer": "A. Recommend immediate initiation of complement inhibition to prevent complications.",
            "feedback": "Correct! Complement inhibition is critical to prevent complications like hemolysis and thrombosis, even in patients with mild symptoms."
        },
        {
            "question": "A 45-year-old patient with PNH has been stable on complement inhibition but begins reporting mild fatigue and low-grade hemolysis. What is the most appropriate recommendation?",
            "options": [
                "A. Monitor the patient closely without making changes.",
                "B. Suggest increasing the dose of the current complement inhibitor.",
                "C. Recommend switching to a newer, long-acting complement inhibitor.",
                "D. Advise the patient that symptoms are normal and require no intervention."
            ],
            "answer": "C. Recommend switching to a newer, long-acting complement inhibitor.",
            "feedback": "Correct! Long-acting complement inhibitors may provide better control of low-grade hemolysis and improve patient outcomes."
        },
        {
            "question": "A clinician asks whether complement inhibition is effective for PNH patients who are transfusion-independent but have mild anemia. What is the best response?",
            "options": [
                "A. Yes, complement inhibition can prevent future complications, even in transfusion-independent patients.",
                "B. No, complement inhibition is only for patients requiring transfusions.",
                "C. Complement inhibition should be reserved for patients with active thrombosis.",
                "D. Complement inhibition is not necessary for anemia alone."
            ],
            "answer": "A. Yes, complement inhibition can prevent future complications, even in transfusion-independent patients.",
            "feedback": "Correct! Complement inhibition can benefit patients with mild anemia by preventing hemolysis and reducing the risk of thrombosis."
        }
    ],
    "aHUS": [
        {
            "question": "A 10-year-old patient with aHUS presents with worsening renal function and persistent hemolysis despite complement inhibition. The clinician asks for guidance. What is the best recommendation?",
            "options": [
                "A. Recommend genetic testing to identify complement pathway mutations.",
                "B. Increase the dose of the current complement inhibitor.",
                "C. Focus on supportive care, such as dialysis.",
                "D. Suggest stopping complement inhibition therapy."
            ],
            "answer": "A. Recommend genetic testing to identify complement pathway mutations.",
            "feedback": "Correct! Genetic testing can help identify underlying complement pathway mutations, which can guide further therapeutic strategies."
        },
        {
            "question": "A clinician describes a 25-year-old patient with aHUS who has been on complement inhibition for 6 months but is now showing signs of relapse. What is the best next step?",
            "options": [
                "A. Switch to a different complement inhibitor with improved efficacy.",
                "B. Stop complement inhibition and observe the patient.",
                "C. Add immunosuppressive therapy to address possible secondary causes.",
                "D. Focus solely on supportive care, such as blood transfusions."
            ],
            "answer": "A. Switch to a different complement inhibitor with improved efficacy.",
            "feedback": "Correct! Switching to a more effective complement inhibitor can help control relapse and improve long-term outcomes in aHUS."
        },
        {
            "question": "A pediatric nephrologist mentions a 12-year-old patient with aHUS who is not responding adequately to complement inhibition. What is the best course of action?",
            "options": [
                "A. Recommend genetic testing to identify complement pathway mutations.",
                "B. Increase the dose of the complement inhibitor.",
                "C. Focus on dialysis and supportive care only.",
                "D. Suggest stopping complement inhibition therapy."
            ],
            "answer": "A. Recommend genetic testing to identify complement pathway mutations.",
            "feedback": "Correct! Genetic testing can identify complement pathway mutations, which may provide insights into treatment optimization for refractory aHUS."
        },
        {
            "question": "A pregnant patient presents with suspected aHUS. The clinician is concerned about initiating complement inhibition therapy due to potential risks to the fetus. What is the best response?",
            "options": [
                "A. Emphasize that complement inhibition is safe and can prevent severe maternal and fetal complications.",
                "B. Suggest delaying therapy until after delivery.",
                "C. Recommend supportive care and plasma exchange only.",
                "D. Advise against complement inhibition during pregnancy."
            ],
            "answer": "A. Emphasize that complement inhibition is safe and can prevent severe maternal and fetal complications.",
            "feedback": "Correct! Complement inhibition is considered safe during pregnancy and can prevent life-threatening complications for both the mother and fetus."
        },
        {
            "question": "A 30-year-old patient with recurrent aHUS is concerned about the long-term safety of complement inhibition. What is the most appropriate advice?",
            "options": [
                "A. Highlight the extensive safety data available for long-term complement inhibition.",
                "B. Suggest periodic breaks from therapy to reduce risks.",
                "C. Recommend stopping therapy once the patient achieves remission.",
                "D. Advise switching to supportive care only."
            ],
            "answer": "A. Highlight the extensive safety data available for long-term complement inhibition.",
            "feedback": "Correct! Long-term complement inhibition has been shown to be safe and effective in preventing relapses in patients with aHUS."
        }
    ],
    "gMG": [
        {
            "question": "A 45-year-old patient with generalized myasthenia gravis (gMG) is experiencing frequent exacerbations despite standard immunosuppressive therapy. The clinician is considering complement inhibition. What is the best advice?",
            "options": [
                "A. Complement inhibition is appropriate for patients with refractory gMG who have failed other therapies.",
                "B. Complement inhibition should only be used in newly diagnosed patients.",
                "C. Complement inhibition is not effective for refractory gMG.",
                "D. Suggest increasing the dose of current immunosuppressive therapy instead."
            ],
            "answer": "A. Complement inhibition is appropriate for patients with refractory gMG who have failed other therapies.",
            "feedback": "Correct! Complement inhibition is an effective option for patients with refractory gMG who have not responded to other treatments."
        },
        {
            "question": "A clinician asks about the mechanism of action of complement inhibition in gMG. What is the best explanation?",
            "options": [
                "A. Complement inhibition prevents the formation of the membrane attack complex, reducing damage at the neuromuscular junction.",
                "B. Complement inhibition increases acetylcholine production.",
                "C. Complement inhibition reduces autoantibody production.",
                "D. Complement inhibition enhances muscle strength directly."
            ],
            "answer": "A. Complement inhibition prevents the formation of the membrane attack complex, reducing damage at the neuromuscular junction.",
            "feedback": "Correct! Complement inhibition prevents the formation of the membrane attack complex, which reduces immune-mediated damage at the neuromuscular junction in gMG."
        },
        {
            "question": "A 60-year-old patient with gMG has been on complement inhibition therapy for 3 months and reports significant symptom improvement. However, the clinician is concerned about long-term infection risk. What is the best response?",
            "options": [
                "A. Highlight the importance of continued vaccination and ongoing infection monitoring.",
                "B. Recommend stopping complement inhibition to avoid infection risk.",
                "C. Suggest reducing the frequency of complement inhibition therapy.",
                "D. Advise the clinician not to worry about infections."
            ],
            "answer": "A. Highlight the importance of continued vaccination and ongoing infection monitoring.",
            "feedback": "Correct! Vaccination and monitoring are essential to mitigate infection risks while maintaining the benefits of complement inhibition in gMG."
        },
        {
            "question": "A neurologist mentions a patient with gMG who has failed multiple lines of therapy and is now considering complement inhibition. They are concerned about the cost-effectiveness of therapy. What is the best response?",
            "options": [
                "A. Emphasize the clinical efficacy and improved quality of life seen with complement inhibition in refractory gMG patients.",
                "B. Suggest using complement inhibition only in younger patients.",
                "C. Recommend alternative therapies to reduce costs.",
                "D. Agree that complement inhibition is too expensive for routine use."
            ],
            "answer": "A. Emphasize the clinical efficacy and improved quality of life seen with complement inhibition in refractory gMG patients.",
            "feedback": "Correct! Complement inhibition has demonstrated significant clinical efficacy and can greatly improve quality of life in refractory gMG patients, justifying its cost."
        },
        {
            "question": "A 35-year-old patient with gMG reports difficulty swallowing and severe muscle weakness, which are affecting their daily life. The clinician is evaluating complement inhibition. What is the best advice?",
            "options": [
                "A. Complement inhibition is a suitable option for patients with severe gMG symptoms that impact their quality of life.",
                "B. Complement inhibition is only recommended for mild cases of gMG.",
                "C. Suggest using steroids instead of complement inhibition.",
                "D. Advise against complement inhibition due to potential side effects."
            ],
            "answer": "A. Complement inhibition is a suitable option for patients with severe gMG symptoms that impact their quality of life.",
            "feedback": "Correct! Complement inhibition is highly effective for patients with severe gMG symptoms that significantly impact their quality of life."
        },
        {
            "question": "A clinician asks whether complement inhibition can be used in gMG patients who are stable on immunosuppressive therapy but have occasional exacerbations. What is the best response?",
            "options": [
                "A. Complement inhibition is effective for refractory gMG and can reduce exacerbations in patients not fully controlled by immunosuppressive therapy.",
                "B. Complement inhibition should be stopped once a patient is stable.",
                "C. Complement inhibition is only for newly diagnosed patients.",
                "D. Suggest increasing the dose of immunosuppressive therapy instead of using complement inhibition."
            ],
            "answer": "A. Complement inhibition is effective for refractory gMG and can reduce exacerbations in patients not fully controlled by immunosuppressive therapy.",
            "feedback": "Correct! Complement inhibition is beneficial for refractory gMG, even in patients with partial control on immunosuppressive therapy, as it reduces exacerbations and improves outcomes."
        }
    ]
}

# Initialize the answer log file if it doesn't exist
def initialize_answer_log():
    if not os.path.exists(ANSWER_LOG_FILE):
        # Create a DataFrame with the required columns
        df = pd.DataFrame(columns=[
            "Timestamp", "User Name", "Topic", "Question", "User Answer",
            "Correct Answer", "Is Correct"
        ])
        df.to_excel(ANSWER_LOG_FILE, index=False)


# Function to record an answer in the Excel log
def record_answer(user_name, topic, question, user_answer, correct_answer, is_correct):
    if os.path.exists(ANSWER_LOG_FILE):
        # Load the existing Excel file
        df = pd.read_excel(ANSWER_LOG_FILE)
    else:
        # Create a new DataFrame with the required columns if the file doesn't exist
        df = pd.DataFrame(columns=[
            "Timestamp", "User Name", "Topic", "Question", "User Answer",
            "Correct Answer", "Is Correct"
        ])

    # Create a new row as a DataFrame
    new_row = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "User Name": user_name,
        "Topic": topic,
        "Question": question,
        "User Answer": user_answer,
        "Correct Answer": correct_answer,
        "Is Correct": is_correct
    }])

    # Concatenate the new row to the existing DataFrame
    df = pd.concat([df, new_row], ignore_index=True)

    # Save the updated DataFrame back to the Excel file
    df.to_excel(ANSWER_LOG_FILE, index=False)
    
def get_randomized_questions(topic_questions):
    return random.sample(topic_questions, len(topic_questions))

def main():
    # Initialize session state variables
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "question_count" not in st.session_state:
        st.session_state.question_count = 0
    if "history" not in st.session_state:
        st.session_state.history = []  # Always initialize history as an empty list
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "show_next_question" not in st.session_state:
        st.session_state.show_next_question = False
    if "selected_topic" not in st.session_state:
        st.session_state.selected_topic = None

    # Title and sidebar setup
    st.title("Advanced Key Account Manager Training Tool")
    #st.sidebar.title("Navigation")
    #st.sidebar.markdown("Train on **advanced medical scenarios** for PNH, aHUS, and gMG.")
    
    # Topic selection
    st.sidebar.subheader("Topics")
    topics = list(scenarios.keys())
    selected_topic = st.sidebar.selectbox("Choose a topic:", topics)
    
    # User login and collaboration
    st.sidebar.subheader("Collaborate")
    user_name = st.sidebar.text_input("Enter your name:", placeholder="Your Name")
    if user_name:
        st.sidebar.write(f"Welcome, **{user_name}**! Ready to challenge yourself?")
        with st.sidebar.expander("💬 Leave a Comment"):
            comment = st.text_area("Your comment", placeholder="Share your thoughts...")
            if st.button("Submit Comment"):
                st.sidebar.write(f"**{user_name} says:** {comment}")

    # Reset when the topic changes
    if selected_topic != st.session_state.selected_topic:
        st.session_state.selected_topic = selected_topic
        # Shuffle and store the questions for this topic
        st.session_state.shuffled_questions = get_randomized_questions(scenarios[selected_topic])
        st.session_state.current_question_index = 0  # Start at the first question
        st.session_state.history = []
        st.session_state.score = 0
        st.session_state.question_count = 0

    # Display a random question from the selected topic
    if st.session_state.selected_topic:
        # Generate a new question only if none is stored
        if st.session_state.current_question is None:
            st.session_state.current_question = random.choice(scenarios[st.session_state.selected_topic])
            st.session_state.show_next_question = False

        # Extract the current question
        question_data = st.session_state.current_question

        # Display the question and options
        st.subheader(f"📋 Clinician Question: {question_data['question']}")
        options = question_data["options"]
        user_answer = st.radio("Select your answer:", options)

        # Submit button to check the answer
        if st.button("Submit Answer"):
            if not st.session_state.show_next_question:
                # Increment the question count
                st.session_state.question_count += 1
        
                # Calculate if the user's answer is correct
                is_correct = user_answer == question_data["answer"]
        
                # Check if the user's answer is correct
                if is_correct:
                    st.success("✅ Correct! Great job!")
                    st.session_state.score += 1
                else:
                    st.error("❌ Incorrect. Keep improving!")
        
                # Append the question, user's answer, and feedback to the history
                st.session_state.history.append({
                    "question": question_data["question"],
                    "your_answer": user_answer or "No answer submitted",  # Handle empty user answer
                    "correct_answer": question_data["answer"],
                    "feedback": question_data["feedback"],
                    "is_correct": is_correct
                })
        
                # Provide feedback
                st.info(f"Feedback: {question_data['feedback']}")
                st.info(f"The correct answer is: {question_data['answer']}")
        
                # Show the "Next Question" button
                st.session_state.show_next_question = True

        # Display the "Next Question" button after submission
        if st.session_state.show_next_question:
            if st.button("Next Question"):
                # Clear the current question so that a new one can be generated
                st.session_state.current_question = None
                st.session_state.show_next_question = False

    # Display progress in the sidebar
   # st.sidebar.subheader("📊 Progress")
   # progress = st.session_state.score / max(1, st.session_state.question_count) * 100
   # st.sidebar.progress(progress / 100)  # Display progress bar
   # st.sidebar.markdown(f"**Score:** {st.session_state.score}/{st.session_state.question_count} correct")

    # Leaderboard (mocked for now)
    #st.sidebar.subheader("🏆 Leaderboard")
    #leaderboard = [
     #   {"name": "Alice", "score": 8},
      #  {"name": "Bob", "score": 7},
       # {"name": f"{user_name}", "score": st.session_state.score} if user_name else None
    #]
    #for entry in leaderboard:
     #   if entry:
      #      st.sidebar.markdown(f"**{entry['name']}**: {entry['score']} points")

    # Show question history if the user enables it in the sidebar
    if st.sidebar.checkbox("📜 Show Answer History"):
    st.subheader("Answer History")
    
    # Check if there is any history to display
    if st.session_state.history:
        for idx, entry in enumerate(st.session_state.history, 1):
            # Validate required keys before accessing them
            if all(key in entry for key in ["question", "your_answer", "correct_answer", "feedback"]):
                st.markdown(f"**Question {idx}:** {entry['question']}")
                st.markdown(f"- **Your Answer:** {entry['your_answer']}")
                st.markdown(f"- **Correct Answer:** {entry['correct_answer']}")
                st.markdown(f"- **Feedback:** {entry['feedback']}")
                st.markdown("---")
            else:
                st.warning(f"Skipping invalid history entry at index {idx}.")
    else:
        st.info("No answers have been submitted yet.")
            

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("🔧 Created to enhance the training experience for Key Account Managers.")
    st.sidebar.markdown("**Version:** 1.0 | **Contact:** adrian.racovita@astrazeneca.com")
# Run the app
if __name__ == "__main__":
    main()
