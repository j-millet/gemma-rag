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
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    
  }
  
  #chat-holder {
    border-radius: 1em;
    border: 2px solid #fff;
    padding: 1em;
  }
</style>
