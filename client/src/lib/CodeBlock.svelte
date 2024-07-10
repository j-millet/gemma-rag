<script>
    export let lang
    export let text
  </script>
  {#if text}
  <div id="main_block">
    {#if lang}
    <div id="lang_block">
      <p>Language: {lang}</p>
    </div>
    {/if}
    <div id="code_block">
      <code>{text}</code>
    </div>
  </div>
  {/if}

  <style>
    #code_block{
      padding: 0.1em;
    }
    #main_block{
      background-color: #1c1c1cc7;
      border: 1px solid white;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      justify-content: center;
      padding: 0;
      margin: 0.5em;
    }
    #lang_block{
      border-bottom: 2px solid white;
      padding: 0;
      margin:0;
      width: 100%;
    }
    p{
        color: white;
        font-size: 1em;
        margin: 0.2em;
        text-transform: capitalize;
    }
    code{
        color: white;
        font-size: 0.8em;
        margin:0.2em;
        font-family: 'Inter', monospace;
    }
  </style>