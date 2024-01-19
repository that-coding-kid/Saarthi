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

#import argostranslate.package
#import argostranslate.translate

model = whisper.load_model("small")

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
from google.colab import drive
file1 = open("/content/drive/MyDrive/pre-final.txt", "r+")
new=file1.readlines()

file2 = open("/content/drive/MyDrive/.txt", "r+",encoding="utf-8")
new2 = file2.readlines()

with open('/content/drive/MyDrive/metas4.pickle','rb') as handle:
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
  doc = Document(page_content = new[j], metadata = i)
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
        language=request.POST.get('language')
        from_code = request.POST.get('language')
        # Save the audio file in the media directory
        audio_path = os.path.join('media', audio_file.name)
        with open(audio_path, 'wb') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        # Use whisper to transcribe the saved audio file
        audio=whisper.load_audio(audio_path)
        transcribed_text = whisper.transcribe(audio=audio, model=model)
        to_code="en"
        #installed_languages = argostranslate.translate.get_installed_languages()
        #from_lang = list(filter(lambda x: x.code == from_code,installed_languages))[0]
        #to_lang = list(filter(lambda x: x.code == to_code,installed_languages))[0]
        #translation = from_lang.get_translation(to_lang)
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
        answer_text=result['answer']
        print('Answer: ' + result['answer'] + '\n')
        chat_history.append((query, result['answer']))

        return JsonResponse({'status': 'success','transcribed_text': transcribed_text, "answer_text":answer_text})
    else:
        return JsonResponse({'status': 'error'})


@require_POST 
@csrf_exempt
def send_text_query(request):
    data = request.POST 
    text_query = data.get('text_query', '')
    print(text_query)
    chat_history = []
    inputs, outputs =[],[]
    query = text_query

    if query.lower() in ["exit", "quit", "q"]:
            print('Exiting')
            sys.exit()
        
    if len(inputs) > 0:
          inputs.append(query)
          last_input, last_output = inputs[-1], outputs[-1]
          query = f"{query} (based on my previous question: {last_input}, and your previous answer {last_output}"
    else:
          inputs.append(query)

    result = qa_chain({'question': query, 'chat_history': chat_history})
    answer_text=result['answer']
    print('Answer: ' + result['answer'] + '\n')
    chat_history.append((query, result['answer']))

    return JsonResponse({'status': 'success', "answer_text":answer_text})


