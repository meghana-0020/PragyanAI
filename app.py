import os
import pandas as pd
import streamlit as st

from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.documents import Document

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

from langchain_core.output_parsers import StrOutputParser

from langchain_community.chat_message_histories import ChatMessageHistory

from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_groq import ChatGroq



# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()


# =====================================================
# STREAMLIT CONFIG
# =====================================================

st.set_page_config(
    page_title="PragyanAI Assistant",
    layout="wide"
)


st.title(
    "🤖 PragyanAI Conversational Sales & FAQ Assistant"
)


st.caption(
    "AI assistant trained on PragyanAI Presentation & FAQ Knowledge Base"
)



# =====================================================
# GROQ API KEY
# =====================================================

groq_api_key = os.getenv(
    "GROQ_API_KEY"
)


if not groq_api_key:

    st.error(
        "GROQ_API_KEY missing. Add it in .env file"
    )

    st.stop()



# =====================================================
# LLM
# =====================================================

llm = ChatGroq(

    groq_api_key=groq_api_key,

    model_name="llama-3.3-70b-versatile",

    temperature=0.3

)



# =====================================================
# PERSONAS
# =====================================================

SALES_PROMPTS = {


"PragyanAI Student Counselor":

"""
You are Aarav, Academic & Career Advisor for PragyanAI.

Guide students about:

- 18 Month AI/GenAI Program
- Fees
- Curriculum
- Placement
- Career opportunities


Answer only using context.

Context:

{context}
""",



"PragyanAI Institutional / CoE Advisor":

"""
You are Dr Kavita, Institutional Relations Lead.

Explain:

- College partnerships
- AI transformation
- Student outcomes

Answer only from context.


Context:

{context}

""",



"PragyanAI Enterprise AI & Placement Lead":

"""
You are Rohan, Enterprise Placement Lead.

Explain:

- Hiring partnerships
- AI engineers
- Enterprise AI solutions

Mention:

LangChain
RAG
Generative AI
Agentic AI


Context:

{context}

"""

}




# =====================================================
# MEMORY
# =====================================================

if "store" not in st.session_state:

    st.session_state.store = {}



def get_session_history(session_id):

    if session_id not in st.session_state.store:

        st.session_state.store[session_id] = ChatMessageHistory()


    return st.session_state.store[session_id]




def clear_memory():

    st.session_state.store = {}

    st.session_state.messages = []




# =====================================================
# EMBEDDINGS
# =====================================================


embeddings = HuggingFaceEmbeddings(

    model_name="all-MiniLM-L6-v2"

)




# =====================================================
# LOAD DOCUMENTS
# =====================================================

def load_documents(files=None):

    docs=[]


    # uploaded files

    if files:

        for file in files:


            if file.name.endswith(".pdf"):

                loader = PyPDFLoader(
                    file.name
                )

                docs.extend(
                    loader.load()
                )


            elif file.name.endswith(".xlsx"):


                df = pd.read_excel(
                    file
                )


                for _,row in df.iterrows():

                    text=" | ".join(

                        [
                            f"{c}: {v}"

                            for c,v in row.items()

                        ]

                    )


                    docs.append(

                        Document(
                            page_content=text
                        )

                    )



    # default excel

    if os.path.exists(
        "pragyan_faq_prices.xlsx"
    ):


        df=pd.read_excel(
            "pragyan_faq_prices.xlsx"
        )


        for _,row in df.iterrows():

            text=" | ".join(

                [
                    f"{c}: {v}"

                    for c,v in row.items()

                ]

            )


            docs.append(

                Document(
                    page_content=text
                )

            )



    if not docs:


        docs.append(

            Document(

                page_content="""
                PragyanAI is an 18 month AI GenAI program.
                6 months offline training and
                12 months placement drive.
                """

            )

        )


    return docs





# =====================================================
# VECTOR DATABASE
# =====================================================


if "vectorstore" not in st.session_state:


    with st.spinner(
        "Loading Knowledge Base..."
    ):


        documents = load_documents()


        st.session_state.vectorstore = FAISS.from_documents(

            documents,

            embeddings

        )



# =====================================================
# RAG FUNCTION
# =====================================================


def respond(message, persona):


    retriever = st.session_state.vectorstore.as_retriever(

        search_kwargs={
            "k":4
        }

    )


    docs = retriever.invoke(
        message
    )


    context="\n".join(

        [
            d.page_content

            for d in docs

        ]

    )



    system_prompt = SALES_PROMPTS[persona].format(

        context=context

    )



    prompt = ChatPromptTemplate.from_messages(

        [

            (
                "system",
                system_prompt
            ),


            MessagesPlaceholder(

                variable_name="history"

            ),


            (
                "human",
                "{input}"
            )

        ]

    )



    chain = (

        prompt

        |

        llm

        |

        StrOutputParser()

    )



    memory_chain = RunnableWithMessageHistory(

        chain,

        get_session_history,

        input_messages_key="input",

        history_messages_key="history"

    )



    result = memory_chain.invoke(

        {
            "input":message
        },

        config={

            "configurable":{

                "session_id":persona

            }

        }

    )


    return result





# =====================================================
# SIDEBAR
# =====================================================


with st.sidebar:


    st.header(
        "PragyanAI Settings"
    )


    persona = st.selectbox(

        "Select Persona",

        list(SALES_PROMPTS.keys())

    )


    files = st.file_uploader(

        "Upload PDF / Excel",

        type=[
            "pdf",
            "xlsx"
        ],

        accept_multiple_files=True

    )



    if st.button(
        "Update Knowledge Base"
    ):


        docs=load_documents(
            files
        )


        st.session_state.vectorstore = FAISS.from_documents(

            docs,

            embeddings

        )


        st.success(
            f"{len(docs)} documents loaded"
        )



    if st.button(
        "Clear Memory"
    ):

        clear_memory()




# =====================================================
# CHAT UI
# =====================================================


if "messages" not in st.session_state:

    st.session_state.messages=[]



for msg in st.session_state.messages:


    with st.chat_message(
        msg["role"]
    ):

        st.write(
            msg["content"]
        )



user_input = st.chat_input(

    "Ask PragyanAI..."

)



if user_input:


    st.session_state.messages.append(

        {
            "role":"user",
            "content":user_input
        }

    )


    with st.chat_message(
        "user"
    ):

        st.write(
            user_input
        )



    with st.chat_message(
        "assistant"
    ):


        with st.spinner(
            "Thinking..."
        ):


            answer = respond(

                user_input,

                persona

            )


            st.write(
                answer
            )



    st.session_state.messages.append(

        {
            "role":"assistant",
            "content":answer
        }

    )
