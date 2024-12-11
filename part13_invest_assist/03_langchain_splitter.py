from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

loader = PyPDFLoader("./src/bok_sample.pdf")
pages = loader.load_and_split()

text = pages[0].page_content
print(len(text))

text_splitter = CharacterTextSplitter(
    separator='\n',
    chunk_size=500,
    chunk_overlap=100,
    length_function=len
)

texts = text_splitter.split_text(text)

print(len(texts[0]))

print(f'청크 수: {len(texts)}')
print(f'청크 1: {texts[0]}')
print(f'청크 2: {texts[1]}')
