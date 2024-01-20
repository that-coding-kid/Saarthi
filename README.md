# SIF Space Hackathon'2023 Repository

This repository contains our works for the Space Hackathon '2023 held at the Indian International Space Festival 2023. This made it to the top 50 finale teams. The problem statement includes building a voice powered chatbot for BHUVAN portal.

## Overview
The problem statement expects us to build a chatbot that is capable of understanding and processing multilingual voice‐based search queries. It should accurately interpret the user’s query and deliver context-aware responses. We are expected to enhance the user experience through a well-built voice-enabledinterface. SAARTHI is our voice powered chatbot.

## Prerequisites

Our chatbot can be run remotely on Google Colab without installing anything on your system.

## Getting Started

1. Navigate to Google Colab: [colab.research.google.com](https://colab.research.google.com/)
2. Go to File -> Open Notebook -> from GitHub -> Paste this URL: `https://github.com/that-coding-kid/Saarthi.git`
3. The dataset consists of a set of URLs scrapped, preprocessed and saved as a text file.

## Flow 
![flowhart](https://github.com/that-coding-kid/Saarthi/assets/120119962/e39cff30-e044-4313-9c64-961f49072c5d)
**Brief about our Approach:**

1.**Web Scrapping and Data Preprocessing**: Leveraging Langchain, we efficiently scraped data from specified URLs. To augment the bot's intent awareness, we manually enriched the dataset with additional descriptors. Further enhancing the conversational depth, we refined the data ensuring a more descriptive and contextually nuanced interaction.

2.**Creating Embeddings**: Utilizing the Hugging Face platform, specifically the 'instructor-XL' embeddings, we generated embeddings for the dataset. These embeddings form the basis for similarity searches and contribute to the overall functionality of the system.

3.**Retrieval Augmented Generation using FAISS and Mixtral-8x7B-Instruct-v0.1**: Implemented retrieval augmented generation using FAISS as a knowledge base and semantic index similarity. The system, upon receiving a query, retrieves the context of k-nearest neighbors, enhancing precision in generated responses for a more contextually accurate interaction.

4.**Voice to Text using Whisper small model**: Our system seamlessly integrates the open-source ASR Model- ‘Whisper Voice API’ (Whisper-small model) for live voice-to-text transcription, ensuring accurate and efficient conversion.

5.**Dynamic and context aware responses using Mixtral-8x7B-Instruct-v0.1** : Subsequently, the query, along with the context retrieved from Faiss, is input into 'Mixtral-8x7B-Instruct-v0.1', an open-source Large Language Model. Accessing its API from Hugging Face, this model demonstrates superior accuracy compared to Llama 13B and is on par with GPT-3.5 in terms of performance. The response is then generated, leveraging the capabilities of Mixtral-8x7B-Instruct-v0.1, incorporating the contextual information from the query and Faiss-retrieved context.

6.**Voice based input and output (Bilingual)**: We provide users with the option to choose between Hindi and English for their preferred language. The generated response is presented in a voice-based format, utilizing translators and text-to-voice models to enhance the overall user experience.


## Accuracies

## Whisper
|            	| large 	| medium 	| small 	| base 	| tiny 	| WERR: S → M 	|
|:----------:	|:-----:	|:------:	|:-----:	|:----:	|:----:	|:-----------:	|
| English    	| 0.15  	| 0.17   	| 0.17  	| 0.2  	| 0.2  	| 0           	|
| Italian    	| 0.16  	| 0.17   	| 0.22  	| 0.33 	| 0.5  	| 0.24        	|
| German     	| 0.18  	| 0.18   	| 0.21  	| 0.27 	| 0.4  	| 0.14        	|
| Spanish    	| 0.19  	| 0.19   	| 0.2   	| 0.28 	| 0.4  	| 0.07        	|
| French     	| 0.26  	| 0.26   	| 0.29  	| 0.37 	| 0.5  	| 0.09        	|
| Portuguese 	| 0.25  	| 0.28   	| 0.28  	| 0.39 	| 0.5  	| 0.02        	|
| Japanese*  	| 0.29  	| 0.3    	| 0.34  	| 0.44 	|      	| 0.11        	|
| Danish     	| 0.3   	| 0.3    	| 0.41  	| 0.64 	| 0.8  	| 0.25        	|
| Swedish    	| 0.29  	| 0.31   	| 0.38  	| 0.51 	| 0.6  	| 0.19        	|
| Indonesian 	| 0.31  	| 0.31   	| 0.38  	| 0.52 	|      	| 0.17        	|
| Greek      	| 0.29  	| 0.31   	| 0.44  	| 0.62 	| 0.8  	| 0.29        	|
| Chinese*   	| 0.33  	| 0.33   	| 0.35  	| 0.44 	|      	| 0.06        	|
| Thai*      	| 0.34  	| 0.34   	| 0.52  	| 0.59 	| 0.7  	| 0.34        	|
| Tagalog    	| 0.36  	| 0.37   	| 0.48  	| 0.7  	| 0.9  	| 0.24        	|
| Korean     	| 0.4   	| 0.4    	| 0.44  	| 0.51 	|      	| 0.09        	|
| Norwegian  	| 0.42  	| 0.42   	| 0.46  	| 0.75 	| 0.9  	| 0.09        	|
| Finnish    	| 0.41  	| 0.43   	| 0.53  	| 0.7  	| 0.9  	| 0.19        	|
| Arabic     	| 0.52  	| 0.53   	| 0.61  	| 0.75 	| 0.9  	| 0.14        	|
| Hindi      	| 0.6   	| 0.67   	| 0.104 	| 0.11 	|      	| 0.35        	|

![image](https://github.com/saurbh264/IISF-Space-Hackathon/assets/126571954/795d14f5-df69-4e4b-9c65-2365b25d8cf6)

## Technology and Tech Stack used:

We have used multiple open-source APIs to achieve our task. The domain-wise APIs and their GitHub links are below.

1. Audio Transcription: [OpenAI-Whisper](https://openai.com/research/whisper)
2. Text Translation: [Argotranslate](https://github.com/argosopentech/argos-translate)
3. Voice-Recoding: JavaScript API
4. Embeddings Creation: [hkunlp/instructor-xl](https://huggingface.co/hkunlp/instructor-xl)
5. Database Used: [FAISS-Index](https://github.com/facebookresearch/faiss)
6. Web Scraping: [Langchain.webloader](https://js.langchain.com/docs/integrations/document_loaders/web_loaders/)
7. Pre-Processing: [RegEx](https://github.com/python/cpython/tree/3.12/Lib/re/)
8. QA Chain: [Langchain](https://www.langchain.com/)
9. LLM: [Mixtral - 8x7B](https://www.langchain.com/)
10. Web Framework: [Django](https://github.com/django/django)
    


# If you want to contribute, open an issue or submit a pull request.
