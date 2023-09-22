import openai
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Replace with your OpenAI API key
api_key = "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"

# Define a dictionary of subjects and their descriptions
subjects = {
    "science": "Science is the systematic study of the natural world and how it works.",
    "math": "Mathematics is the language of patterns, relationships, and quantitative reasoning.",
    "history": "History is the record of past events and the story of humanity's past.",
    "literature": "Literature encompasses written or spoken works, including novels, poetry, and plays."
}

# Define resources for each subject (initially empty)
resources = {
    "science": "",
    "math": "",
    "history": "",
    "literature": ""
}

# Define quiz questions for each subject (same as before)
quiz_questions = {
    "science": [],
    "math": [],
    "history": [],
    "literature": []
}

# Initialize an empty student profile (same as before)
student_profile = {}

# Initialize the OpenAI API
openai.api_key = api_key

def generate_quiz_questions(topic):
    openai.api_key = api_key

    # Create a prompt asking the model to generate quiz questions
    prompt = f"Generate quiz questions about {topic}."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,  # Adjust max_tokens to control response length
        temperature=0.7,  # Adjust temperature for response randomness
        stop=None  # Allow the model to generate longer responses
    )

    return response.choices[0].text

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    return sentiment

def update_student_profile(student_name, subject):
    if student_name not in student_profile:
        student_profile[student_name] = []
    student_profile[student_name].append(subject)

def get_subject_info(subject, prompt_type="overview"):
    openai.api_key = api_key
    subject = subject.lower()

    if subject not in subjects:
        # Offer suggestions for similar subjects
        similar_subjects = [s for s in subjects.keys() if subject in s]
        suggestion = f"Did you mean {' or '.join(similar_subjects)}?"

        return f"I'm sorry, I can't provide information on {subject}. {suggestion}"

    prompt = subjects[subject]

    if prompt_type == "overview":
        prompt += " Please provide an overview of this subject."
    elif prompt_type == "importance":
        prompt += " Why is this subject important?"
    elif prompt_type == "key_points":
        prompt += " What are the key points students should know about this subject?"
    elif prompt_type == "examples":
        prompt += " Can you provide some real-life examples related to this subject?"
    elif prompt_type == "study_tips":
        prompt += " Share some effective study tips for this subject."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the "gpt-3.5-turbo" model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    sentiment_analysis = analyze_sentiment(response['choices'][0]['message']['content'])

    return {
        "response": response.choices[0].text,
        "sentiment": sentiment_analysis
    }

def generate_resources(subject):
    # Create a prompt asking the model to generate educational resources
    prompt = f"Suggest educational resources for learning {subject}."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the "gpt-3.5-turbo" model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    print("Welcome to the High School Helper!")

    while True:
        student_name = input("Enter your name: ")
        subject = input("Enter a subject (science, math, history, literature) or 'exit' to quit: ")

        if subject.lower() == "exit":
            break

        prompt_type = input("Enter the type of information you want (overview, importance, key_points, examples, study_tips, quiz, resources): ")

        if prompt_type == "quiz":
            quiz_questions[subject.lower()] = generate_quiz_questions(subject)
            print(f"\nQuiz Questions about {subject}:\n{quiz_questions[subject.lower()]}")
        elif prompt_type == "resources":
            resources[subject.lower()] = generate_resources(subject)
            print(f"\nEducational Resources for {subject}:\n{resources[subject.lower()]}")
        else:
            result = get_subject_info(subject, prompt_type)

            print("\nResponse:")
            print(result["response"])

            sentiment = result["sentiment"]
            print("\nSentiment Analysis:")
            print(f"Positive: {sentiment['pos']:.2f}")
            print(f"Neutral: {sentiment['neu']:.2f}")
            print(f"Negative: {sentiment['neg']:.2f}")
            print(f"Compound: {sentiment['compound']:.2f}")

            update_student_profile(student_name, subject)
            print(f"\n{student_name}'s Learning Profile:")
            for student, subjects_learned in student_profile.items():
                print(f"{student}: {', '.join(subjects_learned)}")

