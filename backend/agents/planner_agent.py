from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.rag.retriever import ask_question

@tool
def retrieve_study_material(topic: str) -> str:
    """Retrieve relevant study material for a given topic from uploaded documents."""
    return ask_question(f"Explain the key concepts of: {topic}")

@tool
def generate_daily_schedule(subjects: str, days: int, hours_per_day: int) -> str:
    """Generate a day-wise study schedule given subjects, number of days, and hours per day."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)
    prompt = f"""
    Create a detailed {days}-day study plan for the following subjects: {subjects}.
    The student can study {hours_per_day} hours per day.
    Break it into morning/afternoon/evening sessions.
    Format it clearly day by day.
    """
    return llm.invoke(prompt).content

def run_planner_agent(subjects: str, days: int, hours_per_day: int) -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tools = [retrieve_study_material, generate_daily_schedule]

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert AI study planner. 
        Use the tools to retrieve study material and generate a personalized study schedule.
        Always retrieve relevant material first, then create the schedule."""),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    result = executor.invoke({
        "input": f"Create a {days}-day study plan for: {subjects}. Student has {hours_per_day} hours/day."
    })
    return result["output"]