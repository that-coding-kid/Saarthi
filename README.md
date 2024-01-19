# Space Hackathon'2023 Repository

This repository contains our works for the Space Hackathon '2023 held at the Indian International Space Festival 2023.

## Overview

Explore the projects developed during the hackathon and find the corresponding code in their respective directories.

## Prerequisites

Our chatbot can be run remotely on Google Colab without installing anything on your system. 
- [Python](https://www.python.org/) (version X.X.X)

## Getting Started

1. Navigate to Google Colab: [colab.research.google.com](https://colab.research.google.com/)
2. Go to File -> Open Notebook -> from GitHub -> Paste this URL: `https://github.com/saurbh264/IISF-Space-Hackathon.git`

## Updating the database

- We are fetching the data from websites. Since websites can change, we have created an architecture which allows you to fetch, pre-process and embed data and store it in the FAISS Index Database. Run the following "//Code Here"

## Flow 
![WhatsApp Image 2024-01-17 at 21 24 49_082efb10](https://github.com/saurbh264/IISF-Space-Hackathon/assets/126571954/1d10ba60-a7b9-4edd-95be-03fdc03c3988)

##Accuracies

##Whisper
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

## More examples

## APIs Used

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


If you want to contribute, open an issue or submit a pull request.
