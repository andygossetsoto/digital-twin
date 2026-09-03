import os
from openai import OpenAI
import gradio as gr
from pprint import pprint
import uuid
import chromadb
import json
import requests
import random
import re

#=======================================
# Setup
#=======================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise Exception("API key is missing.")

client = OpenAI()

#=======================================
# Documents
#=======================================
document_overview = """
Andrea is an experienced Front End Engineer based in Atlanta, Georgia. She studied Animation and Digital 
Arts at Tecnológico de Monterrey in Mexico from 2011 to 2015. She is currently going through an AI 
Engineering course where she's learned about LLM Basics, Context, LLM Tool Calling, RAG, Deployment to 
Hugging Face and Render, and Agentic AI.

What drives Andrea professionally:
Andrea enjoys understanding the business context behind a request rather than focusing only on its 
technical implementation. She likes identifying opportunities to improve both the codebase and the team's 
Sprint and development processes. When she identifies an area for improvement, she works to create practical 
strategies that can be introduced gradually and managed easily by the entire team.

Mentorship is also an important part of Andrea's professional approach. She enjoys helping her coworkers 
develop their skills, grow professionally, and become more confident contributors to their teams.

Her approach:
Andrea tries to think two steps ahead, considering not only how to solve the immediate problem but also 
how a decision may affect the team, product, and codebase in the future. She approaches collaboration with 
a mentor's mindset and looks for opportunities to help others succeed.

Communication style:
Andrea's communication style is friendly, approachable, and supportive. She tries to communicate as a 
mentor: clearly explaining her reasoning, sharing knowledge, and making herself accessible to coworkers 
who need help.

Additional information about Andrea:
- Although Andrea studied Animation and Digital Arts, she does not currently work in that field. She 
graduated in 2015 and, three months later, started her first job as a Front End Developer. She discovered 
that she loved software development and has continued working in the field ever since.
- In 2008, Andrea spent time studying high school abroad.
- Andrea loves peaches. She enjoys eating them on their own as well as in cakes, Jell-O, with cinnamon, 
and in many other ways.
- Andrea has loved singing since she was a child. She initially mostly sang in the shower, but as she got 
older, she began singing while driving and almost anywhere she had the opportunity. She now takes online 
singing lessons with a kind and supportive teacher who has helped her improve her technique and learn how 
to sing without damaging her vocal cords. Andrea is currently preparing a repertoire of 10 songs: five in 
English and five in Spanish, spanning different musical genres.
"""

document_education = """
Important context:
Andrea does not currently work in Animation and Digital Arts. She graduated in 2015 and, three months 
later, began her first job as a Front End Developer. She discovered that she loved software development 
and has continued building her career in technology ever since.

University:
Tecnológico de Monterrey

Degree:
Bachelor's degree in Animation and Digital Arts

Dates:
2011-2015

Grade:
9.1 out of 10

About the program:
The Animation and Digital Arts program, also known as LAD, is a comprehensive degree that combines 
technology, narrative storytelling, and visual arts. The program has been ranked as the #1 animation 
program in Mexico and #13 internationally by Animation Career Review. Its collaborative curriculum 
prepares students to create content for the entertainment, advertising, and interactive media industries.

Core areas of the curriculum:

Art and Design:
Students develop skills in aesthetics, character design, anatomy, digital drawing, sculpture, and other 
areas of visual design.

Technology and Innovation:
Students work with industry-standard software, real-time engines, and emerging technologies such as 
artificial intelligence (AI), Virtual Reality (VR), and Augmented Reality (AR).

Audiovisual Production and Narrative:
Students learn to create and communicate stories through disciplines such as storyboarding, 
cinematography, directing, and sound design.

Areas of specialization:
Rather than focusing exclusively on a single discipline, Tecnológico de Monterrey offers multiple 
concentrations that allow students to customize their academic paths. Areas of specialization include:

- Animation: 2D animation, 3D character animation, and stop-motion animation.
- Gaming and Interactivity: video game design, immersive environments, and User Experience/User 
Interface (UX/UI) design.
- Post-Production: sound design, Visual Effects (VFX), digital modeling, and lighting.
- Film and Business: film production and direction, creative writing, and entrepreneurship within 
the creative industries.

Career opportunities:
The program prepares graduates to work not only as technical specialists but also in creative and 
technical leadership positions. Graduates can pursue opportunities in animation and VFX studios, 
video game development, film production, commercial advertising, UI/UX design, and architectural 
visualization.

Alumni of the program have worked at organizations such as Sony Pictures Imageworks, Moving Picture 
Company (MPC), Netflix, and Cinesite. Graduates have also contributed to major film productions 
including Spider-Man: Across the Spider-Verse, Guardians of the Galaxy Vol. 3, Dune, and Avatar.

While still in college Andrea interned as a 3D modeller for MetaCube, a company that created the 
movie "Día de Muertos". She created a lot of environment models that included a lot of skulls in 
them.
"""

document_professional_experience = """
Professional Summary:

Andrea has worked as a Front End Engineer since 2016, developing web applications and working with 
Content Management Systems (CMS) across multiple industries. Her experience includes both 
individual contributor and technical leadership responsibilities.

In addition to front-end development, Andrea places significant importance on understanding the 
business needs behind technical requirements. She has experience mentoring engineers, leading 
development initiatives, collaborating with cross-functional teams, improving Agile and Scrum 
processes, and identifying opportunities to improve both user experience and engineering 
efficiency.


Professional Experience:

2015: 3D Digital Modeler Intern at MetaCube

Andrea began her professional career as a 3D Digital Modeler intern at MetaCube, where she 
worked on the animated film Día de Muertos. Although this position was related to her Animation 
and Digital Arts degree, she transitioned into front-end software development shortly afterward.


2016-2018: Front End Engineer at Base22

Andrea worked as a Front End Engineer at Base22, beginning her professional career in software 
development and web application development.


2018-2022: Senior Front End Engineer at Globant

- Led a consulting development team working with Realogy to build two internal platforms using 
Angular 7, NgRx, Jasmine, and Apollo GraphQL. These intranets provided real estate professionals 
with a centralized platform for accessing essential tools used in their day-to-day work.

- Engineered an npm library using Node.js to provide a standardized theme across multiple 
intranets and applications. This improved development efficiency and visual consistency across products.

- Collaborated with Stanley Black & Decker's team to improve its Site Manager and Public API 
internal applications. Andrea also developed a week-by-week action plan designed to streamline 
the team's development and Scrum processes.

- Mentored three colleagues at a time, providing ongoing guidance and support to help them 
develop professionally and advance within their teams.

- Interviewed prospective engineering candidates and evaluated their potential fit within the 
company and its development teams.


2022-2023: Software Engineer at Twitter

- Led the front-end effort for the Semantic Core UI migration using React.js, TypeScript, 
JavaScript, and CSS. The migration supported Twitter's internal advertising platform, which 
enabled clients to gather insights and make more informed decisions about ad promotion.

- Mentored and led a five-person group within the TwST (Twitter Security Team) organization, 
supporting professional development, team collaboration, and cross-functional work toward 
departmental objectives.

- Authored the Technical Design Document for the Semantic Core UI migration. The document 
defined the technical approach for new implementations while establishing a more organized 
architecture designed to improve code quality and long-term maintainability.


2023-Present: Senior Front End Engineer at Rooms To Go

Andrea works as a Senior Front End Engineer at Rooms To Go, where she has contributed to 
improving e-commerce website performance, streamlining content management and updates, 
implementing new customer-facing functionality, and collaborating with cross-functional 
teams. She has also taken on front-end leadership responsibilities and worked to improve 
Agile processes, engineering efficiency, and delivery.

Key contributions include:

- Spearheaded front-end Artificial Intelligence (AI) initiatives designed to improve 
customer engagement, contributing to a 30 percent increase in sales revenue.

- Helped migrate the primary Rooms To Go e-commerce website from React.js and Material UI 
(MUI) to Next.js, TypeScript, and Tailwind CSS. The new architecture introduced a more 
efficient server-side solution and resulted in a 45% performance improvement, improving 
the customer experience.

- Developed, updated, and redesigned React.js components, Strapi schemas, and the 
organization's internal npm library to simplify e-commerce content management. These 
improvements supported timely website updates, including weekly sales and promotional content.

- Collaborated closely with Content, UX, and Marketing teams to understand business 
requirements and translate them into actionable engineering tickets. Andrea also assumed 
leadership responsibilities for coordinating and supporting their implementation within the 
front-end team.


Technical Skills:

Programming and Web Technologies:
JavaScript (ES6+), TypeScript, HTML, CSS, Node.js, Scala

Front-End Frameworks and Libraries:
React.js, Next.js, Angular 7, Vue, jQuery, Redux, NgRx, Material UI (MUI), Tailwind CSS, 
SASS, Mustache, Handlebars

Testing:
Jest, Jasmine, Cypress

APIs and Data:
Apollo GraphQL, GraphQL, REST APIs

Content Management Systems:
Strapi, IBM Web Content Manager (WCM), Liferay DXP

Build and Development Tools:
Webpack, Gulp, Grunt, Git

AI and Automation:
n8n, Claude, Cursor, Gemini

Development Methodologies:
Agile, Scrum, Kanban


Languages:

Spanish: Native
English: Fluent
French: Proficient
"""

#=======================================
# Chunking Function
#=======================================
def split_text_into_chunks(
    text: str,
    max_chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        max_end = min(start + max_chunk_size, len(text))
        if max_end == len(text):
            chunks.append(text[start:].strip())
            break
        halfway = start + max_chunk_size // 2
        section = text[halfway:max_end]
        boundaries = [
            section.rfind("\n\n"),
            section.rfind("\n"),
        ]
        sentence_matches = list(re.finditer(r"[.!?](?=\s|$)", section))
        boundaries.append(
            sentence_matches[-1].end() if sentence_matches else -1
        )
        boundaries.append(section.rfind(" "))
        cut = next((b for b in boundaries if b != -1), None)
        end = halfway + cut if cut is not None else max_end
        if cut is not None:
            if text[end:end + 2] == "\n\n":
                end += 2
            elif text[end:end + 1] == "\n":
                end += 1
            elif end < len(text) and text[end] in ".!?":
                end += 1
        chunks.append(text[start:end].strip())
        start = end - overlap
    return chunks

#=======================================
# RAG: Chunk, Embed & Store in Chroma DB
#=======================================
documents = [
    {"text": document_overview, "source": "Overview"},
    {"text": document_education, "source": "Education"},
    {"text": document_professional_experience, "source": "Professional Experience"}
]

chunks = []
ids = []
metadatas = []

for doc in documents:
    #Prepare the lists
    chunks_ = split_text_into_chunks(doc["text"], max_chunk_size=300, overlap=30)
    ids_ = [str(uuid.uuid4()) for _ in range(len(chunks_))]
    metadatas_ = [{"source": doc["source"], "chunk_index": i} for i in range(len(chunks_))]
    #Add to main lists
    chunks.extend(chunks_)
    ids.extend(ids_)
    metadatas.extend(metadatas_)

#Print for logs
print(f"Created {len(chunks)} chunks: \n")

for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i + 1} (ID: {ids[i]}, Source: {metadatas[i]['source']}, Index: {metadatas[i]['chunk_index']}, Length: {len(chunk)}):")
    print(chunk)
    print()

#Generate embeddings for all chunks
response = client.embeddings.create(
    model ="text-embedding-3-small",
    input = chunks
)
embeddings = [item.embedding for item in response.data]

#Verify embeddings for logs
print(f"Generated {len(embeddings)} embeddings")
print(f"Each embedding has {len(embeddings[0])} dimensions")

#initialize ChromaDB client (persistent storage)
chroma_client = chromadb.PersistentClient(path="./chroma_db_twin")

#Alternative: initialize ChromaDB client (in-memory   storage)
#chroma_client = chromadb.Client()

#Empty the collection before adding new data (for testint purposes in regular projects you don't need this functionality)
collection = chroma_client.get_or_create_collection(name="digital_twin")
if collection.get()["ids"]:
    collection.delete(collection.get()["ids"])

#Get or Create + Empty the collection before adding new data (for testint purposes in regular projects you don't need this functionality)
if collection.get()["ids"]:
    collection.delete(collection.get()["ids"])

#Adding data to ChromaDB
collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=chunks,
    metadatas=metadatas
)
pprint(collection.get())

#=======================================
# Tools
#=======================================
tools = []

PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

#Create send_notification function
def send_notification(message: str):
    if PUSHOVER_USER is None or PUSHOVER_TOKEN is None: #Handling of potential missing credentials
        return "Notification failed: Pushover not configured."
    payload = {"user": PUSHOVER_USER, "token": PUSHOVER_TOKEN, "message": message}
    requests.post(pushover_url, data=payload)
    return f"Nofification sent: {message}"

#Describe Pushover as an LLM tool
send_notification_function = {
    "name": "send_notification",
    "description": "Send a push notification to the real Andrea. Use this when: \
        1) Someone wants to get in touch, hire, or collaborate\
        - ask for their name and contact details first, then send notification to \
        Andrea with the name and contact details. \
        2) You don't know the answer to a question about Andrea - send AUTOMATICALLY \
        without asking, include the question so she can add this info later.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The notification message to send to the user's device."
            }
        },
        "required": ["message"]
    }
}

#Add Pushover to the list of tools for the LLM
tools.append({"type": "function", "function": send_notification_function})

#Simulates rolling a single six-sided die
def dice_roll():
    result = random.randint(1,6)
    return result

#Describe function for the LLM
roll_dice_function = {
    "name": "dice_roll",
    "description": "Simulates rolling a single six-sided die and returns the result. Use this when the user wants to roll a die for games, decisions, or random number generation.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
    }
}

#Add function to lit of tools of LLM
tools.append({"type": "function", "function": roll_dice_function})

#=======================================
# Tool Handler
#=======================================
def handle_tool_call(tool_calls):
    tool_results = []

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        #print(f"Calling function {function_name}") #For future debugging!

        #Route to the appropriate function based on function_name
        if function_name == "send_notification":
            content = send_notification(args["message"])
        elif function_name == "dice_roll":
            content = f"Rolled: {dice_roll()}"
        #elif function_name == "insert_function_name_3":
            # content = insert_function_name3(args["message"])
        #....
        else:
            content = f"Unknown function: {function_name}"

        tool_call_result = {
            "role": "tool",
            "content": content,
            "tool_call_id": tool_call.id,
        }
        tool_results.append(tool_call_result)
    
    return tool_results

#=======================================
# System Message
#=======================================
system_message = """You are a digital twin of Andrea Gosset Soto. When people talk to you, 
you respond AS Andrea Gosset Soto - in first person, using her voice, personality, and knowledge. 
Start your very first message as: "Hi there! I'm Andrea" and go on with your regular message.

Important: d not make things up. If you don't know an answer, say you don't know.
The only factual information available to you is what's in this system message.
You cannot get any more factos about Andrea from the interenet or make them up.

IMPORTANT: Whenever you don't know something about Andrea,
ALWAYS use the send_notification tool to aler the real Andrea - do this automatically without 
asking the user."""

#=======================================
# Main Response Function
#=======================================
def response_ai(message, history):
    #RAG:Embed the query using the same model we used for the chunks to ensure compatibility
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[message]
    )

    query_embedding = response.data[0].embedding

    #RAG: Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    #RAG: Stich retrieve chunks together to create the context for the response
    context = "\n---\n".join(results["documents"][0])

    #Print logs for debugging
    print("\n========================\n")
    print(f"User message: \n{message}\n")
    print("***Retrieved Chunks:")
    for a, b in zip(results["documents"][0], results["metadatas"][0]):
        print("---------------------")
        print(f"<<Document {b['source']} -- Chunk {b['chunk_index']}:\n{a}\n")

    #Update system message with context (for this conversation turn)
    system_message_enhanced = system_message + "\n\nContext:\n" + context

    #Build message for this turn
    messages = [{"role": "system", "content": system_message_enhanced}] + history + [{"role": "user", "content": message}]

    #Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=tools
    )
    message = response.choices[0].message

    while message.tool_calls:
            from pprint import pprint
            pprint(message.tool_calls)
            tools_result = handle_tool_call(message.tool_calls)
            messages.append(message)
            messages.extend(tools_result)
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                tools=tools
            )
            message = response.choices[0].message
            #Note: maybe consider adding protection from infinite consecutive tool calling
        
    return(message.content)

#=======================================
# Launch Gradio
#=======================================
gr.ChatInterface(
    fn=response_ai,
    title="Andrea's Digital Twin",
    chatbot=gr.Chatbot(avatar_images=(None, "andrea.jpg")),
    description="Chat with an AI version of Andrea Gosset. Ask about her experience, project, or just say hi!",
    examples=["What is your background?", "AI Engineering experience", "Front End experience", "Where did you go to college?"]

).launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))