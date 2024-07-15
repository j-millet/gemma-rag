<script>
  import { createEventDispatcher } from "svelte";
  import ChatMessage from "./ChatMessage.svelte";

  export let content = "";
  export let finished = false;
  export let context = [];

  let viewContext = false;

  const dispatch = createEventDispatcher();

  function fireStop() {
    dispatch("stopGeneration");
  }

  function toggleContext() {
    viewContext = !viewContext;
  }
</script>

<ChatMessage {content} />
<div id="message-controls">
  {#if context.length > 0}
    <button on:click={toggleContext}>View context</button>
  {/if}
  {#if !finished}
    <button id="stopButton" on:click={fireStop}>▢</button>
  {/if}
</div>
{#if viewContext}
  <div id="context-box">
    {#each context as item}
      <h3>{item.source}</h3>
      <p>{item.content}</p>
    {/each}
  </div>
{/if}

<style>
  #message-controls {
    display: flex;
    justify-content: flex-end;
    margin-top: 0.5em;
    height: 2em;
  }

  #stopButton {
    background-color: transparent;
    color: white;
    border: none;
    border-radius: 50%;
    width: 1.5em;
    height: 1.5em;
    font-size: 1em;
    cursor: pointer;
  }
  #context-box {
    overflow: scroll;
    max-height: 15em;
    margin-top: 0.5em;
    margin-bottom: 0.5em;
  }
</style>
