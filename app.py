import os
from dotenv import load_dotenv
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
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise Exception("API key is missing.")

client = OpenAI()

#=======================================
# Documents
#=======================================
document_overview = """
PROFESSIONAL OVERVIEW
Andrea is an experienced Front End Engineer based in Atlanta, Georgia. Her professional background is 
primarily in front-end software development and web development. She currently works as a Senior Front 
End Developer at Rooms To Go, where she has worked for approximately three and a half years.
Andrea is currently completing an AI Engineering course to expand her software engineering knowledge 
into artificial intelligence. Her coursework includes Large Language Model fundamentals, LLM context, 
tool and function calling, Retrieval-Augmented Generation (RAG), Agentic AI, and application deployment.
As part of her AI Engineering studies, Andrea has learned how to deploy AI applications using platforms 
such as Hugging Face and Render. She is also learning how LLM-powered applications can retrieve external 
information, call tools, use context, and perform multi-step tasks through agentic workflows.

EDUCATION AND CAREER
Andrea studied Animation and Digital Arts at Tecnológico de Monterrey in Mexico from 2011 to 2015. Her 
university education focused on animation and digital arts, but she ultimately chose a different 
professional path and does not currently work in the animation industry.
While attending college in 2015, Andrea worked as a 3D modeling intern at MetaCube. MetaCube is a company that 
created the movie "Día de Muertos".
Andrea graduated from Tecnológico de Monterrey in 2015 and started her first job as a Front End Developer 
approximately three months later. Through that role, she discovered that she loved software development 
and decided to continue building her professional career in front-end engineering and technology.
Andrea's career therefore transitioned from an academic background in Animation and Digital Arts into 
software engineering. Although her university degree is not in computer science, she has built her 
professional experience through years of working directly in front-end development and software 
engineering roles.
In 2008, Andrea spent approximately one year studying abroad at Masillon - Ecole Bilingue Internationale. 
This experience took place before her university studies at Tecnológico de Monterrey and is part of her 
international educational background.

PROFESSIONAL MOTIVATIONS
Andrea enjoys understanding the business context behind a request rather than focusing exclusively on 
technical implementation. Before developing a solution, she likes to understand why the request exists, 
what problem it is intended to solve, and how the final implementation will affect the business, product, 
and users.
Andrea is interested in improving more than individual features or pieces of code. She looks for 
opportunities to improve the codebase, development workflows, Sprint processes, team collaboration, 
efficiency, and maintainability. She considers both software quality and the processes used by the team 
to build that software.
When Andrea identifies an opportunity for improvement, she prefers practical and sustainable solutions. 
Rather than introducing large disruptive changes at once, she likes creating strategies that can be 
implemented gradually and that are easy for the entire team to understand, adopt, maintain, and manage 
over time.

PROBLEM-SOLVING APPROACH
Andrea describes her problem-solving approach as trying to think two steps ahead. She considers not 
only how to solve the immediate problem but also how a technical decision may affect the team, product, 
development process, user experience, and codebase in the future.
When evaluating technical solutions, Andrea thinks about long-term maintainability, scalability, future 
development, and the impact on other developers. She prefers solutions that solve the current problem 
effectively without unnecessarily creating additional complexity or future maintenance problems.
Andrea's decision-making combines technical and business considerations. She wants an implementation 
to make sense from an engineering perspective while also supporting the original business objective. 
Understanding the reason behind a request helps her determine whether the proposed technical solution 
is actually the best approach.

MENTORSHIP AND TEAM DEVELOPMENT
Mentorship has been an important part of Andrea's previous professional experience. In a past role, 
she had opportunities to mentor coworkers and enjoyed helping them strengthen their technical skills, 
understand unfamiliar concepts, grow professionally, and become more confident contributors to their team.
Through her previous mentorship experience, Andrea developed a collaborative approach centered on 
knowledge sharing and helping other developers grow. She enjoyed explaining technical decisions, working 
through problems with coworkers, and helping them build the skills and confidence needed to work more 
independently.
Andrea is not currently serving in a formal mentorship role at Rooms To Go. However, the skills and mindset 
she developed through previous mentorship experience continue to influence how she collaborates, shares 
knowledge, explains technical concepts, and supports coworkers when opportunities arise.

COMMUNICATION STYLE
Andrea's communication style is friendly, approachable, supportive, and collaborative. When discussing 
technical topics, she prefers to explain both what decision was made and why it was made. Providing 
context is important to her because she wants coworkers to understand the reasoning behind a solution 
rather than simply follow instructions.
Andrea's previous mentorship experience influences the way she communicates with coworkers today. She 
values clearly explaining her reasoning, sharing knowledge, answering questions, and helping others 
understand unfamiliar concepts. She tries to remain approachable and create an environment where 
coworkers feel comfortable asking questions.

PERSONAL INTERESTS
Andrea loves peaches and considers them one of her favorite foods. She enjoys eating fresh peaches on 
their own as well as trying them in many different forms, including cakes, Jell-O, peaches with cinnamon, 
and other peach-based foods and desserts.
Andrea has loved singing since she was a child. When she was younger, she mostly sang in the shower, but 
as she got older she began singing while driving and almost anywhere she had the opportunity. Singing has 
remained one of Andrea's long-term hobbies and personal interests.
Andrea currently takes online singing lessons with a kind and supportive teacher. Her lessons have helped 
her improve her vocal technique and learn healthier ways to sing without damaging her vocal cords. She 
continues practicing regularly and is focused on improving both her technique and confidence.
Andrea is currently preparing a repertoire of 10 songs as part of her singing practice. The repertoire 
contains five songs in English and five songs in Spanish and includes music from several different genres. 
Her current singing goal is to learn, practice, and prepare this bilingual collection of songs.
"""

document_education = """
EDUCATION OVERVIEW
Andrea studied Animation and Digital Arts at Tecnológico de Monterrey from 2011 to 2015. She earned a 
Bachelor's degree in Animation and Digital Arts and graduated with a grade of 9.1 out of 10.

Andrea does not currently work in Animation and Digital Arts. About three months after graduating in 2015, 
she began her first job as a Front End Developer. Through that role, she discovered that she loved software 
development and has continued building her professional career in technology ever since.

UNIVERSITY AND DEGREE
University: Tecnológico de Monterrey
Degree: Bachelor's degree in Animation and Digital Arts
Program name: Animation and Digital Arts, also known as LAD
Dates attended: 2011-2015
Final grade: 9.1 out of 10

ABOUT THE ANIMATION AND DIGITAL ARTS PROGRAM
The Animation and Digital Arts program at Tecnológico de Monterrey, also known as LAD, is a comprehensive 
degree that combines technology, narrative storytelling, and visual arts. Its curriculum is collaborative 
and prepares students to create content for entertainment, advertising, and interactive media industries.
The Animation and Digital Arts program has been ranked as the #1 animation program in Mexico and #13 
internationally by Animation Career Review. The program combines artistic, technical, and narrative 
disciplines rather than focusing exclusively on a single area of animation or digital production.

ART AND DESIGN CURRICULUM
The Art and Design portion of the Animation and Digital Arts curriculum develops students' visual and 
artistic skills. Areas of study include aesthetics, character design, anatomy, digital drawing, sculpture, 
and other disciplines related to visual design and artistic development.


TECHNOLOGY AND INNOVATION CURRICULUM
The Technology and Innovation portion of the program exposes students to industry-standard software, 
real-time engines, and emerging technologies. Areas of study include technologies such as artificial 
intelligence (AI), Virtual Reality (VR), and Augmented Reality (AR).

AUDIOVISUAL PRODUCTION AND NARRATIVE
The Audiovisual Production and Narrative portion of the Animation and Digital Arts program teaches 
students how to create and communicate stories. Areas of study include storyboarding, cinematography, 
directing, sound design, and other disciplines involved in visual and audiovisual storytelling.

AREAS OF SPECIALIZATION
Tecnológico de Monterrey's Animation and Digital Arts program allows students to customize their 
academic path through multiple areas of specialization. Rather than requiring students to focus 
exclusively on one discipline, the program offers concentrations across animation, interactivity, 
post-production, film, and business.
Animation specializations include 2D animation, 3D character animation, and stop-motion animation. 
These areas focus on different techniques for creating animated characters, movement, and visual 
storytelling across traditional and digital production methods.
Gaming and Interactivity specializations include video game design, immersive environments, and User 
Experience/User Interface design, commonly known as UX/UI. These areas combine interactive technology, 
digital experiences, and user-centered design.
Post-Production specializations include sound design, Visual Effects (VFX), digital modeling, and 
lighting. These disciplines focus on the technical and artistic processes used to create, enhance, and 
finalize digital and audiovisual productions.
Film and Business specializations include film production and direction, creative writing, and 
entrepreneurship within the creative industries. These areas combine storytelling, production, leadership, 
and business knowledge related to entertainment and creative work.

CAREER OPPORTUNITIES
The Animation and Digital Arts program prepares graduates for both technical specialist roles and creative 
or technical leadership positions. Career opportunities can include work in animation and VFX studios, 
video game development, film production, commercial advertising, UI/UX design, and architectural visualization.
Graduates of the Animation and Digital Arts program have worked at organizations including Sony Pictures 
Imageworks, Moving Picture Company (MPC), Netflix, and Cinesite. Alumni have pursued careers across 
animation, visual effects, film production, and other areas of the entertainment industry.
Graduates of the program have contributed to major film productions including Spider-Man: Across the 
Spider-Verse, Guardians of the Galaxy Vol. 3, Dune, and Avatar. These examples reflect the program's 
connection to professional animation, film, and visual effects industries.

ANDREA'S COLLEGE INTERNSHIP
While attending college, Andrea worked as a 3D modeling intern at MetaCube. MetaCube is a company that 
created the movie "Día de Muertos". This internship gave Andrea professional experience in 3D modeling 
while she was still completing her Animation and Digital Arts degree.
During her internship at MetaCube, Andrea primarily created 3D environment models. Many of the environments 
she worked on included skulls, so skull modeling became a recurring part of the environment assets she 
produced during the internship.
"""

document_professional_experience = """
PROFESSIONAL SUMMARY
Andrea has worked professionally as a Front End Engineer since 2016. Her experience includes developing 
web applications, working with Content Management Systems (CMS), and contributing to software projects 
across multiple industries. Her career has included both individual contributor responsibilities and 
technical leadership responsibilities.
Andrea places significant importance on understanding the business needs behind technical requirements 
rather than focusing only on implementation. Her professional experience includes collaborating with 
cross-functional teams, leading development initiatives, improving Agile and Scrum processes, and 
identifying opportunities to improve user experience and engineering efficiency.
Andrea also has previous professional mentorship experience. In past roles at Globant and Twitter, 
she mentored engineers and supported their professional development. Mentorship is part of her previous 
leadership experience, but she is not currently serving in a formal mentorship role at Rooms To Go.

PROFESSIONAL EXPERIENCE

METACUBE — 3D DIGITAL MODELER INTERN — 2015
Andrea began her professional career in 2015 as a 3D Digital Modeler intern at MetaCube. During this 
internship, she worked on the animated film "Día de Muertos." The role was directly related to her 
university studies in Animation and Digital Arts and provided her with professional experience in 3D 
digital modeling.

Although Andrea's first professional experience was in 3D modeling, she transitioned into front-end 
software development shortly afterward. Her MetaCube internship represents the beginning of her 
professional career before she moved from the Animation and Digital Arts field into software engineering.


BASE22 — FRONT END ENGINEER — 2016-2018
Andrea worked as a Front End Engineer at Base22 from 2016 to 2018. This position marked the beginning 
of her professional career in software development and web application development after transitioning 
away from the Animation and Digital Arts field.


GLOBANT — SENIOR FRONT END ENGINEER — 2018-2022
Andrea worked as a Senior Front End Engineer at Globant from 2018 to 2022. During this role, she worked 
as a consultant with multiple clients, including Realogy and Stanley Black & Decker. Her responsibilities 
included front-end development, technical leadership, process improvement, candidate interviews, and 
employee mentorship.

At Globant, Andrea led a consulting development team working with Realogy to build two internal 
platforms. The applications were developed using Angular 7, NgRx, Jasmine, and Apollo GraphQL and 
functioned as intranets for real estate professionals.

The two Realogy intranets provided real estate professionals with centralized access to essential tools 
used in their day-to-day work. Andrea's responsibilities on the project included development leadership 
as well as contributing to the implementation of the internal web applications.

Andrea engineered an npm library using Node.js to provide a standardized theme across multiple intranets 
and applications. The shared library helped improve development efficiency by allowing teams to reuse 
common functionality and styling while also increasing visual consistency across products.

Andrea also collaborated with Stanley Black & Decker's development team to improve its Site Manager and 
Public API internal applications. Her work included contributing to the applications themselves as well 
as evaluating opportunities to improve the team's development processes.

For the Stanley Black & Decker team, Andrea developed a week-by-week action plan intended to streamline 
the development workflow and improve Scrum processes. The plan focused on creating a more organized and 
efficient approach to the team's software development and delivery practices.

Mentorship was part of Andrea's responsibilities at Globant. She mentored three colleagues at a time, 
providing ongoing guidance and support intended to help them develop professionally, strengthen their 
skills, and advance within their respective teams.

Andrea also participated in Globant's engineering hiring process. She interviewed prospective engineering 
candidates and evaluated their technical and professional potential to determine how well they could fit 
within the company and its development teams.


TWITTER — SOFTWARE ENGINEER — 2022-2023
Andrea worked as a Software Engineer at Twitter from 2022 to 2023. Her responsibilities included front-end 
engineering, technical design, technical leadership, mentorship, and cross-functional collaboration within 
projects related to Twitter's internal systems.

Andrea led the front-end effort for the Semantic Core UI migration at Twitter. The implementation used 
React.js, TypeScript, JavaScript, and CSS and supported an internal advertising platform used by clients 
to gather insights and make more informed decisions about advertising promotion.

Andrea authored the Technical Design Document for the Semantic Core UI migration. The document defined the 
technical approach for new implementations while also establishing a more organized application 
architecture designed to improve code quality and long-term maintainability.

Andrea also mentored and led a five-person group within the TwST, or Twitter Security Team, organization. 
In this previous mentorship role, she supported professional development, encouraged team collaboration, 
and helped coordinate cross-functional work toward broader departmental objectives.


ROOMS TO GO — SENIOR FRONT END ENGINEER — 2023-PRESENT
Andrea has worked as a Senior Front End Engineer at Rooms To Go since 2023. Her work includes improving 
the company's e-commerce website, streamlining content management and website updates, implementing 
customer-facing functionality, and collaborating with cross-functional teams.

At Rooms To Go, Andrea has also taken on front-end leadership responsibilities and contributed to 
improvements in Agile processes, engineering efficiency, and software delivery. Her current leadership 
responsibilities focus on front-end work, technical coordination, business requirements, and development 
processes rather than formal employee mentorship.

Andrea helped migrate the primary Rooms To Go e-commerce website from an architecture using React.js and 
Material UI (MUI) to one using Next.js, TypeScript, and Tailwind CSS. The new architecture introduced a 
more efficient server-side solution.

The Rooms To Go website migration resulted in a 45% performance improvement. By improving the application's 
architecture and server-side behavior, the migration increased website performance and contributed to a 
better customer experience on the company's primary e-commerce platform.

Andrea develops, updates, and redesigns React.js components, Strapi schemas, and the organization's internal 
npm library. This work is intended to simplify the management of e-commerce content and make recurring 
website changes easier for the teams responsible for maintaining the site.

The content-management improvements Andrea has contributed to at Rooms To Go support timely website updates, 
including frequent sales and promotional changes. Weekly promotions require the e-commerce site to be updated 
efficiently, making maintainable components, schemas, and shared tooling important to the content workflow.

Andrea works closely with the Content, UX, and Marketing teams at Rooms To Go to understand business 
requirements. She translates those requirements into actionable engineering tickets so that requested 
features and website changes can be understood and implemented by the front-end engineering team.

Andrea has also assumed front-end leadership responsibilities for coordinating and supporting the 
implementation of requirements from Content, UX, and Marketing. This involves connecting business needs with 
front-end development work and helping organize how those requirements are delivered by the engineering team.


AI PROJECTS AT ROOMS TO GO

AI-POWERED CUSTOMER REVIEW SUMMARIZATION
Andrea spearheaded the front-end implementation of an AI-powered customer review summarization feature at Rooms 
To Go. The project was designed to transform large volumes of individual e-commerce customer reviews into 
concise summaries that make customer feedback easier to understand and use.
The customer review summarization workflow uses n8n to automate the processing and categorization of customer 
reviews. Reviews are organized into relevant categories before the categorized data is provided to a Large 
Language Model (LLM) for analysis and summary generation.

The Large Language Model generates two types of customer review summaries. One is an overall summary that 
represents general customer sentiment and important themes across all reviews. The second consists of 
category-specific summaries that highlight customer feedback associated with individual review categories.

The AI review summarization project combines front-end engineering, n8n workflow automation, LLM integration, 
review categorization, and database updates. Together, these components transform individual customer reviews 
into structured data and concise AI-generated summaries that can be presented to users.


AI-POWERED FRONT-END DOCUMENTATION AUTOMATION
Andrea implemented an AI-powered front-end documentation workflow at Rooms To Go. The system uses GitHub agents 
and AI to detect application changes, investigate the relevant code and project sources, generate technical 
documentation, and automatically publish approved documentation updates to Confluence.

The documentation workflow begins when a specific schema file is modified. A modification to this schema 
indicates that the portion of the front-end application represented by the documentation has changed. This 
file change acts as the trigger for the first GitHub agent in the automation workflow.

When the schema modification is detected, the first GitHub agent initiates a request for the AI to investigate 
the project sources relevant to the application change. The goal of this step is to provide the AI with enough 
information to understand what changed and how the change affects the application's functionality.

The AI analyzes the relevant project sources to determine the functionality and application logic associated 
with the detected change. It then generates a comprehensive technical description intended to capture the 
important logic and behavior required for the application's documentation.

The AI-generated documentation is stored in a structured JSON file. This JSON file serves as the source of 
truth for the expected front-end documentation and contains the documentation data that should ultimately 
be reflected in the corresponding Confluence pages.

When application changes are ready to be merged into production, a second GitHub agent checks whether the 
documentation JSON file has been modified. A change to the JSON file indicates that the application's 
technical documentation also requires an update.

If the second GitHub agent detects a documentation JSON update, it automatically publishes the corresponding 
documentation changes to the appropriate Confluence pages. This connects approved application changes with 
the publication of their associated technical documentation.

The complete workflow creates an automated documentation pipeline. Application changes trigger AI-assisted 
investigation and documentation generation, while the production workflow ensures that approved documentation 
is automatically published to Confluence when the corresponding documentation data changes.

The AI documentation workflow helps keep technical documentation synchronized with the front-end application. 
It also reduces the manual effort required from developers to investigate application changes, write 
documentation, update documentation sources, and communicate approved technical changes through Confluence.


TECHNICAL SKILLS

PROGRAMMING AND WEB TECHNOLOGIES
Andrea's programming and web technology experience includes JavaScript (ES6+), TypeScript, HTML, CSS, 
Node.js, and Scala.


FRONT-END FRAMEWORKS AND LIBRARIES
Andrea's front-end framework and library experience includes React.js, Next.js, Angular 7, Vue, jQuery, 
Redux, NgRx, Material UI (MUI), Tailwind CSS, SASS, Mustache, and Handlebars.


TESTING
Andrea's software testing experience includes Jest, Jasmine, and Cypress.


APIS AND DATA
Andrea's API and data technology experience includes Apollo GraphQL, GraphQL, and REST APIs.


CONTENT MANAGEMENT SYSTEMS
Andrea has professional experience working with Content Management Systems including Strapi, IBM Web 
Content Manager (WCM), and Liferay DXP.


BUILD AND DEVELOPMENT TOOLS
Andrea's build, version control, and development tool experience includes Webpack, Gulp, Grunt, and Git.


AI AND AUTOMATION
Andrea's AI and automation tool experience includes n8n, Claude, Cursor, and Gemini.


DEVELOPMENT METHODOLOGIES
Andrea has professional experience working with Agile, Scrum, and Kanban software development methodologies.


LANGUAGES
Andrea is a native Spanish speaker.
Andrea is fluent in English.
Andrea is proficient in French.
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
print(f"Created {len(chunks)} chunks: \n", flush=True)

for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i + 1} (ID: {ids[i]}, Source: {metadatas[i]['source']}, Index: {metadatas[i]['chunk_index']}, Length: {len(chunk)}):", flush=True)
    print(chunk, flush=True)

#Generate embeddings for all chunks
embedding_response = client.embeddings.create(
    model ="text-embedding-3-small",
    input = chunks
)
embeddings = [item.embedding for item in embedding_response.data]

#Verify embeddings for logs
print(f"Generated {len(embeddings)} embeddings", flush=True)
print(f"Each embedding has {len(embeddings[0])} dimensions", flush=True)

#initialize ChromaDB client (persistent storage)
chroma_client = chromadb.PersistentClient(path="./chroma_db_twin")

#Alternative: initialize ChromaDB client (in-memory   storage)
#chroma_client = chromadb.Client()

#Empty the collection before adding new data (for testing purposes in regular projects you don't need this functionality)
collection = chroma_client.get_or_create_collection(name="digital_twin")
if collection.get()["ids"]:
    collection.delete(collection.get()["ids"])

#Get or Create + Empty the collection before adding new data (for testing purposes in regular projects you don't need this functionality)
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

Important: do not make things up. If you don't know an answer, say you don't know.
The only factual information available to you is what's in this system message.
You cannot get any more facts about Andrea from the internet or make them up.

IMPORTANT: Whenever you don't know something about Andrea,
ALWAYS use the send_notification tool to alert the real Andrea - do this automatically without 
asking the user."""

#=======================================
# Main Response Function
#=======================================
def response_ai(message, history):
    #RAG:Embed the query using the same model we used for the chunks to ensure compatibility
    query_embedding_response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[message]
    )

    query_embedding = query_embedding_response.data[0].embedding

    #RAG: Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    #RAG: Stitch retrieve chunks together to create the context for the response
    context = "\n---\n".join(results["documents"][0])

    #Print logs for debugging
    print("\n========================\n", flush=True)
    print(f"User message: \n{message}\n", flush=True)
    print("***Retrieved Chunks:", flush=True)
    for a, b in zip(results["documents"][0], results["metadatas"][0]):
        print("---------------------", flush=True)
        print(f"<<Document {b['source']} -- Chunk {b['chunk_index']}:\n{a}\n", flush=True)

    #Update system message with context (for this conversation turn)
    system_message_enhanced = system_message + "\n\nContext:\n" + context

    #Build message for this turn
    messages = [{"role": "system", "content": system_message_enhanced}] + history + [{"role": "user", "content": message}]

    #Call LLM
    llm_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=tools
    )
    message = llm_response.choices[0].message

    while message.tool_calls:
        from pprint import pprint
        pprint(message.tool_calls)
        tools_result = handle_tool_call(message.tool_calls)
        messages.append(message)
        messages.extend(tools_result)
        llm_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=tools
        )
        message = llm_response.choices[0].message
        #Note: maybe consider adding protection from infinite consecutive tool calling
        
    return(message.content)

#=======================================
# Launch Gradio
#=======================================
gr.ChatInterface(
    fn=response_ai,
    title="Andrea's Digital Twin",
    chatbot=gr.Chatbot(avatar_images=(None, "andrea.jpg")),
    description="Chat with an AI version of Andrea Gosset. Ask about her experience, projects, or just say hi!",
    examples=["What is your background?", "AI Engineering experience", "Front End experience", "Where did you go to college?"]

).launch(server_name="127.0.0.1", server_port=int(os.environ.get("PORT", 7860)))
