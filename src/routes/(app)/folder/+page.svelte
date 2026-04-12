<script lang="ts">
	import { SvelteFlowProvider } from '@xyflow/svelte';
	import FolderWhiteboard from '$lib/components/folder/FolderWhiteboard.svelte';
	import { getContext } from 'svelte';

	const i18n = getContext('i18n');
</script>

<svelte:head>
	<title>{$i18n.t('Folder')} | Open WebUI</title>
</svelte:head>

<div class="flex flex-col w-full h-full overflow-hidden">
	<SvelteFlowProvider>
		<FolderWhiteboard />
	</SvelteFlowProvider>
</div>
