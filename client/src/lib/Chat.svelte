<script>

  import ChatMessage from "./ChatMessage.svelte";
  import ModelMessage from "./ModelMessage.svelte";

  let chat_history = [];
  let model_responding = false;

  let context_top_k = 5;
  let context_max_cosine = 0.7;

  export function setContextTopK(k) {
    if (k < 1) {
      k = 1;
    }
    context_top_k = k;
  }
  export function setContextMaxCosine(cosine) {
    cosine = Math.min(1, Math.max(0, cosine));
    context_max_cosine = cosine;
  }

  function extractCoreChatHistory(extended_chat_history) {
    let core_chat_history = [];
    for (let i = 0; i < extended_chat_history.length; i++) {
      core_chat_history.push({role:extended_chat_history[i].role,content:extended_chat_history[i].content});
    }
    return core_chat_history;
  }

  function fetchModelResponse(
    input_chat_history,
    incomplete_message,
    max_new_tokens = 10,
    temperature = 0.1
  ) {
    console.log(input_chat_history);
    return fetch("./chat-completion", {
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        chat_history: input_chat_history,
        max_new_tokens: max_new_tokens,
        incomplete_message: incomplete_message,
        temperature: temperature,
      }),
    })
      .then((res) => res.text())
      .then((text) => JSON.parse(text));
  }

  async function fetchContext(query) {
    let context = await fetch("./context-retrieval", {
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: query, top_k: context_top_k, max_cosine: context_max_cosine }),
    })
      .then((res) => res.json())
      .then((res) => res.context);
    return context;
  }

  export async function sendMessage(message,use_context=true) {
    if (model_responding) {
      return;
    }
    if (message == "") {
      return;
    }
    chat_history = [...chat_history, { role: "user", content: message, meta:{} }];
    model_responding = true;

    let context = [];
    let text_context = "";
    if (use_context){
      context = await fetchContext(message);
      
      for (let i = 0; i < context.length; i++) {
        text_context += context[i].content + "\n";
      }
    }

    chat_history = [...chat_history,{ role: "assistant", content: "", meta:{finishedMessage:false,context:context}}];
    let working_chat_history = structuredClone(chat_history);

    if(use_context){
    working_chat_history[working_chat_history.length - 2].content =
      "Using only the provided context (if context is empty DO NOT use your own knowledge): " +
      text_context +
      "\nRespond to the prompt (please cite sources):\n" +
      message;
    }
    let last_message = chat_history[chat_history.length - 1];
    let last_message_working = working_chat_history[working_chat_history.length - 1];

    while(model_responding){
      let model_response = await fetchModelResponse(
        extractCoreChatHistory(working_chat_history),
        !last_message.meta.finishedMessage
      )

      last_message.content += model_response.response;
      last_message.meta.finishedMessage = !model_response.incomplete_message;
      

      chat_history.pop();
      chat_history = [...chat_history,last_message];

      last_message_working.content += model_response.response;
      last_message_working.meta.finishedMessage = !model_response.incomplete_message;

      working_chat_history.pop();
      working_chat_history = [...working_chat_history,last_message_working];
      
      
      if (!model_response.incomplete_message) {
        model_responding = false;
      }
    }

    last_message.meta.finishedMessage = true;
      chat_history.pop();
      chat_history = [...chat_history,last_message];
  }

  export function isModelResponding() {
    return model_responding;
  }
  export function stopGenerating() {
    model_responding = false;
  }
</script>

<main>
  <div class="chat-box">
    {#if chat_history}
      {#each chat_history.toReversed() as message}
        <div class="message-{message.role}">
          {#if message.role=="assistant"}
            <ModelMessage content={message.content} context={message.meta.context} finished={message.meta.finishedMessage} on:stopGeneration={stopGenerating}/>
          {:else}
            <ChatMessage content={message.content} />
          {/if}
        </div>
      {/each}
    {/if}
    {#if chat_history.length == 0}
      <div id="empty-chat-box">
        <p id="empty-chat-msg">No messages yet, start chatting!</p>
      </div>
    {/if}
  </div>
</main>

<style>
  main {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: center;
  }
  .chat-box {
    display: flex;
    flex-direction: column-reverse;
    justify-content: flex-start;
    align-items: flex-start;
    padding: 1em;
    overflow: scroll;
    width: 90vw;
    height: 75vh;
  }
  .message-user {
    border: 2px solid #00d9ff;
    border-radius: 1em;
    align-self: flex-end;
    border-radius: 1em;
    padding: 1em;
    margin: 0.5em;
    max-width: 30%;
    text-align: left;
  }
  .message-assistant {
    border: 2px solid #9900ff;
    border-radius: 1em;
    padding: 1em;
    margin: 0.5em;
    max-width: 50%;
    align-self: flex-start;
    text-align: left;
  }

  #empty-chat-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }
  #empty-chat-msg {
    font-size: 1.5em;
  }
</style>
