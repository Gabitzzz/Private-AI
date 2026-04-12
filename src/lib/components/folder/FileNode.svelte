<script lang="ts">
	import { Handle, Position } from '@xyflow/svelte';
	import { getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { deleteFileById } from '$lib/apis/files';
	
	import Document from '$lib/components/icons/Document.svelte';
	import Photo from '$lib/components/icons/Photo.svelte';
	import Headphone from '$lib/components/icons/Headphone.svelte';
	import CommandLine from '$lib/components/icons/CommandLine.svelte';
	import Trash from '$lib/components/icons/GarbageBin.svelte';
	import Download from '$lib/components/icons/ArrowDownTray.svelte';

	const i18n = getContext('i18n');

	export let data;
	const { file, onDelete } = data;

	const getFileIcon = (filename: string) => {
		const extension = filename.split('.').pop()?.toLowerCase();
		if (['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp'].includes(extension)) return Photo;
		if (['mp3', 'wav', 'ogg', 'm4a'].includes(extension)) return Headphone;
		if (['py', 'js', 'ts', 'html', 'css', 'json', 'sh', 'md'].includes(extension)) return CommandLine;
		return Document;
	};

	const formatSize = (bytes: number) => {
		if (bytes === 0) return '0 B';
		const k = 1024;
		const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
		const i = Math.floor(Math.log(bytes) / Math.log(k));
		return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
	};

	const handleDelete = async () => {
		const res = await deleteFileById(localStorage.token, file.id).catch((err) => {
			toast.error(err);
			return null;
		});

		if (res) {
			toast.success($i18n.t('File deleted successfully'));
			onDelete(file.id);
		}
	};

	const handleDownload = () => {
		window.open(`/api/v1/files/${file.id}/content?attachment=true`, '_blank');
	};

	$: Icon = getFileIcon(file.filename);
</script>

<div class="group relative flex flex-col w-48 bg-white dark:bg-gray-900 rounded-xl border border-gray-100 dark:border-gray-800 shadow-sm hover:shadow-md transition-all p-3 select-none">
	<Handle type="target" position={Position.Top} className="opacity-0" />
	
	<div class="flex items-start justify-between mb-2">
		<div class="p-2 bg-gray-50 dark:bg-gray-850 rounded-lg text-gray-600 dark:text-gray-400">
			<Icon className="size-6" />
		</div>
		
		<div class="flex space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
			<button 
				on:click|stopPropagation={handleDownload}
				class="p-1.5 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md text-gray-500 transition-colors"
				title={$i18n.t('Download')}
			>
				<Download className="size-4" />
			</button>
			<button 
				on:click|stopPropagation={handleDelete}
				class="p-1.5 hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-500 hover:text-red-600 transition-colors rounded-md"
				title={$i18n.t('Delete')}
			>
				<Trash className="size-4" />
			</button>
		</div>
	</div>

	<div class="flex flex-col overflow-hidden">
		<span class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate mb-0.5" title={file.filename}>
			{file.filename}
		</span>
		<span class="text-xs text-gray-500 dark:text-gray-500">
			{formatSize(file.meta?.size || 0)}
		</span>
	</div>

	<Handle type="source" position={Position.Bottom} className="opacity-0" />
</div>

<style>
	:global(.svelte-flow__node-file) {
		padding: 0;
		border: none;
		background: transparent;
	}
</style>
