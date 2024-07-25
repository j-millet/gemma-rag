# Gemma-based, local chatbot with RAG functionality

## To run
Prerequisites: python, npm, conda or other venv solution (not obligatory but highly encouraged)
* Clone repo
* Run ```pip install -r requirements.txt``` inside ```/server```
* Run ```npm install && npm run build``` inside ```/client```
* Generate own secret key, change ```config-template.json``` and rename to ```config.json``` inside ```/server```
* Run ```python rag_server.py``` inside ```/server```
* (You may need to login to huggingface via [HuggingFace CLI](https://huggingface.co/docs/huggingface_hub/main/en/guides/cli) and be granted access to gemma if you haven't received it before.)

## Screenshots
![](https://cdn.discordapp.com/attachments/949452484231954452/1262731079778045982/image.png?ex=6697a975&is=669657f5&hm=5594b11b9c3a1c392586292a8ea195d14ba5f6b78c9cb838a48ca1372a763c6f&)
