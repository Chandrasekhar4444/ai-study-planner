from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

@tool
def analyze_quiz_scores(scores: str) -> str:
    """Analyze quiz scores and identify weak areas."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    prompt = f"""
    Analyze these quiz results: {scores}
    Identify:
    1. Strong topics (score > 70%)
    2. Weak topics (score < 70%)
    3. Topics to revisit
    Return a clear analysis.
    """
    return llm.invoke(prompt).content

@tool
def suggest_improvements(weak_topics: str) -> str:
    """Suggest study strategies for weak topics."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    prompt = f"""
    The student is struggling with: {weak_topics}
    Suggest 3-5 specific, actionable study strategies to improve in these areas.
    Be practical and encouraging.
    """
    return llm.invoke(prompt).content

def run_progress_agent(scores_data: dict) -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tools = [analyze_quiz_scores, suggest_improvements]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an AI academic coach. 
        Analyze student progress and provide actionable improvement suggestions."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = executor.invoke({
        "input": f"Analyze this student's quiz performance and suggest improvements: {str(scores_data)}"
    })
    return result["output"]