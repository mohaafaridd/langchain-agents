from langchain_openai import OpenAI
from langchain.chains.llm_math.base import LLMMathChain
from langchain.chains.llm import LLMChain
from langchain.agents import Tool
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from dotenv import load_dotenv
from langchain_community.agent_toolkits.load_tools import load_tools
load_dotenv()

llm = OpenAI(temperature=0)

llm_math = LLMMathChain.from_llm(llm)

math_tool = Tool(
  name="Calculator",
  func=llm_math.run,
  description="Useful for when you need to answer questions about math."
)

prompt = PromptTemplate(
  input_variables=["query"],
  template="{query}"
)

llm_chain = LLMChain(llm=llm, prompt=prompt)

llm_tool = Tool(
  name="Language Model",
  func=llm_chain.run,
  description="Use this tool for general purpose queries and logic"
)

# tools = [llm_tool, math_tool]
tools = load_tools(
  ['llm-math'],
  llm=llm,
)

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(
  llm=llm,
  tools=tools,
  prompt=prompt
)

agent_executor = AgentExecutor(agent=agent,tools=tools,verbose=True)

agent_executor.invoke({"input": "what is (4.5*2.1)^2.2?"})
agent_executor.invoke({"input": "if Mary has four apples and Giorgio brings two and a half apple "
                "boxes (apple box contains eight apples), how many apples do we "
                "have?"})
# agent_executor.invoke({"input": "what is the capital of Norway?"})

