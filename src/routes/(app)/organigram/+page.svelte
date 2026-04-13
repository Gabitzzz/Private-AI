<script lang="ts">
	import { SvelteFlowProvider } from '@xyflow/svelte';
	import Organigram from '$lib/components/organigram/Organigram.svelte';
	import { getContext } from 'svelte';

	const i18n = getContext('i18n');
</script>

<svelte:head>
	<title>{$i18n.t('Organigram')} | Open WebUI</title>
</svelte:head>

<div class="flex flex-col w-full h-full overflow-hidden bg-white dark:bg-[#050505]">
	<SvelteFlowProvider>
		<Organigram />
	</SvelteFlowProvider>
</div>
