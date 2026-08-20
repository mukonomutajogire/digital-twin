import os
from openai import OpenAI
import gradio as gr
from pprint import pprint
import uuid
import chromadb
import json
import requests
import random

#-----------------------------------------------------
# Setup
#-----------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise Exception("API key is missing.")
client = OpenAI()

#-----------------------------------------------------
# Document
#-----------------------------------------------------
document_professional_summary = """

•	18 years of experience in software engineering, technical support engineering, Site Reliability Engineering (SRE), cloud engineering, distributed systems, telecom, and customer-facing technical operations.
•	Extensive experience providing technical guidance to customers, developers, and external partners throughout API integration, onboarding, production deployment, troubleshooting, and support.
•	Strong experience designing, developing, testing, deploying, and supporting Java-based backend services, REST APIs, cloud-native applications, distributed systems, and microservices throughout the Software Development Lifecycle (SDLC).
•	Proven ability to troubleshoot complex customer issues using observability platforms including Prometheus, Grafana dashboards, Elasticsearch, Kibana, PagerDuty, logging, metrics, alerting, and distributed tracing to quickly diagnose and resolve production incidents.
•	Extensive experience collaborating with software engineering, product management, customer success, solution architects, vendors, and customer development teams to resolve customer escalations, improve API integrations, and enhance customer experience.
•	Experience developing troubleshooting guides, technical documentation, automation scripts, KPI dashboards, and support documentation to improve operational efficiency and customer self-service.
•	Strong background in production support, incident response, root cause analysis, postmortems, customer communications, API lifecycle management, cloud-native platforms, Kubernetes operations, Linux administration, and automation in Agile environments.
•	Lean Six Sigma Green Belt with strong analytical, problem-solving, and continuous improvement skills focused on improving customer satisfaction, operational excellence, reliability, and engineering productivity.
•	Innovative software engineer passionate about customer success, API platforms, cloud-native technologies, AI infrastructure, and leveraging LLMs, RAG, MCP, AIOps, and MLOps to automate workflows and improve engineering operations.
"""

document_professional_experience = """
Site Reliability Professional, Aduna Global USA                                                                                 July 2025 to June 2026
•	Served as the primary technical interface for customers, CSPs, developers, and external partners during SIM Swap, Number Verification, Device Swap, and KYC API integrations, providing technical guidance throughout onboarding, testing, deployment, validation, and production support.
•	Designed, configured, tested, and supported REST APIs using Swagger/OpenAPI and Postman while helping customers successfully integrate with API services and resolve implementation issues.
•	Investigated customer-reported production issues across distributed systems, diagnosed API integration failures, performed root cause analysis, coordinated engineering escalations, and restored services within SLA commitments.
•	Partnered closely with software engineering, product management, and customer stakeholders to communicate customer issues, validate fixes, improve product quality, and enhance customer experience.
•	Monitored cloud-native production services using Prometheus, Grafana dashboards, Elasticsearch, Kibana, PagerDuty, logs, metrics, and alerting to proactively identify and troubleshoot customer-impacting issues.
•	Automated operational workflows and support processes using shell scripting and AI technologies including LLMs, RAG, MCP, AIOps, and MLOps, improving productivity and troubleshooting efficiency.
•	Authored operational runbooks, troubleshooting guides (TSGs), technical documentation, KPI dashboards, and executive reports to improve support consistency and customer self-service.
•	Led Agile Scrum ceremonies, Jira administration, release coordination, change management, and continuous improvement initiatives while collaborating across engineering, and customer-facing teams.

Operations and Support Engineer, Ericsson USA                                                                   November 2021 to June 2025
•	Delivered customer-facing technical support for cloud-native SaaS platforms by diagnosing complex production issues using Kubernetes, kubectl, Prometheus, Grafana, Elasticsearch, Kibana, and ITSM tools.
•	Deployed, configured, and maintained Azure Kubernetes Service (AKS) environments using Kubernetes, Helm, FluxCD, Terraform, Git, GitLab, and GitOps practices.
•	Troubleshot distributed cloud infrastructure and customer-impacting production issues using logging, monitoring, and observability tools.
•	Participated in 24×7 on-call rotations, responding to critical production incidents, leading root cause analysis, coordinating service restoration, and reducing Mean Time to Resolve (MTTR).
•	Collaborated with software engineering, R&D, product management, customer support, vendors, and cross-functional teams to resolve customer escalations and improve platform reliability.
•	Improved operational procedures, monitoring capabilities, automation, and engineering workflows through continuous process improvement initiatives.
•	Developed troubleshooting guides, operational procedures, technical documentation, and change management documentation to improve engineering effectiveness and customer support.

Software Developer, VividCloud USA                                                                                September 2019 to October 2021
•	Designed, developed, tested, debugged, and maintained Java-based REST APIs, backend services, and cloud-native microservices supporting scalable enterprise software.
•	Worked throughout the Software Development Lifecycle (SDLC), including design, implementation, testing, deployment, debugging, production support, and continuous improvement.
•	Collaborated with software engineers, product owners, QA teams, and customers to gather requirements, resolve production issues, implement new features, and improve application performance.
•	Supported customer API integrations, investigated defects, performed debugging and root cause analysis, and resolved production issues to ensure reliable customer experiences.
•	Performed API integration testing using Postman, created technical documentation, supported CI/CD pipelines, participated in Agile ceremonies, and contributed to continuous process improvements.
•	Built reusable software components and improved application maintainability, scalability, and operational reliability.

Senior Manager | Manager | Engineer network Operations, MTN Rwanda                             March 2006 - April 2018
•	Led technical operations, troubleshooting, service delivery, and performance management across Core, RAN, IP, and Transmission networks supporting large-scale distributed telecommunications infrastructure.
•	Managed 24×7 Network Operations Center (NOC) activities including incident management, customer escalations, operational readiness, service restoration, and continuous service improvement.
•	Coordinated customers, vendors, field engineers, and cross-functional technical teams to resolve complex customer-impacting issues while maintaining high service availability.
•	Developed operational procedures, troubleshooting guides, technical documentation, knowledge base content, KPI dashboards, and performance reports supporting engineering excellence.
•	Led infrastructure modernization initiatives, mentored engineering teams, managed technical projects, and promoted knowledge sharing and operational best practices across the organization.
"""

document_education = """
Master of Technology in Telecommunication Tshwane University of Technology, South Africa, 2007
Master of Science (MSc) in Electronic Engineering Ecole Supérieure d’Ingénieurs en Electronique et Electrotechnique, France, 2007 
Bachelor of Science (BSc) in Electrical Engineering University of the Witwatersrand, South Africa, 2004
"""

document_certification = """
AI Engineer Challenge by SuperDataScience (https://www.skool.com/ai-challenge)                                         2026
Lean Six Sigma Green Belt by Ericsson                                                                                  2026                                             
Cloud Native Fundamental 2024 by Ericsson                                                                         2024-2027
Microsoft Certified Azure Fundamentals by Microsoft                                                                    2024
Lean Six Sigma Yellow Belt by Ericsson                                                                                 2024                                             
Global Tech Talent 2023 by Ericsson                                                                                    2023 
AWS Certified Developer–Associate by Amazon Web Services Training & Certification                                 2020-2023                                                                    
Certified Associate in Project Management (CAPM) by Project Management Institute                                  2019-2027
Java and Object-oriented programming by Southern Maine Community College (SMCC)                                        2018
"""

#-----------------------------------------------------
# Chunking Function
#-----------------------------------------------------
def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    BOUNDARIES = ["\n\n", "\n", ". ", "? ", "! ", " "]

    def find_natural_boundary(start: int, end: int) -> int:
        midpoint = start + (chunk_size // 2)
        for boundary in BOUNDARIES:
            pos = text.rfind(boundary, midpoint, end)
            if pos != -1:
                return pos + len(boundary)
        return end

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            end = find_natural_boundary(start, end)
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return chunks

#-----------------------------------------------------
# RAG: Chunk, Embed & Store in ChromaDB
#-----------------------------------------------------
documents = [
    {"text": document_professional_summary, "source": "Professional Summary"},
    {"text": document_professional_experience, "source": "Professional Experience"},
    {"text": document_education, "source": "Education"},
    {"text": document_certification, "source": "Certification"}    
]

chunks = []
ids = []
metadatas = [] 

for doc in documents:
    # Prepare the lists
    chunks_ = split_text_into_chunks(doc["text"], chunk_size = 300, overlap = 30)
    ids_ = [str(uuid.uuid4()) for _ in range(len(chunks_))]
    metadatas_ = [{"source": doc["source"], "chunk_index": i} for i in range(len(chunks_))]

    # Add to main lists
    chunks.extend(chunks_)
    ids.extend(ids_)
    metadatas.extend(metadatas_)

# print for logs    
print(f"Created {len(chunks)} chunks:\n")

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} (ID: {ids[i]}, Source: {metadatas[i]['source']}, Index: {metadatas[i]['chunk_index']}, Length: {len(chunk)}):")
    print(chunk)
    print()

# Generate embeddings for all chunks
response = client.embeddings.create(
    model = "text-embedding-3-small",
    input = chunks
)
embeddings = [item.embedding for item in response.data]

# Verify embeddings for logs
print(f"Generated {len(embeddings)} embeddings")
print(f"Each embedding has {len(embeddings[0])} dimensions")

# initialize ChromaDB client (persitent storage)
chroma_client = chromadb.PersistentClient(path="./chroma_db_twin")
# Alternative: initialize ChromaDB client (in-memory storage)
#chroma_client = chromadb.Client()

# Get or create + Empty the collection before adding new data (for testing purposes)
collection = chroma_client.get_or_create_collection(name="digital_twin")
if collection.get()["ids"]:
    collection.delete(collection.get()["ids"])

# Adding data to ChromaDB
collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=chunks,
    metadatas=metadatas
)
pprint(collection.get())

#-----------------------------------------------------
# Tools
#-----------------------------------------------------
tools = []

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

# Create send_notification function

def send_notification(message: str):
    payload = {"user": pushover_user, "token": pushover_token, "message": message}
    requests.post(pushover_url, data = payload)

# Describe Pushover as an LLM tool
send_notification_function = {
    "name": "send_notification",
    "description": "Sends a push notification to the real-world version of you via pushover on Mobile. Use this if the user needs to alert the real-world version of you.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The notification message to send to the user's device"
            }
        },
        "required": ["message"]
    }
}

# Add Pushover to the list of tools for the LLM
tools.append({"type":"function", "function":send_notification_function})

# Simulates rolling a single six-sided dice 
def dice_roll ():
    result = random.randint(1,6)
    return result

# Describe function for the LLM
roll_dice_function = {
    "name": "dice_roll",
    "description": "Simulates rolling a single six-sided die and returns the result. Use this when the user wants to roll a die for games, decisions, or random number generations.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": []
        }
}
# Add roll_dice_function to the list of tools of LLM
tools.append({"type":"function", "function":roll_dice_function})

#-----------------------------------------------------
# Tool Handler
#-----------------------------------------------------
def handle_tool_call(tool_calls):
       tool_results = []

       for tool_call in tool_calls: 
              function_name = tool_call.function.name
              args = json.loads(tool_call.function.arguments)
              # print(f"Calling function {function_name}") # For future debugging

              # Route to the appropriate function based on function_name
              if function_name == "send_notification":
                     send_notification(args["message"])
                     content = f"Notification sent: {args['message']}"
              elif function_name == "dice_roll":
                     content = f"Rolled: {dice_roll()}"
              else:
                     content = f"Unknown function: {function_name}"

              tool_call_result = {
                     "role": "tool",
                     "content": content,
                     "tool_call_id": tool_call.id
              }

              tool_results.append(tool_call_result)

       return tool_results

#-----------------------------------------------------
# System Message
#-----------------------------------------------------
system_message = """You are a digital twin of Gaby Mutajogire. When people talk to you, you respond AS Gaby - in first person, using his voice, personality, and knowledge.


Important: do not make things up. If you don't know an answer, say you don't know.
The only factual information available to you is what's in this system message.
You cannot get any more facts about Gaby from the internet or make them up."""
#-----------------------------------------------------
# Main Response Function
#-----------------------------------------------------
def respond_ai(message, history):
    # RAG: Embed the query using the same model we used for the chunks to ensure compatibility    
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = [message]
    )
    query_embedding = response.data[0].embedding

    # RAG: Search ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    # RAG: Stitch retrieved chunks together to create the context for the response
    context = "\n---\n".join(results["documents"][0])

    # Print logs for debugging
    print("\n==========================================================\n")
    print(f"User message:\n{message}\n")
    print("***Retrieved Chunks:")
    for a,b in zip(results["documents"][0], results["metadatas"][0]):
        print("------------------------------------------------------------")
        print(f"<<Document {b['source']} -- Chunk {b['chunk_index']}>>\n{a}\n")

    # Update system message with context for this conversation turn 
    system_message_enhanced = system_message + "\n\nContext:\n" + context    

    # Build messages for this turn
    messages = [{"role": "system", "content": system_message_enhanced}] + history + [{"role": "user", "content": message}]   

    # Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools = tools
    )
    message = response.choices[0].message

    # Check if model wants to call a tool
    while message.tool_calls:
        pprint(message.tool_calls)     # print the function that is called

        tool_result = handle_tool_call(message.tool_calls) # whole list of tool calls on purpose
        messages.append(message)
        messages.extend(tool_result)

        response = client.chat.completions.create(
            model = "gpt-4.1-mini",
            messages = messages,
            tools = tools
        )
        message = response.choices[0].message    

        # Note: Maybe consider adding protection from infinite consecutive tool calling

    return(message.content)
#-----------------------------------------------------
# Launch Gradio
#-----------------------------------------------------
demo = gr.ChatInterface(fn=respond_ai)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860))
    )