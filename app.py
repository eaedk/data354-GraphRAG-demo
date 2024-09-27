import asyncio
import random
import os
from concurrent.futures import ThreadPoolExecutor

from neo4j_graphrag.retrievers import VectorRetriever, VectorCypherRetriever
from neo4j_graphrag.generation import GraphRAG, RagTemplate
from neo4j import GraphDatabase
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.types import RetrieverResultItem

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_ollama import OllamaEmbeddings, ChatOllama

import streamlit as st
from dotenv import load_dotenv

from code.config import Config

# Load environment variables from a .env file
load_dotenv()

PROMPT_TEMPLATE = RagTemplate(
    template="""You are an expert RAG assistant. Your task is to
    answer the user's question based on the provided context. Use only the
    information within that context.

    Context:
    {context}

    Question:
    {query_text}

    Answer:
    """
)

# List of humorous loading messages to display while processing
LOADING_MESSAGES = [
    "Calculating your answer through multiverse...",
    "Adjusting quantum entanglement...",
    "Summoning star wisdom... almost there!",
    "Consulting Schrödinger's cat...",
    "Warping spacetime for your response...",
    "Balancing neutron star equations...",
    "Analyzing dark matter... please wait...",
    "Engaging hyperdrive... en route!",
    "Gathering photons from a galaxy...",
    "Beaming data from Andromeda... stand by!",
]

# Set up the Streamlit page configuration
st.set_page_config(page_title="GraphRAG", page_icon="🧠🧐")

# Custom CSS to adjust the size of the loading spinner
st.markdown(
    """
    <style>
        .st-emotion-cache-p4micv {
            width: 2.75rem;
            height: 2.75rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize the message history in the session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! What do you want to know about your documents?",
        }
    ]

def show_message_history():
    """
    Display the chat history from the session state.
    Each message is displayed with an appropriate avatar based on the role.
    """
    for message in st.session_state.messages:
        role = message["role"]
        avatar_path = (
            Config.Path.IMAGES_DIR / "assistant-avatar.png"
            if role == "assistant"
            else Config.Path.IMAGES_DIR / "user-avatar.png"
        )
        with st.chat_message(role, avatar=str(avatar_path)):
            st.markdown(message["content"])

async def ask_question(chain: GraphRAG, question: str, session_id: str):
    """
    Asynchronous generator to handle question processing.

    Args:
        chain (GraphRAG): The GraphRAG instance.
        question (str): The user's question.
        session_id (str): Session identifier.

    Yields:
        str: Parts of the response as they become available.
    """
    # Run the synchronous search method in a separate thread
    response = await asyncio.to_thread(chain.search, question)
    
    # Yield the full response
    yield response

async def ask_chain(question: str, chain: GraphRAG):
    """
    Handle the assistant's response to a user's question.
    Displays a loading message while processing and updates the chat with the full response.

    Args:
        question (str): The user's question.
        chain (GraphRAG): The RAG chain to handle the question.
    """
    assistant = st.chat_message(
        "assistant", avatar=str(Config.Path.IMAGES_DIR / "assistant-avatar.png")
    )
    with assistant:
        message_placeholder = st.empty()
        # Display a random loading message
        message_placeholder.text(random.choice(LOADING_MESSAGES))
        
        full_response = ""
        try:
            # Asynchronously iterate over the response events
            async for event in ask_question(chain, question, session_id="session-id-42"):
                if isinstance(event, str):
                    full_response += event
                    message_placeholder.markdown(full_response)
                elif isinstance(event, list):
                    # Handle additional documents or data if necessary
                    pass
        except Exception as e:
            message_placeholder.error(f"An error occurred: {e}")

    # Append the assistant's response to the session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Initialize a ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=2)

def show_chat_input_sync(chain: GraphRAG):
    """
    Display the chat input box where users can type their questions.
    Upon submission, the user's message is added to the history, and the assistant's response is triggered.

    Args:
        chain (GraphRAG): The QA chain or processing object to handle user queries.
    """
    if prompt := st.chat_input("Ask your question here"):
        # Add user's message to the session state
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message(
            "user",
            avatar=str(Config.Path.IMAGES_DIR / "user-avatar.png"),
        ):
            st.markdown(prompt)
        
        # Create a placeholder for the assistant's response
        assistant_placeholder = st.empty()

        def handle_ask_chain_sync():
            full_response = ""
            try:
                # Display a random loading message
                assistant_placeholder.text(random.choice(LOADING_MESSAGES))
                
                # Perform the search synchronously
                response = chain.search(prompt)
                full_response += response
                assistant_placeholder.markdown(full_response)
            except Exception as e:
                assistant_placeholder.error(f"An error occurred: {e}")
            
            # Append the assistant's response to the session state
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        # Schedule the synchronous task in a separate thread
        executor.submit(handle_ask_chain_sync())

@st.cache_resource
def setup_RAG():
    " setup the app configuration"
    # DB config
    driver = GraphDatabase.driver(
        uri=os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])
    )
    
    # For computing embedding
    embedder = OllamaEmbeddings(model=Config.Model.EMBEDDINGS) if Config.Model.USE_LOCAL else OpenAIEmbeddings(model=Config.Model.EMBEDDINGS) 
    
    # For querying the DB
    retriever = VectorRetriever(
        driver,
        index_name=Config.Database.DOCUMENTS_COLLECTION,
        embedder=embedder
        # return_properties=["title", "plot"],
    )

    # LLM
    if Config.Model.USE_LOCAL:
        llm = ChatOllama(model=Config.Model.LOCAL_LLM, temperature=Config.Model.TEMPERATURE)
    else:
        llm = OpenAILLM(model_name=Config.Model.REMOTE_LLM, model_params={"temperature": Config.Model.TEMPERATURE})
        # llm = ChatGroq(temperature=0, groq_api_key=os.environ["GROQ_API_KEY"], model_name="Gemma2-9b-It")
    
    # Initialize the RAG pipeline
    graph_rag_chain = GraphRAG(retriever=retriever, llm=llm, prompt_template=PROMPT_TEMPLATE)

    return graph_rag_chain

# def show_chat_input_async(chain: GraphRAG):
#     """
#     Display the chat input box where users can type their questions.
#     Upon submission, the user's message is added to the history, and the assistant's response is triggered.

#     Args:
#         chain (GraphRAG): The QA chain or processing object to handle user queries.
#     """
#     if prompt := st.chat_input("Ask your question here"):
#         # Add user's message to the session state
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         with st.chat_message(
#             "user",
#             avatar=str(Config.Path.IMAGES_DIR / "user-avatar.png"),
#         ):
#             st.markdown(prompt)
        
#         # Create a placeholder for the assistant's response
#         assistant_placeholder = st.empty()

#         # Define the asynchronous task
#         async def handle_ask_chain():
#             await ask_chain(prompt, chain)
        
#         # Schedule the asynchronous task
#         asyncio.create_task(handle_ask_chain())

def main():
    """
    The main function to run the Streamlit application.
    It displays the message history and the chat input box.
    """
    # Setup the RAG 
    graph_rag_chain = setup_RAG()

    # Display the chat history
    show_message_history()
    
    # Display the chat input box (synchronous)
    show_chat_input_sync(chain=graph_rag_chain)

if __name__ == "__main__":
    main()
