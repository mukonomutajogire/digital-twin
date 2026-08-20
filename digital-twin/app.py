import os
from openai import OpenAI
import gradio as gr

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
    # Update system message with context for this conversation turn 
    system_message_enhanced = system_message + "\n\nContext:\n" + document_professional_experience

    # Logs for debugging 
    print("\n===========================================\n")
    print("***User message:\n", message)
    print("\nContext this turn:\n", system_message_enhanced)
    

    # Build messages for this turn
    messages = [{"role": "system", "content": system_message_enhanced}] + history + [{"role": "user", "content": message}]   

    # Call LLM
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )
    message = response.choices[0].message

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