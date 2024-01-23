from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Import the csrf_exempt decorator
import os
import whisper
import sys
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import CTransformers
import pickle
import faiss
from langchain.vectorstores import FAISS
from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from django.views.decorators.http import require_POST
from googletrans import Translator
import json

model = whisper.load_model("small")
options = whisper.DecodingOptions(language="en")

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
from google.colab import drive
file1 = open(f"/content/Saarthi/Databases/prefinal.txt", "r+")
new=file1.readlines()

file2 = open("/content/Saarthi/Databases/second.txt", "r+",encoding="utf-8")
new2 = file2.readlines()

with open('/content/Saarthi/Databases/metas4.pickle','rb') as handle:
  c= pickle.load(handle)

from langchain.text_splitter import RecursiveCharacterTextSplitter , Document
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
docs = text_splitter.split_documents([Document(page_content=new[i]) for i in range(len(new))])
from langchain.embeddings import HuggingFaceInstructEmbeddings
instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl",
                                                      model_kwargs={"device": "cuda"},
                                                     )
docs2 = []
for j, i in enumerate(c):
  doc = Document(page_content = new2[j], metadata = i)
  docs2.append(doc)


faiss_index = FAISS.from_documents(docs, instructor_embeddings)
second_index = FAISS.from_documents(docs2, instructor_embeddings)
from langchain import HuggingFaceHub

llm = HuggingFaceHub(
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    model_kwargs={"temperature":0.55, "max_length":10}
)
qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    faiss_index.as_retriever(search_kwargs={'k': 3}),
    return_source_documents=True
)


@csrf_exempt  # Apply the decorator here
def index(request):
    return render(request, 'bot/index.html')

@csrf_exempt  # Apply the decorator here
def save_audio(request):
    if request.method == 'POST' and 'audio' in request.FILES:
        audio_file = request.FILES['audio']
        language_trans = request.POST.get('language', 'en')
        # Save the audio file in the media directory
        audio_path = os.path.join('media', audio_file.name)
        with open(audio_path, 'wb') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # Use whisper to transcribe the saved audio file
        audio=whisper.load_audio(audio_path)
        transcribed_text = model.transcribe(audio=audio, language='en', fp16=False, verbose=True)
        translator=Translator()
        translatedText_1=translator.translate(transcribed_text["text"], dest=language_trans)
        chat_history = []
        inputs, outputs =[],[]

        query = transcribed_text["text"]
        if query.lower() in ["exit", "quit", "q"]:
            print('Exiting')
            sys.exit()
        
        if len(inputs) > 0:
          inputs.append(query)
          last_input, last_output = inputs[-1], outputs[-1]
          query = f"{query} (based on my previous question: {last_input}, and your previous answer {last_output}"
        else:
          inputs.append(query)
        sim_docs = second_index.similarity_search(query)
        link = sim_docs[0].metadata['source']
        print("Reference: "+ link + "\n")
        result = qa_chain({'question': query, 'chat_history': chat_history})
        translatedText_2=translator.translate(result['answer'], dest=language_trans) 
        answer_text=  "Reference: "+link + "\n\n"  + translatedText_2.text
        print('Answer: ' + result['answer'] + '\n')
        chat_history.append((query, result['answer']))
        return JsonResponse({'status': 'success','transcribed_text': translatedText_1.text, "answer_text":answer_text})
    else:
        return JsonResponse({'status': 'error'})


@require_POST 
@csrf_exempt
def send_text_query(request):
    data = json.loads(request.body.decode('utf-8'))
    text_query = data.get('text_query', '')
    language_trans = data.get('language', 'en')
    print("language:", language_trans)
    translator=Translator()
    translatedText_1=translator.translate(text_query, dest='en')
    chat_history = []
    inputs, outputs =[],[]
    query = translatedText_1.text
    print("Question:", query)

    if query.lower() in ["exit", "quit", "q"]:
        print('Exiting')
        sys.exit()
    
    if len(inputs) > 0:
      inputs.append(query)
      last_input, last_output = inputs[-1], outputs[-1]
      query = f"{query} (based on my previous question: {last_input}, and your previous answer {last_output}"
    else:
      inputs.append(query)
    sim_docs = second_index.similarity_search(query)
    link = sim_docs[0].metadata['source']
    print("Reference: "+ link + "\n")
    result = qa_chain({'question': query, 'chat_history': chat_history})
    translatedText_2=translator.translate(result['answer'], dest=language_trans) 
    answer_text=  "Reference: "+link + "\n\n"  + translatedText_2.text
    print('Answer: ' + result['answer'] + '\n')
    chat_history.append((query, result['answer']))
    return JsonResponse({'status': 'success', "answer_text":answer_text})


