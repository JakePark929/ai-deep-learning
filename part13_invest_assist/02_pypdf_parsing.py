from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./src/bok_sample.pdf")
pages = loader.load_and_split()

text_2 = pages[2].page_content
text_3 = pages[3].page_content

print(text_2)
print(text_3)
