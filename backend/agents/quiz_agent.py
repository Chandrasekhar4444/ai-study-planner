from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.rag.retriever import ask_question
import json

@tool
def fetch_topic_content(topic: str) -> str:
    """Fetch content about a topic from the uploaded study material."""
    return ask_question(f"What are the main points about {topic}?")

@tool
def create_quiz_questions(topic: str, num_questions: int) -> str:
    """Generate multiple choice quiz questions for a topic."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5)
    prompt = f"""
    Generate {num_questions} multiple choice questions about: {topic}
    
    Return ONLY a JSON array in this format:
    [
      {{
        "question": "question text",
        "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
        "answer": "A) option1",
        "explanation": "brief explanation"
      }}
    ]
    Return only the JSON, no other text.
    """
    response = llm.invoke(prompt).content
    return response

def run_quiz_agent(topic: str, num_questions: int = 5):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tools = [fetch_topic_content, create_quiz_questions]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an AI quiz generator. 
        First fetch content about the topic, then generate quiz questions based on that content."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = executor.invoke({
        "input": f"Generate {num_questions} quiz questions about: {topic}"
    })

    try:
        output = result["output"]
        start = output.find("[")
        end = output.rfind("]") + 1
        json_str = output[start:end]
        return json.loads(json_str)
    except:
        return []