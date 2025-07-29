from langchain_core.tools import Tool
from langchain_core.runnables import RunnableSequence
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent

from tools.rag_tool import rag_tool
from agents.suggestion_agent import meal_suggestion_tool
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logger import log_prompt_response
from diary_db import log_meal_diary, log_chat

# 1. Setup LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.2)

# 2. List of tools
tools = [
    rag_tool,
    meal_suggestion_tool,
]

# 3. Create ReAct agent with tool use
# prompt = ChatPromptTemplate.from_messages([
#     ("system", (
#         "You are a helpful Nutrition AI assistant. You have access to the following tools: {tool_names}.\n\n"
#         "Use them if needed to answer the user’s query. Think step-by-step before using tools.\n\n"
#         "TOOLS:\n{tools}\n\n"
#     )),
#     ("human", "{input}"),
#     MessagesPlaceholder(variable_name="agent_scratchpad"),  # correct usage
# ])
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)
nutrition_agent = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. Wrapper for app.py
def run_nutrition_agent(user_query: str, username: str) -> str:
    try:
        response = nutrition_agent.invoke({
            "input": user_query
        })
        result = response.get("output", "Sorry, I couldn't process that.")
        
        # Logging
        # log_prompt_response(username, user_query, result)
        # log_chat(username, user_query, result)
        # log_meal_diary(username, result)

        return result
    except Exception as e:
        return f"⚠️ Agent Error: {str(e)}"
