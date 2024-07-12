<script>
  import Chat from './lib/Chat.svelte';  
  import ChatInput from './lib/ChatInput.svelte';
  let chat=null;
  let chatInput=null

  function handleMessage(event){
    if(!chat.isModelResponding()){
      chat.sendMessage(event.detail.message);
      chatInput.clear();
    }
  }
  function handleClick(){
    chat.stopGenerating();
  }
</script>

<main>
  <div id="chat-holder">
    <Chat bind:this={chat}/>
    <div id="controls">
      <button on:click={handleClick}>▢</button>
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
