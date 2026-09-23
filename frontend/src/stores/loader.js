import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLoaderStore = defineStore('loader', () => 
{
    const globalIsLoading = ref(false)
    const isLoading = ref(false)

    function show() 
    {
        isLoading.value = true
    }

    function hide() 
    {
        isLoading.value = false
    }

    function globalShow()
    {
        globalIsLoading.value = true
    }

    function globalHide()
    {
        globalIsLoading.value = false
    }

    return { isLoading, globalIsLoading, show, hide, globalShow, globalHide}
})