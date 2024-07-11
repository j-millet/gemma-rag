<script>
  import Chat from './lib/Chat.svelte';  
</script>

<main>
  <div id="chat-holder">
    <Chat/>
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
</style>
