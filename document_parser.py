from langchain_community.document_loaders import PyPDFLoader
import tempfile
from fastapi import FastAPI, UploadFile, File


app = FastAPI(
    title="LangChain  Server(Document Parser)",
    version="1.0",
    description="A simple api server using Langchain's document_loaders",
)

@app.get('/home')
async def homepage():
    return {"message": "welcome here"}


@app.post("/parse_pdf")
async def parse_pdf(pdf:UploadFile = File(...)):
    try:
        pdf_file = await pdf.read()
        temp = tempfile.NamedTemporaryFile()
        temp.write(pdf_file)
        loader = PyPDFLoader(temp.name)
        pages = loader.load_and_split()
        temp.close()
        return [{"page_content": p.page_content, "page": p.metadata.get('page') } for p in pages]
    except Exception as e:
        print("shit happened")
        return {"error": str(e)}
