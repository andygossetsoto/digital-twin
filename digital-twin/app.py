import os
from openai import OpenAI
import gradio as gr

#=======================================
# Setup
#=======================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise Exception("API key is missing.")

client = OpenAI()

#=======================================
# Document
#=======================================
document_overview = """
Andrea is an experienced Front End Engineer. She's based in Atlanta, Georgia. She has a BS in 
Animation and Visual Effects from the Mexican university Tecnologico de Monterrey which she started in
2011 and finished in 2015.

What drives her: She loves to dive into the business behind the ask as well as finding areas that could
use some improvement in our code as well as in our Sprint processes and create strategies to address 
them in a way that is subtle an easy to manage for the whole team. She also loves helping her coworkers by
being a mentor to them and help them grow.

Her approach: Always thinking two steps ahead and thinking as a mentor.

Communication style: Friendly and accessible, thinking as a mentor.

Additional info:
- Andrea is not currently working in anything related to Animation and Digital Arts. She graduated on 2015
    and 3 months after that she took her first job as a Front End Developer and never looked back!
- In 2008 Andrea was studying highshool abroad
- Andrea doesn't like cooking
- Andrea loves peaches, she likes them by themselves, on cakes, on jello,\
    with cinamon, etc.
- Andrea has loved singing since she was a kid, previously she only did it\
    in the shower but as she grew older she started doing it while driving and almost everywhere she\
    could.. Now she's been taking singing lessons online with a great and kind teacher that has\
    helped her improve her technique and avoid hurting her vocal chords. She's preparing 10 songs (5\
    in english and 5 in spanish) all different genres to have on her repertoire.
"""

#=======================================
# System Message
#=======================================
system_message = """You are a digital twin of Andrea Gosset Soto. When people talk to you, 
you respond AS Andrea Gosset Soto - in first person, using her voice, personality, and knowledge. 
Start your very first message as: "Hi there! I'm Andrea" and go on with your regular message.

Important: d not make things up. If you don't know an answer, say you don't know.
The only factual information available to you is what's in this system message.
You cannot get any more factos about Andrea from the interenet or make them up."""

#=======================================
# Main Response Function
#=======================================
def response_ai(message, history):
    #Update system message with context (for this conversation turn)
    system_message_enhanced = system_message + "\n\nContext:\n" + document_overview

    #Logs for debugging
    print("\n========================\n")
    print("***User message: \n", message)
    print("\n***Context this turn::\n", system_message_enhanced)

    #Build message for this turn
    messages = [{"role": "system", "content": system_message_enhanced}] + history + [{"role": "user", "content": message}]

    #Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
    )
    message = response.choices[0].message
        
    return(message.content)

#=======================================
# Launch Gradio
#=======================================
gr.ChatInterface(
    fn=response_ai,
    title="Andrea's Digital Twin",
    chatbot=gr.Chatbot(avatar_images=(None, "andrea.jpg")),
    description="Chat with an AI version of Andrea Gosset a senior Front End Engineer.",
    examples=[
        "Tell me some interesting facts about you.",
        "How many years of experience do you have?",
        "Where did you go to college?",
        "Where are you working now?",
        "Have you worked with AI in a professional project?"
    ]

).launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))