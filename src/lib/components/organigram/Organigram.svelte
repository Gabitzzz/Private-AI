<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { writable } from 'svelte/store';
	import {
		SvelteFlow,
		Background,
		BackgroundVariant,
		type Node,
		type Edge,
		ConnectionLineType,
		MarkerType
	} from '@xyflow/svelte';
	import '@xyflow/svelte/dist/style.css';

	import MemberNode from './MemberNode.svelte';

	const i18n = getContext('i18n');

	const nodeTypes = {
		member: MemberNode
	};

	let nodes = writable<Node[]>([
		{
			id: 'root',
			type: 'member',
			position: { x: 400, y: 50 },
			data: { 
				name: 'Open WebUI Corporation', 
				isRoot: true 
			}
		},
		// Level 1
		{
			id: 'cto',
			type: 'member',
			position: { x: 150, y: 200 },
			data: { 
				name: 'Jane Doe', 
				role: 'CTO', 
				color: '#3b82f6',
				image: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jane'
			}
		},
		{
			id: 'cfo',
			type: 'member',
			position: { x: 400, y: 200 },
			data: { 
				name: 'John Smith', 
				role: 'CFO', 
				color: '#10b981',
				image: 'https://api.dicebear.com/7.x/avataaars/svg?seed=John'
			}
		},
		{
			id: 'coo',
			type: 'member',
			position: { x: 650, y: 200 },
			data: { 
				name: 'Sarah Wilson', 
				role: 'COO', 
				color: '#f59e0b',
				image: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Sarah'
			}
		},
		// Level 2 under CTO
		{
			id: 'eng',
			type: 'member',
			position: { x: 50, y: 400 },
			data: { 
				name: 'Mike Johnson', 
				role: 'VP Engineering', 
				color: '#3b82f6',
				image: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Mike'
			}
		},
		{
			id: 'ai',
			type: 'member',
			position: { x: 250, y: 400 },
			data: { 
				name: 'Alice AI', 
				role: 'AI Director', 
				color: '#8b5cf6',
				image: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alice'
			}
		}
	]);

	let edges = writable<Edge[]>([
		{ id: 'e-root-cto', source: 'root', target: 'cto', type: 'bezier', animated: true, style: 'stroke: #cbd5e1; stroke-width: 2;' },
		{ id: 'e-root-cfo', source: 'root', target: 'cfo', type: 'bezier', animated: true, style: 'stroke: #cbd5e1; stroke-width: 2;' },
		{ id: 'e-root-coo', source: 'root', target: 'coo', type: 'bezier', animated: true, style: 'stroke: #cbd5e1; stroke-width: 2;' },
		{ id: 'e-cto-eng', source: 'cto', target: 'eng', type: 'bezier', style: 'stroke: #cbd5e1; stroke-width: 2;' },
		{ id: 'e-cto-ai', source: 'cto', target: 'ai', type: 'bezier', style: 'stroke: #cbd5e1; stroke-width: 2;' }
	]);
</script>

<div class="flex-1 w-full h-full relative overflow-hidden">
	<div class="absolute top-8 left-8 z-10">
		<h1 class="text-3xl font-black text-gray-900 dark:text-white tracking-tight">
			Corporate <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Organigram</span>
		</h1>
		<p class="text-gray-500 dark:text-gray-400 mt-1 font-medium italic">Visualize your organizational structure</p>
	</div>

	<SvelteFlow
		{nodes}
		{edges}
		{nodeTypes}
		fitView
		connectionLineType={ConnectionLineType.Bezier}
		colorMode="system"
	>
		<Background variant={BackgroundVariant.Lines} gap={40} size={1} color="#f1f5f9" />
	</SvelteFlow>
</div>

<style>
	:global(.svelte-flow__container) {
		background-color: transparent !important;
	}
	
	:global(.svelte-flow__node) {
		background: transparent !important;
		border: none !important;
		padding: 0 !important;
	}

	:global(.svelte-flow__edge-path) {
		stroke-dasharray: 5;
		animation: dash 20s linear infinite;
	}

	@keyframes dash {
		from {
			stroke-dashoffset: 1000;
		}
		to {
			stroke-dashoffset: 0;
		}
	}

	:global(html.dark .svelte-flow__background) {
		--bg-color: #050505;
		--line-color: #111;
	}
</style>
