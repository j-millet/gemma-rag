<script>
    import SvelteMarkdown from "svelte-markdown";
    import CodeBlock from "../lib/CodeBlock.svelte";
    let chat_history = []
    let textarea_message = ""
    let incomplete_message = false
    let model_responding = false
    function fetchModelResponse(chat_history,incomplete_message,max_new_tokens=5) {
        let message = "";
        return fetch("./chat-completion",
        {
          method:"post",
          headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
          body: JSON.stringify(
            {
              "chat_history":chat_history,
              "max_new_tokens":max_new_tokens,
              "incomplete_message":incomplete_message
            })
        })
        .then(res => res.text())
        .then(text => JSON.parse(text))
    }
    async function sendMessage() {
        if(model_responding){
            return;
        }
        if (textarea_message == "") {
            return;
        }
        model_responding = true;
        chat_history = [...chat_history,{"role":"user","content":textarea_message}]
        textarea_message = "";

        do{
            await fetchModelResponse(chat_history,incomplete_message).then(res => {
                console.log(res)
                incomplete_message = res.incomplete_message
                let last_message = chat_history[chat_history.length-1]
                if (incomplete_message) {
                    console.log(last_message)
                    if (last_message.role == "user"){
                        chat_history = [...chat_history,{"role":"assistant","content":res.response}]
                    }
                    else{
                        last_message.content += res.response
                        chat_history.pop()
                        chat_history = [...chat_history,last_message]
                    }
                }
                else if(chat_history[chat_history.length-1].role == "user"){
                    chat_history = [...chat_history,{"role":"assistant","content":res.response}]
                }
                else{
                    last_message.content += res.response
                    chat_history.pop()
                    chat_history = [...chat_history,last_message]
                }
            })

        }while(incomplete_message)
        model_responding = false;
    }
    function handleKeydown(event) {
        if (event.key === "Enter") {
            sendMessage()
        }
    }
</script>

<main>
    <div class="chat-box">
        {#if chat_history}
            {#each chat_history.toReversed() as message}
            <div class="message-{message.role}">
                <SvelteMarkdown source={message.content} renderers={{code:CodeBlock}}/>
            </div>
            {/each}
        {/if}
        {#if chat_history.length == 0}
        <div id="empty-chat-box">
            <p id="empty-chat-msg">No messages yet, start chatting!</p>
        </div>
        {/if}
    </div>
    
    
    <textarea bind:value={textarea_message} on:keydown={handleKeydown}/>

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
        width: 80vw;
        height: 70vh;
    }
    .message-user {
        background-color: hsla(0, 0%, 0%, 0);
        border: 2px solid #00d9ff;
        border-radius: 1em;
        align-self: flex-end;
        border-radius: 1em;
        padding: 1em;
        margin: 0.5em;
        max-width: 30%;
        text-align: right;
    }
    .message-assistant{
        background-color: hsla(0, 0%, 0%, 0);
        border: 2px solid #9900ff;
        border-radius: 1em;
        padding: 1em;
        margin: 0.5em;
        max-width: 50%;
        align-self: flex-start;
        text-align: left;
    }
    textarea {
        width: 50%;
        height: 3%;
        border-radius: 1em;
        align-self: flex-end;
        padding: 1em;
        font-size: x-large;
        margin-top: 1em;
        resize: none;
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