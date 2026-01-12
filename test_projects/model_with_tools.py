import os
import streamlit as st
import json
import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# --- 1. SETUP AND INITIALIZATION ---

# Load API key from environment variables
load_dotenv()

# Setup model (Using gpt-4o-mini for its strong ability to follow structured output instructions)
# Set temperature low to encourage more deterministic tool-use decisions
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# Initialize Session State Variables
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()
if "world_model" not in st.session_state:
    # This list is the external 'World Model' (Model-Based Agent, B)
    st.session_state.world_model = []
if "response_history" not in st.session_state:
    st.session_state.response_history = []


# --- 2. AGENT ACTUATORS (TOOLS) ---

# This function acts as a digital "Actuator" that modifies the external world state (Model)
def add_task_to_model(task_description: str):
    """Adds a task to the agent's external to-do list (World Model)."""
    if task_description and task_description not in st.session_state.world_model:
        st.session_state.world_model.append(task_description)
        return f"Successfully added task: '{task_description}' to the world model."
    return "Task already exists or was empty. No change made."

# This is a hypothetical tool the agent can "use" (Utility-Based Agent, D)
def check_time_and_urgency(query: str):
    """Estimates the current time and provides a generic assessment of query urgency."""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    if "urgent" in query.lower() or "now" in query.lower():
        return f"The current time is {current_time}. Your request seems urgent and should be prioritized."
    return f"The current time is {current_time}. You can proceed with the task."


# --- 3. STRUCTURED OUTPUT SCHEMA (Utility-Based Agent, D) ---
# We define the *exact* JSON structure the LLM MUST return if it decides to use a tool.
# This replaces the brittle text-based instruction block.

class ToolCall(BaseModel):
    """A tool call request, used when the agent needs to take a specific action."""
    action: str = Field(description="The name of the tool to be called (add_task_to_model or check_time_and_urgency).")
    action_input: str = Field(description="The string argument to pass to the selected tool.")


# --- 4. AGENT SYSTEM PROMPT (MODEL INJECTION & UTILITY LOGIC) ---

SYSTEM_PROMPT = """
You are a 'Goal-Oriented Agent' focused on user task management. Your goal is to maximize user satisfaction (Utility).

Based on the user's request, decide whether to:
1. Respond conversationally (if no action is needed).
2. Use one of your internal Tools (if an action is required to update the world state or provide information).

# CURRENT WORLD STATE (Model-Based Reflex Agent - B):
This is the current state of your external task list. Use this information when answering questions about tasks.
TASKS: {tasks}

# TOOL INSTRUCTION:
If you decide to use a tool, you MUST output a JSON object strictly conforming to the provided schema. If you do not use a tool, provide a standard text response.

# AVAILABLE TOOLS:
- add_task_to_model(task_description: str): Use this when the user explicitly asks to add something to their list.
- check_time_and_urgency(query: str): Use this when the user asks about time or urgency.
"""


# --- 5. STREAMLIT UI AND AGENT LOGIC ---

st.set_page_config(layout="wide")
st.title("🤖 Robust Goal-Oriented LLM Agent (V2)")
st.caption("Now using Pydantic for reliable tool calling, eliminating JSON parsing errors.")

# Display World Model (External State)
st.sidebar.markdown("### 🌎 Agent's External World State (Model)")
if st.session_state.world_model:
    for i, task in enumerate(st.session_state.world_model):
        st.sidebar.markdown(f"- **{i+1}.** {task}")
else:
    st.sidebar.info("The task list is empty. Ask the agent to add a task!")

# Main chat input
user_input = st.chat_input("Ask the agent to manage a task (e.g., 'Please add buying milk to my list')")

if user_input:
    st.session_state.response_history.append({"role": "user", "content": user_input})

    # 1. Update the prompt with the latest World State before prediction
    formatted_prompt = SYSTEM_PROMPT.format(tasks=st.session_state.world_model)
    
    # We use a custom chain for prediction to try and force structured output first
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", formatted_prompt),
        ("ai", st.session_state.memory.buffer),
        ("user", user_input)
    ])
    
    # Attempt to get a tool call using the structured parser (D - Utility Decision)
    structured_llm = llm.with_structured_output(ToolCall, include_raw=True)
    
    # 2. Get the agent's raw response
    try:
        # Predict using the structured LLM instance
        response_data = structured_llm.invoke(prompt_template.format_messages(
            tasks=st.session_state.world_model, 
            user=user_input
        ))
        
        # If successful, response_data is a dictionary with 'raw' and the parsed object
        tool_call = response_data['parsed']
        tool_name = tool_call.action
        tool_input = tool_call.action_input

        # Execute the tool (Actuator)
        agent_message = f"**Agent Plan:** Decided to use tool `{tool_name}` with input: *'{tool_input}'*."
        
        if tool_name == "add_task_to_model":
            tool_output = add_task_to_model(tool_input)
        elif tool_name == "check_time_and_urgency":
            tool_output = check_time_and_urgency(tool_input)
        else:
            tool_output = f"Error: Unknown tool {tool_name}."
        
        final_response = f"**Tool Execution Result:** {tool_output}"
        
        # Update conversation memory with the original conversational prompt and the tool's result
        st.session_state.memory.save_context({"input": user_input}, {"output": final_response})


    except Exception as e:
        # If structured parsing fails (meaning the model decided to chat instead),
        # use the regular conversational chain.
        # Note: If the error is *not* a structured output failure but a generic one, this might catch it.
        # We assume if structured output fails, the model intended a conversational response.
        
        # Use the standard chain for conversational response
        conversation_chain.prompt = formatted_prompt # Ensure memory is up-to-date
        final_response = conversation_chain.predict(input=user_input)
        agent_message = "**Agent Conversation:**"


    # 3. Display Final Response
    st.session_state.response_history.append({"role": "agent", "content": final_response})
    # Streamlit will automatically rerun and update the sidebar due to session state changes.


# Display Conversation History
st.markdown("---")
st.markdown("### 💬 Conversation History")
chat_container = st.container(height=500, border=True)

with chat_container:
    for chat in st.session_state.response_history:
        if chat["role"] == "user":
            st.chat_message("user").write(chat["content"])
        else:
            # Use 'assistant' role for the agent's processed output
            st.chat_message("assistant").write(chat["content"])



    
