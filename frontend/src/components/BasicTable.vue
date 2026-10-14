<script setup>
    const model = defineModel();
</script>

<template>
    <onyks-container gap="l" align="center">

        <onyks-table :expandedTemplate="model.expandedTemplate" :expandable="model.expandable" :columns="model?.columns ?? []" :data="model?.data ?? []" @checkbox-click="model.checkboxClick($event.detail)"></onyks-table>

        
        <onyks-container type="group" align="center" justify="center" gap="m">
            <onyks-pagination-nav :max-index="Math.ceil((model?.total ?? 0) / (model?.limit || 1))" :index="model?.page ?? 1" max-view="3" size="m" @page-change="model.pageChange($event.detail?.index)"></onyks-pagination-nav>
            <onyks-text>Selected:&emsp;{{model.selected}}&emsp;|&emsp;Total:&emsp;{{ model?.total ?? 0 }}</onyks-text>
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