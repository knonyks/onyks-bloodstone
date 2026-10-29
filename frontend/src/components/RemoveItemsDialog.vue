<script setup>
    const model = defineModel()
</script>

<template>
    <onyks-dialog :open="model.first_open" @dialog-close="model.first_open = false" :corner-close="model.corner_close || undefined" :title="model.title" bottom-buttons modal>
        <onyks-container gap="m" type="stack">
            <onyks-text v-if="model.items.length == 1">{{$t('common.trying_to_remove_1', { count: model.items.length })}}</onyks-text>
            <onyks-text v-else>{{$t('common.trying_to_remove_2', { count: model.items.length })}}</onyks-text>
            <onyks-container class="delete-items" padding="m" gap="m">

                <onyks-text v-for="(item, index) in model.items" :key="item[model.keys[0]]">{{ index + 1 }}. {{ item[model.keys[1]] }}</onyks-text>

            </onyks-container>
            <onyks-loading-bar size="m" striped animated :max="model.items.length" :current-state="model.counter"></onyks-loading-bar>
        </onyks-container>
        <onyks-button background="green" slot="footer" @click="() => model.handle_delete(model.keys)" :disabled="model.is_loading" size="m">{{$t('common.confirm')}}</onyks-button>
    </onyks-dialog>

    <onyks-dialog :open="model.second_open" @dialog-close="() => { model.second_open = false; model.counter = 0; model.error_codes = []; model.success_counter = 0; model.error_counter = 0; model.handle_end() }" corner-close :title="$t('common.removing_result')" modal>
        <onyks-container gap="m" type="stack">
            <onyks-text>{{$t('common.removed_x_of_y', [ model.success_counter, model.items.length ])}} {{ model.error_counter > 0 ? $t('common.some_items_could_not_be_deleted') : '' }}</onyks-text>
            <onyks-container class="delete-items" gap="m" type="grid" cols="10" padding="m" mobile-breakpoint="500">
                
                <template v-for="(item, index) in model.error_codes" :key="index">
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