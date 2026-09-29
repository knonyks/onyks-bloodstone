<script setup>
    import { ref } from 'vue';

    const emit = defineEmits(['page-change', 'checkbox-click'])
    const model = defineModel({ required: true });
    const table = ref(null);

    const handleCheckboxClick = (e) =>
    {
        const detail = e.detail;
        const data = model.value?.data?.items;
        if (!detail || !Array.isArray(data)) return;

        if(detail.type === 'row')
        {
            const row = data[detail.rowIndex];
            if (row) row.selected = detail.checked;
        }
        else
        {
            data.forEach((item) => item.selected = detail.checked)
        }
        model.value.selectedCount = data.filter((item) => item.selected).length
        emit('checkbox-click', detail)
    }

    const handlePageChange = (event) =>
    {
        const index = event.detail?.index;
        if (index == null) return;
        model.value.nextPage?.(index);
        emit('page-change', index);
    }

    const refresh = () =>
    {
        table?.value?.refresh?.()
    }

    defineExpose({ refresh });
</script>

<template>
    <onyks-container gap="l" align="center">
        <onyks-container :class="{ extend: model.extend }" :padding="`${model.extend ? 'm' : ''}`">
            <onyks-table ref="table" :columns="model?.columns ?? []" :data="model?.data?.items ?? []" @checkbox-click="handleCheckboxClick"></onyks-table>
        </onyks-container>
        <onyks-container type="group" align="center" justify="center" gap="m">
            <onyks-pagination-nav :max-index="Math.ceil((model.data?.total ?? 0) / (model.data?.limit || 1))" :index="model.data?.page ?? 1" max-view="3" size="m" @page-change="handlePageChange"></onyks-pagination-nav>
            <onyks-text>Selected:&emsp;{{model.selectedCount}}&emsp;|&emsp;Total:&emsp;{{ model.data?.total ?? 0 }}</onyks-text>
        </onyks-container>
    </onyks-container>
</template>

<style lang="css" scoped>
    onyks-table
    {
        height: 450px;
        box-sizing: border-box;
        width: 100%;
    }

    .extend
    {
        box-sizing: border-box;
        width: 100vw;
        position: relative;
        padding-top: 0;
        padding-bottom: 0;
    }

    .extend > onyks-table
    {
        height: 700px;
    }

    onyks-container
    {
        width: 100%;
        white-space: nowrap
    }

    onyks-text
    {
        flex: 1;
        text-align: right;
    }
</style>