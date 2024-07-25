<script>
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    let showPanel = false;

    let temperature = 0.1;

    let contextChunksCount = 5;

    let use_context = false;

    let context_prompt_template = "Using only the provided context (if context is empty DO NOT use your own knowledge):\n<context>\nRespond to the prompt (please cite sources, if available in context):\n<prompt>"
    
    $: context_prompt_template, dispatch("contextPromptChanged");

    $: temperature, dispatch("temperatureChanged");

    $: contextChunksCount, dispatch("contextChunksCountChanged");

    $: use_context, dispatch("useContextChanged");
    
    function toggleShowPanel(){
        showPanel = !showPanel;
    }

    export function offShowPanel(){
        showPanel = false;
    }

    export function getContextPromptTemplate(){
        return context_prompt_template;
    }

    export function getTemperature(){
        return temperature;
    }

    export function getContextChunksCount(){
        return contextChunksCount;
    }

    export function useContext(){
        return use_context;
    }

    export function setUseContext(value){
        use_context = value;
    }

</script>

{#if showPanel}
<div id="settings-panel">
    <div id="settings-panel-top">
        <div>
            <h2>Settings</h2>
        </div>
        <button title="Close" on:click={offShowPanel}>✘</button>
    </div>
    <div id="settings-panel-content">
        <p>Temperature</p>
        <div class="slider-input-div">
            <input type="range" min="0" max="2" step="0.1" bind:value={temperature}>
            <span>{temperature}</span>
        </div>
        <p>Max context chunks used</p>
        <div class="slider-input-div">
            <input type="range" min="1" max="10" step="1" bind:value={contextChunksCount}>
            <span>{contextChunksCount} chunk{(contextChunksCount > 1)? "s":""} ≈ {1000*contextChunksCount} words.</span>
        </div>
        <span>Use context?</span>
        <input type="checkbox" bind:checked={use_context}>
        <p>Context prompt template</p>
        <textarea id="context-prompt-ta" bind:value={context_prompt_template}></textarea>
    </div>
</div>
{/if}
<button title="Settings" on:click={toggleShowPanel}>⚙</button>

<style>
    .slider-input-div{
        display: flex;
        flex-direction: row;
        align-items: center;
        width: 100%;
    }
    .slider-input-div input{
        width: 60%;
        margin-left: 1em;
    }
    #settings-panel{
        position: absolute;
        width:40%;
        height: 70%;
        top:10%;
        left: 30%;
        border-radius: 5%;
        border: 2px solid white;
        background-color: rgb(20,20,20);
    }

    #settings-panel h2{
        text-align: center;
    }

    #settings-panel-top{
        display: flex;
        flex-direction: row;
        justify-content: flex-end;
        padding-left: 1%;
        padding-right: 1em;
    }

    #settings-panel-top div{
        justify-self: flex-start;
        display: flex;
        padding-left: 1em;
        flex-grow: 2;
    }
    #settings-panel-content{
        padding: 1em;
        overflow: scroll;
        max-height: 80%;
        height: 80%;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        
    }
    #context-prompt-ta{
        width: 90%;
        height: 30%;
        resize: vertical;
    }

    button{
        font-size: x-large;
        margin:0.5em;
    }
</style>