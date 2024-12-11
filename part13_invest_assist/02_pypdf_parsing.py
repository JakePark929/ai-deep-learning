from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./src/bok_sample.pdf")
pages = loader.load_and_split()

text = pages[0].page_content

print(len(pages))
print(text)
