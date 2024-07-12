import flask
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig
import colorama

special_tokens = ['<bos>','<eos>','<pad>','<unk>','<start_of_turn>','<end_of_turn>']
model_name = "google/gemma-2b-it"

model = None
tokenizer = None

app = flask.Flask(__name__)

@app.route("/")
def base():
    return flask.send_from_directory("../client/dist", "index.html")

@app.route("/<path:path>")
def home(path):
    return flask.send_from_directory("../client/dist", path)

@app.route("/chat-completion", methods=["POST"])
def chat_completion():
    data = flask.request.json
    chat_history = data["chat_history"]
    max_new_tokens = 100
    if "max_new_tokens" in data: max_new_tokens = data["max_new_tokens"]

    incomplete_message=False
    if "incomplete_message" in data: incomplete_message = data["incomplete_message"]

    input_text = ""
    if not incomplete_message:
        input_text = tokenizer.apply_chat_template(chat_history,tokenize=False,add_generation_prompt=True)
    else:
        input_text = tokenizer.apply_chat_template(chat_history[:-1],tokenize=False,add_generation_prompt=False)
        input_text += f"<start_of_turn>model\n{chat_history[-1]['content']}"
    
    input_ids = tokenizer(input_text, add_special_tokens=False,return_tensors="pt").to("cuda")

    outputs = model.generate(**input_ids,max_new_tokens=max_new_tokens)
    text = tokenizer.decode(outputs[0])

    model_message = text.replace(input_text,"")
    incomplete_message = not "<eos>" in model_message
    for special_token in special_tokens:
        model_message = model_message.replace(special_token,"")

    return flask.jsonify({"response": model_message,"incomplete_message":incomplete_message})

if __name__ == "__main__":
    print(colorama.Fore.YELLOW + f"Loading {model_name}...")
    print(colorama.Style.RESET_ALL,end="")
    try:
        torch.cuda.empty_cache()
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="cuda",
            quantization_config=quantization_config
        )
        print(colorama.Fore.GREEN + "Model loaded. Starting server...")
        print(colorama.Style.RESET_ALL,end="")
    except Exception as e:
        print(colorama.Fore.RED + f"Jesus fucking christ what is happening: {e}")
        print(colorama.Style.RESET_ALL,end="")
        torch.cuda.empty_cache()
    
    app.run(host="0.0.0.0",port=2137)
    print("\r",end="")
    print(colorama.Fore.GREEN + "Shutting down...")
    print(colorama.Style.RESET_ALL,end="")
    torch.cuda.empty_cache()
    