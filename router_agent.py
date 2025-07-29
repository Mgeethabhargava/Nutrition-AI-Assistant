# router_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, initialize_agent
from langchain.agents.agent_toolkits import create_react_agent
from langchain.tools.render import render_text_description
from langchain.chains.router import MultiPromptRouterChain
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

from tools.rag_tool import rag_tool

# Optional: Use os.getenv("OPENAI_API_KEY") if using environment variables
llm = ChatOpenAI(temperature=0.2, model="gpt-4")

# Create prompt-to-chain mapping for router
prompt_infos = [
    {
        "name": "nutrition",
        "description": "Good for answering nutrition facts or meal analysis",
        "prompt_template": PromptTemplate.from_template(
            "You're a nutrition expert. Answer: {input}"
        )
    },
    {
        "name": "rag",
        "description": "Helpful when the user asks questions about documents, research, or ingested PDFs",
        "prompt_template": PromptTemplate.from_template(
            "Use document context to answer: {input}"
        )
    },
    {
        "name": "default",
        "description": "Fallback for general health or nutrition questions",
        "prompt_template": PromptTemplate.from_template(
            "You're a helpful AI assistant. Answer: {input}"
        )
    }
]

# Create chains for each route
destination_chains = {}
for prompt_info in prompt_infos:
    chain = LLMChain(llm=llm, prompt=prompt_info["prompt_template"])
    destination_chains[prompt_info["name"]] = chain

# Router chain
router_chain = MultiPromptRouterChain(
    llm=llm,
    destination_chains=destination_chains,
    default_chain=destination_chains["default"],
    prompt_infos=prompt_infos
)

# Tools to inject into final agent (can be triggered based on output)
tools = [nutrition_tool, rag_tool]

# Final agent with tool usage
agent = initialize_agent(
    tools,
    llm,
    agent_type="zero-shot-react-description",
    verbose=True,
)

# Entry function to route and respond
def nutrition_agent_router(user_input: str) -> str:
    routing_response = router_chain.run(user_input)

    # Optionally check if tool use is triggered inside response
    # (Or route to agent executor for hybrid tool+LLM response)
    return routing_response
