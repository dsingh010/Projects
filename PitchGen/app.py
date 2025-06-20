
import gradio as gr
import anthropic
import os

# --- Claude API Client Setup ---
# The app will try to get the API key from your environment variables.
# If it's not found, it will use a dummy function for offline testing.
try:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    print("Anthropic API client initialized.")
except KeyError:
    print("WARNING: ANTHROPIC_API_KEY environment variable not found.")
    print("The app will run with a dummy function and return placeholder text.")
    # This dummy client allows the Gradio app to run for UI testing
    # without a real API key.
    class DummyClaude:
        def create(self, *args, **kwargs):
            # Mimics the structure of the actual API response object
            return type('obj', (object,), {
                'content': [
                    type('obj', (object,), {
                        'text': (
                            "### Elevator Pitch\n\n"
                            "This is a **sample pitch** because the "
                            "Anthropic API key is not set. "
                            "Please set the `ANTHROPIC_API_KEY` "
                            "environment variable to get a real response.\n\n"
                            "### Pitch Deck Outline\n\n"
                            "**Slide 1: Title**\n- Your Company Name\n- "
                            "Your Name & Title\n- A compelling tagline."
                        )
                    })
                ]
            })()

    class DummyMessages:
        def create(self, *args, **kwargs):
            return DummyClaude().create(*args, **kwargs)

    class DummyClient:
        messages = DummyMessages()

    client = DummyClient()


def generate_pitch(name, description, problem, solution, audience, model, pitch_for):
    """
    Generates an elevator pitch and slide deck using the Anthropic API.
    """
    if not all([name, description, problem, solution, audience, model]):
        return "Please fill out all the fields above to generate your pitch.", ""

    # This prompt is engineered to get a structured response from Claude.
    prompt = f"""
    You are an expert business consultant specializing in helping solopreneurs craft compelling narratives.
    Based on the following company details, please generate two things:

    1.  **A powerful 30-second elevator pitch.**

    2.  **The content for a 5-slide pitch deck.** For each slide, provide a clear title and then write the specific 3-4 bullet points that should be on the slide itself. **Do not give instructions on what to write; write the actual content.** For example, instead of saying "Explain the business model," you should write "- We operate on a freemium model. - Core features are free, with advanced analytics available for a $10/month subscription."

    **IMPORTANT:** You MUST tailor the tone, language, and focus of both the elevator pitch and the deck outline for the following audience: **{pitch_for}**.
    - If for 'Venture Capitalists', focus on scalability, market size, and return on investment (e.g., mention TAM/SAM/SOM if possible).
    - If for 'Potential Customers', focus on the direct benefits and how it solves their specific problem easily.
    - If for 'A Networking Event', make it more conversational, memorable, and focused on sparking interest for a follow-up conversation.

    **Company Details:**
    - **Company Name:** {name}
    - **What it does:** {description}
    - **The Problem it Solves:** {problem}
    - **The Solution it Offers:** {solution}
    - **Target Audience:** {audience}
    - **Business Model:** {model}

    Please format the output in Markdown, using "### Elevator Pitch" and "### Pitch Deck Outline" as the section headings.
    """

    try:
        # Use a reliable model name, please update if you found a different one works for you
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        full_text = response.content[0].text

        # Split the response into the two sections for separate display
        pitch_section = "### Pitch Deck Outline"
        if pitch_section in full_text:
            pitch = full_text.split(pitch_section)[0]
            deck = pitch_section + full_text.split(pitch_section)[1]
        else:
            pitch = full_text
            deck = "Could not parse the pitch deck from the response."

        return pitch, deck

    except Exception as e:
        error_message = f"An error occurred with the API call: {str(e)}"
        print(error_message)
        return error_message, ""


# --- Gradio User Interface ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="green"), title="Cactus AI Pitch Generator") as app:
    gr.Markdown("# 🌵 Cactus – AI Copilot for Solopreneurs")
    gr.Markdown("Fill in your startup details, and let AI generate a compelling elevator pitch and a slide deck outline for you.")

    with gr.Row(variant="panel"):
        with gr.Column(scale=1):
            gr.Markdown("### Your Company Details")
            company_name = gr.Textbox(label="Company Name", placeholder="e.g., 'ConnectSphere'")
            company_desc = gr.TextArea(label="Company Description", lines=3, placeholder="e.g., 'An AI platform that simplifies professional networking.'")
            problem = gr.TextArea(label="Problem You're Solving", lines=3, placeholder="e.g., 'Busy professionals miss out on valuable connections because finding relevant events is time-consuming.'")
            solution = gr.TextArea(label="Your Solution", lines=3, placeholder="e.g., 'Our app analyzes user profiles and calendars to recommend personalized networking opportunities.'")
            target_audience = gr.Textbox(label="Target Audience", placeholder="e.g., 'Early-career professionals, students, and freelancers.'")
            business_model = gr.Textbox(label="Business Model", placeholder="e.g., 'Freemium subscription with premium features for power users.'")

            pitch_for = gr.Dropdown(
                label="Who is this pitch for?",
                choices=[
                    "Venture Capitalists",
                    "Potential Customers",
                    "A Networking Event"
                ],
                value="Venture Capitalists"
            )

            generate_btn = gr.Button("Generate Pitch & Deck", variant="primary", scale=1)

        with gr.Column(scale=2):
            gr.Markdown("## ✨ Your Generated Assets")
            output_pitch = gr.Markdown(label="Elevator Pitch")
            output_deck = gr.Markdown(label="Pitch Deck Outline")

    generate_btn.click(
        fn=generate_pitch,
        inputs=[company_name, company_desc, problem, solution, target_audience, business_model, pitch_for],
        outputs=[output_pitch, output_deck],
        api_name="generate_pitch"
    )

if __name__ == "__main__":
    print("Attempting to launch Gradio app...")
    app.launch()

