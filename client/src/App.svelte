<script>
  import Chat from './lib/Chat.svelte';  
  import ChatInput from './lib/ChatInput.svelte';
	import { onMount } from 'svelte';

  let chat=null;
  let chatInput=null

  let context_cosine = 0.7;

  let uploaded_files = [];

  onMount(()=>{
    startSession();
  })

  window.onbeforeunload = function() {
    fetch('./close-session', {method: 'POST'})
  }
  function startSession(){
    fetch('./open-session', {method: 'POST'})
  }

  function handleMessage(event){
    if(!chat.isModelResponding()){
      chat.sendMessage(event.detail.message);
      chatInput.clear();
    }
  }
  function handleClick(){
    chat.stopGenerating();
  }
  let file_input = null;

    async function uploadFile() {
        const formData = new FormData();
        formData.append('file', file_input.files[0]);
        console.log(formData);
        const filepath = await fetch('./upload', {
            method: 'POST',
            body: formData
        }).then((res) => res.json()).then((res) => res.filepath);

        uploaded_files = [...uploaded_files, filepath.split('/').pop()];
        
    }
</script>

<main>
  <div id="chat-holder">
    <Chat bind:this={chat}/>
    <div id="controls">
      <p>Max distance = {Math.round(context_cosine*100)/100}</p>
      <div>
        <input type="range" min="0.3" max="1" step="0.01" bind:value={context_cosine} on:change={() => {chat.setContextMaxCosine(context_cosine)}} />
      </div>
      <div>
        <p style="padding:0.5em">{uploaded_files}</p>
      </div>
      <input type="file" bind:this={file_input} />
      <button on:click={uploadFile}>Upload File</button>
      <ChatInput width="40vw" bind:this={chatInput} on:send={handleMessage}/>
    </div>
  </div> 
</main>

<style>
  main {
    background-color: rgb(29, 29, 29);
    width: 100vw;
    height: 100vh;
    padding: 0;
    margin: 0;
    position: absolute;
    margin-left: -50vw;
    margin-top: -50vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  #chat-holder {
    padding: 1em;
  }

  #controls {
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    align-items: center;
    width: 100%;
  }

  button {
    background-color: rbga(0, 0, 0, 0);
    color: white;
    border: none;
    border-radius: 1em;
    margin-right: 1em;
    font-size: x-large;
  }

</style>
