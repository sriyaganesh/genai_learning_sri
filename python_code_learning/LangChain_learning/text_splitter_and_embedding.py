from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter


print("\n")
# PDF Load
pdf_file=PyPDFLoader("C:/Users/SrividhyaGanesan/OneDrive - EPAM/Sri/AI/genai_learning_sri/python_code_learning/llm_details.pdf")
result_pdf=pdf_file.load()
print(result_pdf)

full_text="\n".join([doc.page_content for doc in result_pdf])

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base", chunk_size=100, chunk_overlap=0
)
texts= text_splitter.split_text(full_text)
print(texts)


rec_text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base", chunk_size=100, chunk_overlap=0
)
rec_texts= rec_text_splitter.split_text(full_text)
print(texts)


######################


from langchain_openai  import OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
openai_embed=OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
textembed="This is a sample text to be embedded"
embeded=openai_embed.embed_query(textembed)
print("Embedding:",embeded)
print(embeded[:5])



from langchain_community.embeddings  import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
huggingface_embed=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text_for_embed="This is a sample text to be embedded"
huggingface_embeded=huggingface_embed.embed_query(text_for_embed)
#print("Embedding:",huggingface_embeded)
print(huggingface_embeded[:5])







