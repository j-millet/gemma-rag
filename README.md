# Gemma-based, local chatbot with RAG functionality

## To run
##### (confirmed working on linux (ubuntu 22.04), windows may need additional pip packages)
Prerequisites: python, npm, conda or other venv solution (not obligatory but highly encouraged)
* Run ```pip install -r requirements.txt``` inside ```/server```
* Run ```npm install && npm run build``` inside ```/client```
* Generate own secret key, change ```config-template.json``` and rename to ```config.json``` inside ```/server```
* Run ```python rag_server.py``` inside ```/server```
* (You may need to login to huggingface via [HuggingFace CLI](https://huggingface.co/docs/huggingface_hub/main/en/guides/cli) and be granted access to gemma if you haven't received it before.)

## Screenshots
![](https://i.imgur.com/7Si6PuS.png)
