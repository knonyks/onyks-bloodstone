<script setup>
    const model = defineModel()
</script>

<template>
    <onyks-dialog :open="model.firstOpen" @dialog-close="model.firstOpen = false" corner-close :title="model.title" bottom-buttons modal>
        <onyks-container gap="m" type="stack">
            <onyks-text v-if="model.items.length == 1">{{$t('components.DeleteItemsDialog.subtitle1', { count: model.items.length })}}</onyks-text>
            <onyks-text v-else>{{$t('components.DeleteItemsDialog.subtitle2', { count: model.items.length })}}</onyks-text>
            <onyks-container class="delete-items" padding="m" gap="m">

                <onyks-text v-for="(item, index) in model.items" :key="item.id">{{ index + 1 }}. {{ item.name }}</onyks-text>

            </onyks-container>
            <onyks-loading-bar size="m" striped animated :max="model.items.length" :current-state="model.counter"></onyks-loading-bar>
        </onyks-container>
        <onyks-button background="green" slot="footer" @click="model.handleDelete" :disabled="model.isLoading" size="m">{{$t('components.DeleteItemsDialog.confirm')}}</onyks-button>
    </onyks-dialog>

    <onyks-dialog :open="model.secondOpen" @dialog-close="() => { model.secondOpen = false; model.counter = 0; model.errorCodes = []; model.succesCounter = 0; model.errorCounter = 0; model.handleEnd() }" corner-close :title="$t('components.DeleteItemsDialog.result')" modal>
        <onyks-container gap="m" type="stack">
            <onyks-text>{{$t('components.DeleteItemsDialog.deleted', { counter: model.succesCounter, length: model.items.length })}} {{ model.errorCounter > 0 ? $t('components.DeleteItemsDialog.someItemsCouldNotBeDeleted') : '' }}</onyks-text>
            <onyks-container class="delete-items" gap="m" type="grid" cols="10" padding="m" mobile-breakpoint="500">
                
                <template v-for="(item, index) in model.errorCodes" :key="index">
                    <onyks-text cols="4">{{ item[0] }} </onyks-text>
                    <onyks-tag cols="6" :background="item[1] === 'ITEM_DELETE_SUCCESS' ? 'green' : 'red'" :icon="item[1] === 'ITEM_DELETE_SUCCESS' ? 'F270' : 'F627'">{{ $t('error_codes.' + item[1]) }}</onyks-tag>
                </template>
                
            </onyks-container>
        </onyks-container>
    </onyks-dialog>
</template>

<style lang="css" scoped>
    .delete-items 
    {
        overflow-y: auto;
        max-height: 200px;
    }

    onyks-tag
    {
        max-width: 100%;
        box-sizing: border-box;
    }
</style>