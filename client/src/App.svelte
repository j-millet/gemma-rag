<script>
  import Chat from './lib/Chat.svelte';  
  import ChatInput from './lib/ChatInput.svelte';
  import FileManager from './lib/FileManager.svelte';

  import { onMount } from 'svelte';

  let chat=null;
  let chatInput=null

  let context_cosine = 0.7;


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

  
</script>

<main>
  <div id="chat-holder">
    <Chat bind:this={chat}/>
    
  </div> 
  <div id="controls">
    <FileManager />
    <p>Max distance = {Math.round(context_cosine*100)/100}</p>
    <div>
      <input type="range" min="0.3" max="1" step="0.01" bind:value={context_cosine} on:change={() => {chat.setContextMaxCosine(context_cosine)}} />
    </div>
    
    <ChatInput width="40vw" bind:this={chatInput} on:send={handleMessage}/>
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
    justify-content: flex-end;
    overflow: hidden;
  }
  
  #chat-holder {
    padding: 1em;
  }

  #controls {
    margin:0;
    border-top: 1px solid white;
    display: flex;
    flex-direction: row;
    justify-content: flex-end;
    align-items: center;
    width: 100%;
    height: 10%;
    justify-self: flex-end;
  }

</style>
