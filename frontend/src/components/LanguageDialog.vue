<script setup>
    import { ref } from 'vue';
    import { US, GB, PL } from 'country-flag-icons/string/3x2'

    const languages = ref([
        { code: 'pl', name: 'Polski', flag: PL },
        { code: 'en', name: 'English', flag: GB }
    ])
</script>

<template>
    <!-- <onyks-dialog class="dialog" open corner-close bottom-buttons modal title="Language">
        <onyks-container type="stack" padding="" gap="m">
            <onyks-select  class="select">
                <onyks-select-option :value="lang.code" v-for="lang in languages" :key="lang.code">
                    <onyks-container type="group" gap="s" align="center">
                        <span v-html="lang.flag" class="flag"></span>
                        <onyks-text>{{ lang.name }}</onyks-text>
                    </onyks-container>
                </onyks-select-option>
            </onyks-select>
        </onyks-container>
        <onyks-button background="green" slot="footer">OK</onyks-button>
    </onyks-dialog> -->
</template>

<style lang="css" scoped>
    .select
    {
        height: 200px;
        width: 100%;
    }

    .dialog::part(container)
    {
        max-width: 500px;
    }

    .flag,
    .flag :deep(svg)
    {
        display: inline-block;
        width: 20px;
        height: 20px;
        vertical-align: middle;
        flex-shrink: 0;
    }

    .flag :deep(svg)
    {
        aspect-ratio: 3 / 2;
    }

</style>