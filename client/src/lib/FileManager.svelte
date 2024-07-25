<script>
    import {clickOutside} from './clickOutside.js';
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();

    let uploaded_files = [];

    let file_input = null;

    let selected_file = null;

    let showList = false;

    function toggleShowList(){
        showList = !showList;
    }
    async function uploadFile() {
      if(!file_input.files[0]){
          return;
      }
      const formData = new FormData();
      formData.append('file', file_input.files[0]);
      const filepath = await fetch('./upload', {
          method: 'POST',
          body: formData
      }).then((res) => res.json()).then((res) => res.filepath);

      if(uploaded_files.length === 0){
            dispatch("contextAvailable");
      }
      uploaded_files = [...uploaded_files, filepath];
      selected_file = null;
      file_input.value = null;
    }
    async function deleteFile(file){
        let res = await fetch('./delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename:file
            })
        }).then((res)=>res.text()).then((res)=>JSON.parse(res));
        if(res.error){
            console.log(res.error);
            return;
        }
        uploaded_files = uploaded_files.filter((f)=>f!==file);    
        if (uploaded_files.length === 0){
            dispatch("contextUnavailable");
        }
    }
</script>

{#if showList}
<div id="file-manager-list">
    <h2>Uploaded Files</h2>
    <div id="file-list">
        <ul>
            {#each uploaded_files as file}
                <li>
                    <div class="file-container">
                        <p>{file}</p>
                        <button class="delete-button" on:click={()=>{deleteFile(file)}}>🗑</button>
                    </div>
                </li>
            {/each}
        </ul>
    </div>
</div>
{/if}
<div id="file-manager-box">
    <button title="View uploaded files" on:click={toggleShowList}>{(showList)?"▼":"▲"}</button>
    <input type="file" bind:this={file_input} on:change={()=>{selected_file = file_input.files[0]}} />
    <button title="Choose file" on:click={() => {file_input.click()}}>+</button>
    {#if selected_file}
        <button title="Upload" on:click={uploadFile}>↥</button>
        <p>{"Upload: "+selected_file.name}</p>
        <button title="Clear" on:click={()=>{selected_file = null; file_input.value = null}}>✘</button>
    {/if}
</div>

<style>
    #file-manager-box {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        flex-grow: 1;
        margin:1em;
        width: 15%;
    }
    #file-manager-list{
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;
        position: absolute;
        bottom:10%;
        left: 0.1em;
        background-color: #161616;
        border:2px solid white;
        border-radius: 1em;
        padding: 1em;
    }
    #file-list{
        overflow: scroll;
        max-height: 10em;
        min-height: 1em;
        width:100%;
        text-align: left;
    }
    .file-container{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        width: 100%;
    }
    
    .delete-button{
        background-color: rgba(0,0,0,0);
    }
    input{
        display: none;
    }
    button{
        margin:0.5em;
        padding: 1.5%;
        font-size: large;
    }
</style>