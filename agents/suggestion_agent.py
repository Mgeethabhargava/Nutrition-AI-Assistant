# agents/suggestion_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
import os

# Tool: Dummy suggestion tool for personalization
@tool
def meal_suggestion_tool(query: str) -> str:
    """Suggest a meal plan based on the user query."""
    # In real app, integrate this with nutrition data / rules
    return f"Here's a meal plan suggestion based on your query: {query}"

tools = [meal_suggestion_tool]

# Prompt with required variables
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a nutrition suggestion expert. Use tools to generate meal suggestions based on the user's query.\n"
        "Available tools: {tool_names}\n\n{tools}\n"
    )),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Suggestion agent
suggestion_agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
suggestion_agent = AgentExecutor(agent=suggestion_agent, tools=tools, verbose=True)
