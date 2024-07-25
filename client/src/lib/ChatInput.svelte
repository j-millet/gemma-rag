<script>
  import { createEventDispatcher } from "svelte";

  export let width = "100%";

  const dispatch = createEventDispatcher();

  let shift_held = false;
  let textarea_message = "";

  export function clear() {
    textarea_message = "";
  }

  function sanitize(string) {
    const map = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "/": "&#x2F;",
    };
    const reg = /[&<>/]/gi;
    return string.replace(reg, (match) => map[match]);
  }

  function handleKeydown(event) {
    if (event.key === "Enter" && !shift_held) {
      dispatch("send", { message: sanitize(textarea_message.replace(/^\s\s*/, '').replace(/\s\s*$/, '')) });
    } else if (event.key === "Shift") {
      shift_held = true;
    }
  }
  function handleKeyUp(event) {
    if (event.key === "Shift") {
      shift_held = false;
    }
  }
</script>

  <div>
    <textarea
      style="width: {width}"
      bind:value={textarea_message}
      on:keydown={handleKeydown}
      on:keyup={handleKeyUp}
    />
  </div>


<style>
  textarea {
    border-radius: 1em;
    border: 2px solid #fff;
    align-self: flex-end;
    padding: 1em;
    font-size: x-large;
    margin: 1em;
    resize: none;
    height: 100%;
  }
  textarea:focus {
    outline:none;
    border: 2px solid #00d9ff;
   }
</style>
