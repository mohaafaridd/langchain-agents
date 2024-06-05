from langchain_openai import OpenAI, ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from init_stocks_db import engine
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain.agents import Tool, create_react_agent, AgentExecutor
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain import hub
from langchain.memory import ConversationBufferMemory

load_dotenv()

llm = ChatOpenAI(temperature=0)

db = SQLDatabase(engine)

sql_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)

sql_tool = Tool(
    name="Stock DB",
    func=sql_chain.run,
    description="Useful for when you need to answer questions about stocks and their prices.",
)

tools = load_tools(
    ["llm-math"],
    llm=llm,
)

tools.append(sql_tool)

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
# memory = ConversationBufferMemory(memory_key="chat_history")

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# conversational_agent = AgentExecutor(
#     agent=agent, tools=tools, verbose=True, memory=memory
# )

# Provide different answer from the video :(
result = agent_executor.invoke(
    {
        "input": "What is the multiplication of the ratio between stock "
        + "prices for 'ABC' and 'XYZ' in January 3rd and the ratio "
        + "between the same stock prices in January the 4th?",
    }
)
# result = conversational_agent.invoke(
#     {
#         "input": "What's the result of an investment of $10,000 growing at 8% annually for 5 years with compound interest?"
#     }
# )
