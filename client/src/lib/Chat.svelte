<script>
  import SvelteMarkdown from "svelte-markdown";
  import CodeBlock from "../lib/CodeBlock.svelte";
  let chat_history = [];
  let incomplete_message = false;
  let model_responding = false;

  function fetchModelResponse(
    chat_history,
    incomplete_message,
    max_new_tokens = 10
  ) {
    return fetch("./chat-completion", {
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        chat_history: chat_history,
        max_new_tokens: max_new_tokens,
        incomplete_message: incomplete_message,
      }),
    })
      .then((res) => res.text())
      .then((text) => JSON.parse(text));
  }

  export async function sendMessage(message) {
    if (model_responding) {
      return;
    }
    if (message == "") {
      return;
    }
    let context = await fetch("./context-retrieval", {
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: message }),
    }).then((res) => res.json()).then((res) => res.context);

    model_responding = true;
    chat_history = [
      ...chat_history,
      { role: "user", content: message },
    ]; 

    let working_chat_history = structuredClone(chat_history);
    if (context){
      working_chat_history[working_chat_history.length - 1].content = "With provided context: " + context + "\nAnswer the question:\n" + working_chat_history[working_chat_history.length - 1].content;
    }
    console.log(working_chat_history)
    console.log(chat_history)
    do {
      await fetchModelResponse(working_chat_history, incomplete_message).then((res) => {
        incomplete_message = res.incomplete_message;
        let last_message = working_chat_history[working_chat_history.length - 1];
        if (incomplete_message) {
          if (last_message.role == "user") {
            chat_history = [
              ...chat_history,
              { role: "assistant", content: (res.response) },
            ];
            working_chat_history = [...working_chat_history, { role: "assistant", content: (res.response) }];
          } else {
            last_message.content += (res.response);
            chat_history.pop();
            chat_history = [...chat_history, last_message];
            working_chat_history.pop();
            working_chat_history = [...working_chat_history, last_message];
          }
        } else if (chat_history[chat_history.length - 1].role == "user") {
          chat_history = [
            ...chat_history,
            { role: "assistant", content: (res.response)},
          ];
        } else {
          last_message.content += (res.response);
          chat_history.pop();
          chat_history = [...chat_history, last_message];
        }
      });
    } while (incomplete_message && model_responding);
    model_responding = false;
  }

  export function isModelResponding() {
    return model_responding;
  }
  export function stopGenerating() {
    incomplete_message = false;
    model_responding = false;
    console.log(chat_history)
  }
  
</script>

<main>
  <div class="chat-box">
    {#if chat_history}
      {#each chat_history.toReversed() as message}
        <div class="message-{message.role}">
          <SvelteMarkdown
            source={message.content}
            renderers={{ code: CodeBlock }}
          />
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
