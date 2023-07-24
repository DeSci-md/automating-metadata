"""
Use of openai plus langchain for processing information in a pdf
"""
from dotenv import load_dotenv, find_dotenv  # loading in API keys

from langchain.document_loaders import PyPDFLoader  # document loader import
from langchain.text_splitter import CharacterTextSplitter  # for use with loader
from langchain.llms import OpenAI  # LLM import
from langchain import LLMChain  # Agent import
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts.chat import (  # prompts for designing inputs
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)


# Load in API keys from .env file
load_dotenv(find_dotenv())


# Define the PDF document and load it in
loader = PyPDFLoader("Zou et al_2013_ZnO nanorods on reduced graphene sheets with excellent field emission, gas.pdf")
document = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(document)  # splits into chunks


# Define language model to use
llm = OpenAI(model_name="text-davinci-003", temperature=0)


# Defining system and human prompts with variables
system_template = "You are a scientific researcher reading the following publication text: {doc_text}."
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)  # providing the system prompt

human_template = "{query}. {format_instructions}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


# Structured Output Schema
title_schema = ResponseSchema(name="title", description="This is the publication title of the paper")
authors_schema = ResponseSchema(name="authors", description="This is a list of the names of the authors of the paper")

response_schema = [title_schema, authors_schema]

output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions()


# Defining the chain to combine the language model and prompt
chain = LLMChain(llm=llm, prompt=chat_prompt)

query = "What is the title of this paper, and who are the authors?"
out = chain.run(doc_text=docs[0], query=query, format_instructions=format_instructions)
out_dict = output_parser.parse(out)

# Modifying the author output to be a list of names
out_authors = out_dict["authors"]
out_authors = out_authors.replace(' and', ',')  # TODO: better way to do this with regex
out_authors_formatted = out_authors.split(',')
out_dict['authors'] = out_authors_formatted

print(f"Response as dict: {out_dict}")

print(out_dict['title'])
print(out_dict['authors'])
