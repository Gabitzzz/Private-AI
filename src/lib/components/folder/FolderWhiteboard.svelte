<script lang="ts">
	import { onMount, getContext, tick } from 'svelte';
	import { writable } from 'svelte/store';
	import { toast } from 'svelte-sonner';
	import {
		SvelteFlow,
		Controls,
		Background,
		BackgroundVariant,
		type Node,
		type Edge,
		useSvelteFlow
	} from '@xyflow/svelte';
	import '@xyflow/svelte/dist/style.css';

	import { getFiles, uploadFile, updateFileById } from '$lib/apis/files';
	import FileNode from './FileNode.svelte';
	import Spinner from '../common/Spinner.svelte';

	const i18n = getContext('i18n');
	const { screenToFlowPosition } = useSvelteFlow();

	let nodes = writable<Node[]>([]);
	let edges = writable<Edge[]>([]);
	let loading = true;
	let fileInput;

	const nodeTypes = {
		file: FileNode
	};

	const loadFiles = async () => {
		loading = true;
		const res = await getFiles(localStorage.token).catch((err) => {
			toast.error(err);
			return { items: [] };
		});

		const fileNodes: Node[] = res.items.map((file, idx) => {
			const pos = file.data?.whiteboard_position || {
				x: 100 + (idx % 4) * 220,
				y: 100 + Math.floor(idx / 4) * 150
			};

			return {
				id: file.id,
				type: 'file',
				position: pos,
				class: 'file-node',
				data: { 
					file,
					onDelete: (id: string) => {
						nodes.update((n) => n.filter((node) => node.id !== id));
					}
				}
			};
		});

		nodes.set(fileNodes);
		loading = false;
	};

	const onNodeDragStop = async (event: any) => {
		const { node } = event.detail;
		await updateFileById(localStorage.token, node.id, {
			data: {
				whiteboard_position: node.position
			}
		}).catch((err) => {
			console.error('Failed to save node position:', err);
		});
	};

	const processFiles = async (files: File[], forcePosition?: { x: number, y: number }) => {
		let position = forcePosition || { x: 100, y: 100 };

		for (const file of files) {
			const uploadRes = await uploadFile(localStorage.token, file).catch((err) => {
				toast.error(err);
				return null;
			});

			if (uploadRes) {
				await updateFileById(localStorage.token, uploadRes.id, {
					data: {
						whiteboard_position: position
					}
				});

				nodes.update((n) => [
					...n,
					{
						id: uploadRes.id,
						type: 'file',
						position: { ...position },
						data: { 
							file: uploadRes,
							onDelete: (id: string) => {
								nodes.update((nodes) => nodes.filter((node) => node.id !== id));
							}
						}
					}
				]);
				
				position.x += 20;
				position.y += 20;
			}
		}
	};

	const handleFileDrop = async (e: DragEvent) => {
		e.preventDefault();
		const files = Array.from(e.dataTransfer?.files || []);
		if (files.length === 0) return;

		const position = screenToFlowPosition({
			x: e.clientX,
			y: e.clientY
		});

		await processFiles(files, position);
	};

	const onFileChange = async (e) => {
		const files = Array.from(e.target.files);
		if (files.length > 0) {
			await processFiles(files);
		}
	};

	onMount(() => {
		loadFiles();
	});
</script>

<input
	bind:this={fileInput}
	type="file"
	multiple
	class="hidden"
	on:change={onFileChange}
/>

<div 
	class="flex-1 w-full h-full relative overflow-hidden bg-[#fafafa] dark:bg-[#050505]"
	on:dragover|preventDefault
	on:drop={handleFileDrop}
>
	{#if loading}
		<div class="absolute inset-0 flex items-center justify-center z-20 bg-gray-50/50 dark:bg-gray-950/50 backdrop-blur-[2px]">
			<Spinner className="size-8" />
		</div>
	{/if}

	<SvelteFlow
		{nodes}
		{edges}
		{nodeTypes}
		fitView
		on:nodedragstop={onNodeDragStop}
		colorMode="system"
		minZoom={0.2}
		maxZoom={2}
	>
		<Background variant={BackgroundVariant.Dots} gap={24} size={1.2} color="#888" />
		<Controls position="bottom-right" showLock={false} />
		
		<div class="absolute top-6 left-1/2 -translate-x-1/2 z-10 pointer-events-none">
			<div class="bg-white/90 dark:bg-gray-900/90 backdrop-blur-md border border-gray-100/50 dark:border-gray-800/50 rounded-2xl px-6 py-4 shadow-2xl flex items-center space-x-6 pointer-events-auto transition-all hover:scale-[1.02]">
				<div class="flex flex-col">
					<h2 class="text-base font-bold text-gray-900 dark:text-gray-100 flex items-center">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-5 mr-2 text-blue-500">
							<path d="M3.75 3A1.75 1.75 0 0 0 2 4.75v10.5c0 .966.784 1.75 1.75 1.75h12.5A1.75 1.75 0 0 0 18 15.25V7.414A1.75 1.75 0 0 0 17.485 6.18l-3.665-3.666a1.75 1.75 0 0 0-1.236-.514H3.75Z" />
						</svg>
						{$i18n.t('Document Folder')}
					</h2>
					<p class="text-[11px] text-gray-500 font-medium uppercase tracking-wider">{$i18n.t('Interactive Board')}</p>
				</div>
				
				<div class="h-8 w-[1px] bg-gray-100 dark:bg-gray-800" />
				
				<button 
					on:click={() => fileInput.click()}
					class="bg-blue-600 hover:bg-blue-700 text-white rounded-xl px-4 py-2 text-sm font-semibold transition-all shadow-lg shadow-blue-500/20 active:scale-95 flex items-center"
				>
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-4 mr-2">
						<path d="M10.75 4.75a.75.75 0 0 0-1.5 0v4.5h-4.5a.75.75 0 0 0 0 1.5h4.5v4.5a.75.75 0 0 0 1.5 0v-4.5h4.5a.75.75 0 0 0 0-1.5h-4.5v-4.5Z" />
					</svg>
					{$i18n.t('Add Files')}
				</button>
			</div>
		</div>

		<div class="absolute bottom-6 left-6 z-10 pointer-events-none hidden md:block">
			<div class="bg-gray-900/5 dark:bg-white/5 backdrop-blur-[1px] rounded-lg px-3 py-2 text-[10px] text-gray-400 font-medium uppercase tracking-[0.2em]">
				{$i18n.t('Drag & Drop anywhere to upload')}
			</div>
		</div>
	</SvelteFlow>
</div>

<style>
	:global(.svelte-flow__container) {
		background-color: transparent !important;
	}
	
	:global(.svelte-flow__controls) {
		display: flex !important;
		flex-direction: row !important;
		gap: 4px !important;
		background: rgba(255, 255, 255, 0.9) !important;
		backdrop-filter: blur(8px) !important;
		border-radius: 12px !important;
		padding: 4px !important;
		border: 1px solid rgba(0, 0, 0, 0.05) !important;
		box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1) !important;
	}

	:global(html.dark .svelte-flow__controls) {
		background: rgba(17, 24, 39, 0.9) !important;
		border-color: rgba(255, 255, 255, 0.05) !important;
	}

	:global(.svelte-flow__controls-button) {
		border: none !important;
		background: transparent !important;
		width: 32px !important;
		height: 32px !important;
		display: flex !important;
		align-items: center !important;
		justify-content: center !important;
		border-radius: 8px !important;
		transition: all 0.2s !important;
	}

	:global(.svelte-flow__controls-button:hover) {
		background: rgba(0, 0, 0, 0.05) !important;
	}

	:global(html.dark .svelte-flow__controls-button:hover) {
		background: rgba(255, 255, 255, 0.1) !important;
	}

	:global(.svelte-flow__controls-button svg) {
		fill: currentColor !important;
	}
</style>
