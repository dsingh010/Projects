"""

User Input: Collects the child’s name, age, preferred story type ,emotional tone, and story length 
Classifier: Uses GPT and prompt engineering to classify the user's request into a story category  
Story Generator: Uses GPT to create a personalized bedtime story based on the selected category, child’s profile, and emotional tone using a 6 part narritive structure
Text-to-Speech: Converts the story into spoken audio  
Alternate Ending: Uses GPT with a prompt that rewrites the final two sections of the story in a randomly selected creative format  
Story Judge: Evaluates the story by scoring it against a predefined rubric
Story Reviser: Sends the story and feedback back to improve the story, users can repeat this cycle with new feedback until they're satisfied with the final version

System Flow:
        [ User Input ]
               |
         [ Classifier ]
               |
        [ Story Generator ]
            /         \
   [ Text-to-Speech ]  [ Judge Evaluation ]
                            |
                    [ Story Reviser ]
                          |___________________________|
                            |              |   |
                            |              |   |
                            |              |   |
                    [User Satisfied]   [User not satisfied (Loop)]
                            |
                        [End w/ Final Story]
    
"""
import os
import json
from gtts import gTTS
import tempfile
import openai
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Call model
def call_model(prompt: str, max_tokens: int = 3000, temperature: float = 0.1) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()

# Classify story category
def classify_request(request: str) -> str:
    prompt = f"""
You are a bedtime story classifier for kids aged 5–10. Try to match the request below to one of these categories:

- sleep routine, dreams, animals, nature, family, emotions, fantasy,
  adventure, seasonal, classic fairy tales, fables, nursery rhymes,
  space, science, modern classics

If none fit, create a short custom category.

Request: \"{request}\"

Return format: CATEGORY: <category>
"""
    response = call_model(prompt)
    return response.split(":")[1].strip()

# Generate story
def generate_story(request: str, category: str, child_name: str = None, age: int = None,
                   emotional_tone: str = None, story_length: str = "medium") -> str:
    name_line = f"- Name: {child_name}\n" if child_name else ""
    age_line = f"- Age: {age}\n" if age else ""
    emotional_tone_line = f"- Emotional Tone or Theme: {emotional_tone}\n" if emotional_tone else ""

    word_limit_map = {"short": 300, "medium": 600, "long": 1000}
    if story_length not in word_limit_map:
        story_length = "medium"
    word_limit = word_limit_map[story_length]

    prompt = f"""
You are a warm, thoughtful children's storyteller. Write a short, original bedtime story for a child with the following profile:
{name_line}{age_line}- Story Category: {category}
{emotional_tone_line}
The story should follow this structure:
1. Setting the Scene
2. Daily Life
3. Surprise
4. Resolution
5. Wind-Down
6. Takeaway

Guidelines:
- Use simple, age-appropriate language{f" for a {age}-year-old" if age else ""}.
- Refer to {child_name if child_name else "the child"} personally in the story.
- The story should be gentle, emotionally warm, and less than {word_limit} words.

Output only the story — no title, no notes, no commentary.
"""
    return call_model(prompt, temperature=0.7)

# Judge story
def judge_story(story: str) -> dict:
    prompt = f"""
Evaluate this bedtime story (ages 5–10).

Score 1–10:
- Calmness
- Age Appropriateness
- Structure
- Imagination
- Emotional Warmth

Give a 1-sentence improvement suggestion.

Return JSON:
{{
  "scores": {{
    "calmness": <int>,
    "age_appropriateness": <int>,
    "structure": <int>,
    "imagination": <int>,
    "warmth": <int>
  }},
  "average_score": <float>,
  "feedback": "..."
}}

Story:
\"\"\"{story}\"\"\"
"""
    try:
        return json.loads(call_model(prompt))
    except:
        return {
            "scores": {},
            "average_score": 0,
            "feedback": "Judge response could not be parsed."
        }

# Revise story
def revise_story(story: str, feedback: str) -> str:
    prompt = f"""
Revise the bedtime story below using this feedback:

\"\"\"{feedback}\"\"\"

Story:
\"\"\"{story}\"\"\"
"""
    return call_model(prompt, temperature=0.6)

# Generate alternate ending
def generate_alternate_ending(story: str) -> str:
    prompt = f"""
Rewrite the last two sections (Resolution and Takeaway) of this bedtime story with a truly different ending. Randomly choose one of the following formats:

- A silly twist ending  
- An open-ended mystery  
- A calming dream sequence  
- A new character who changes everything  
- A poetic lullaby-style ending  
- A role reversal  
- A letter from the future  
- The hero wakes up — it was all a dream… or was it?

Guidelines:
- Make the ending emotionally warm, mysterious, funny, or magical
- Ensure it's gentle and appropriate for children aged 5–10
- Keep the ending under 200 words
- Do not repeat the original story's moral or lesson

Original Story:
\"\"\"{story}\"\"\"
"""
    return call_model(prompt, temperature=0.8)

# Text-to-speech
def speak_story_gtts(story_text: str):
    formatted = story_text.replace(". ", "... ").replace("!", "... ").replace("?", "... ")
    tts = gTTS(text=formatted, lang='en', slow=True)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        os.system(f"start {fp.name}" if os.name == 'nt' else f"afplay {fp.name}")

# Display judge feedback
def display_judge_result(result: dict):
    print("\nStory Evaluation:")
    for k, v in result["scores"].items():
        print(f"  {k.capitalize():<18}: {v}/10")
    print(f"\nAverage Score: {result['average_score']:.1f}/10")
    print("Feedback:", result["feedback"])

# Main story flow
def run_story():
    print("\nWelcome to the Bedtime Story Generator\n")

    child_name = input("What is your name? (press Enter to skip): ").strip()
    age_input = input("How old are you? (5-10, press Enter to skip): ").strip()
    age = int(age_input) if age_input.isdigit() else None
    request = input("What type of bedtime story would you like? (fantasy, space, etc.): ").strip()

    valid_lengths = {"short", "medium", "long"}
    story_length = ""
    while story_length not in valid_lengths:
        story_length = input("What story length do you prefer? (short / medium / long): ").strip().lower()
        if story_length not in valid_lengths:
            print("Please enter a valid option: short, medium, or long.")

    emotional_tone = input("How should the story feel, what emotional need should it support? (e.g., calm, brave, magical): ").strip()

    category = classify_request(request)
    print(f"\nCategory identified: {category}")

    story = generate_story(request, category, child_name, age, emotional_tone, story_length)
    print("\nYour Bedtime Story:\n")
    print(story)

    if input("\nWould you like the story read aloud? (yes/no): ").strip().lower().startswith('y'):
        speak_story_gtts(story)

    if input("\nWould you like an alternate ending? (yes/no): ").strip().lower().startswith('y'):
        alt = generate_alternate_ending(story)
        print("\nAlternate Ending:\n")
        print(alt)
        if input("\nWould you like to hear the alternate ending read aloud? (yes/no): ").strip().lower().startswith('y'):
            speak_story_gtts(alt)

    if input("\nWould you like me to evaluate the story? (yes/no): ").strip().lower().startswith('y'):
        judge_result = judge_story(story)
        display_judge_result(judge_result)

        current_story = story
        while True:
            custom_feedback = input("What feedback would you like to give to improve the story? (Press Enter to use judge's feedback): ").strip()
            feedback_to_use = custom_feedback if custom_feedback else judge_result["feedback"]

            current_story = revise_story(current_story, feedback_to_use)
            print("\nRevised Story:\n")
            print(current_story)

            if input("\nWould you like this revised story read aloud? (yes/no): ").strip().lower().startswith('y'):
                speak_story_gtts(current_story)

            if input("\nWould you like to revise the story again? (yes/no): ").strip().lower() != "yes":
                break

        print("\nFinal Story:\n")
        print(current_story)
    else:
        print("\nNo evaluation requested. Keeping the original story.")

    print("\nThe End, Sweet Dreams!\n")

if __name__ == "__main__":
    run_story()
