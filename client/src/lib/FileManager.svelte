<script>
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
      uploaded_files = [...uploaded_files, filepath];
      selected_file = null;
      file_input.value = null;
  }
</script>

{#if showList}
<div id="file-manager-list">
    <h2>Uploaded Files</h2>
    <div id="file-list">
        <ul>
            {#each uploaded_files as file}
                <li>{file}</li>
            {/each}
        </ul>
    </div>
</div>
{/if}
<div id="file-manager-box">
    <button on:click={toggleShowList}>{(showList)?"▼":"▲"}</button>
    <input type="file" bind:this={file_input} on:change={()=>{selected_file = file_input.files[0]}} />
    <button on:click={() => {file_input.click()}}>+</button>
    <button on:click={uploadFile}>↥</button>
    <p>{(selected_file)? "Upload: "+selected_file.name:""}</p>
</div>

<style>
    #file-manager-box {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        flex-grow: 1;
        margin:1em;
    }
    input{
        display: none;
    }
    button{
        margin:0.5em
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
</style>