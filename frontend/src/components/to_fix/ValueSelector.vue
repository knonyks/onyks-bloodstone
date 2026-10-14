<script setup lang="js">
    import { reactive } from 'vue';
    import BasicSearch from './BasicSearch.vue';
    
    const selectedItem = defineModel(
    {
        type: Object,
        default: () => ({ id: 0, name: '' })
    })

    const props = defineProps({
        service: {
            type: Object,
            required: true
        }
    })

    // Grupowanie stanu w jeden czytelny obiekt
    const state = reactive({
        items: [],
        query: '',
        total: 0,
        page: 1,
        isLoading: false // Blokada na podwójne zapytania
    })
    
    const search = async () => {
        state.isLoading = true;
        try {
            let response = await props.service.list(1, 50, state.query)
            state.items = response.data.items
            state.total = response.data.total
            state.page = 1
        } catch (error) {
            console.error("Błąd wyszukiwania:", error)
        } finally {
            state.isLoading = false;
        }
    }

    const scrollEnd = async () => {
        // Blokada: jeśli już ładujemy albo dotarliśmy do końca, nie rób nic
        if(state.isLoading || state.items.length >= state.total) return;
        
        state.isLoading = true;
        try {
            let response = await props.service.list(state.page + 1, 50, state.query)
            state.items.push(...response.data.items); // Zamiast concat, ładniejsze i szybsze
            state.total = response.data.total
            state.page += 1
        } catch (error) {
            console.error("Błąd paginacji:", error)
        } finally {
            state.isLoading = false;
        }
    }

    const change = (e) => {
        // Skoro rodzic przekazał v-model do obiektu, odsyłamy cały obiekt
        if(e.detail.selected) {
            selectedItem.value = {
                id: e.detail.value.id,
                name: e.detail.value.name
            };
        } else {
            selectedItem.value = { id: 0, name: '' };
        }        
    }

    const init = async () => {
        state.query = ''; // Resetujemy pole tekstowe
        await search();   // Po prostu wywołujemy search, logika tam już jest!
    }

    defineExpose({ init, search })
</script>

<template>
    <onyks-container gap="m">
        <onyks-text>Selected: {{ selectedItem.name || 'None' }}</onyks-text>

        <BasicSearch v-model="state.query" :search="search"></BasicSearch>
        
        <onyks-select @scroll-end="scrollEnd" @change="change">
            <onyks-select-option 
                v-for="el in state.items" 
                :key="el.id" 
                :value="el" 
                :selected="el.id === selectedItem.id"
            >
                {{ el.name }}
            </onyks-select-option>
        </onyks-select>

        <onyks-text>Total:&emsp;{{ state.items.length }}&emsp;/&emsp;{{ state.total }}</onyks-text>
        
    </onyks-container>
</template>

<style lang="css" scoped>
    onyks-button {
        width: 100%;
    }

    onyks-select {
        width: 100%;
        height: 300px;
    }
</style>