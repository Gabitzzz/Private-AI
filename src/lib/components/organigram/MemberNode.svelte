<script lang="ts">
	import { Handle, Position } from '@xyflow/svelte';
	import { getContext } from 'svelte';

	const i18n = getContext('i18n');

	export let data;
	// data items: name, role, image, color
</script>

<div class="flex flex-col items-center group">
	{#if data.isRoot}
		<div class="bg-gray-100/80 dark:bg-gray-800/80 backdrop-blur-md px-6 py-2 rounded-full border border-gray-200 dark:border-gray-700 shadow-sm transition-all group-hover:shadow-md group-hover:-translate-y-0.5">
			<span class="text-sm font-semibold text-gray-900 dark:text-gray-100">{data.name}</span>
		</div>
	{:else}
		<div class="relative">
			<div 
				class="size-16 rounded-2xl bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 shadow-xl flex items-center justify-center p-3 transition-all duration-300 group-hover:scale-110 group-hover:rotate-3"
				style="border-bottom: 3px solid {data.color || '#3b82f6'}"
			>
				{#if data.image}
					<img src={data.image} alt={data.name} class="size-full object-contain transition-transform group-hover:scale-110" />
				{:else}
					<div class="size-full rounded-lg flex items-center justify-center text-xl font-bold" style="background: {data.color}20; color: {data.color}">
						{data.name.charAt(0)}
					</div>
				{/if}
			</div>
			
			<div class="absolute -bottom-10 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-2 group-hover:translate-y-0 whitespace-nowrap pointer-events-none">
				<div class="bg-gray-900 dark:bg-white text-white dark:text-gray-900 px-3 py-1.5 rounded-lg text-[10px] font-bold shadow-2xl">
					<div class="uppercase tracking-widest">{data.role}</div>
					<div class="text-[12px] opacity-80 mt-0.5">{data.name}</div>
				</div>
			</div>
		</div>
	{/if}

	<Handle type="target" position={Position.Top} class="!w-0 !h-0 !border-0 !bg-transparent" />
	<Handle type="bottom" position={Position.Bottom} class="!w-0 !h-0 !border-0 !bg-transparent" />
</div>

<style>
	:global(.svelte-flow__handle) {
		visibility: hidden;
	}
</style>
