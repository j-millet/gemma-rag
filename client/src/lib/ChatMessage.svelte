<script>
    import SvelteMarkdown from "svelte-markdown";
    import CodeBlock from "../lib/CodeBlock.svelte";

    export let content = "";

</script>

<div>
    <SvelteMarkdown
    source={content}
    renderers={{ code: CodeBlock }}
  />
</div>
<style>
    div{
        min-width: 1em;
    }
</style>
