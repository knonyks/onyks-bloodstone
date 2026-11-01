import { ref } from "vue"

export const useTagsSelector = (_service, tags) =>
{
    const options = ref([])
    const service = _service
    const text = ref('')

    const init = async () =>
    {
        const result = await service.list()
        result.data.items.map(item => { item.label = item.name; item.value = item.name })
        options.value = result?.data?.items ?? []
    }

    const keydownHandler = async (event) =>
    {
        if (event.key === 'Backspace')
        {
            if(text.value === '')
                tags.value.pop();
        }
        if (event.key === 'Enter')
        {
            if (text.value.trim() !== '')
            {
                const tag = text.value.trim().toLowerCase()
                if (!tags.value.some(existing => existing.trim().toLowerCase() === tag))
                    tags.value.push(tag)
            }
            text.value = ''
            await init()
        }
    }

    const select = async (event) =>
    {
        const option = event.detail.name
        if (!tags.value.some(existing => existing.trim().toLowerCase() === option.trim().toLowerCase()))
            tags.value.push(option)
        text.value = ''
        await init()
    }

    const search = async () =>
    {
        if (text.value.trim() === '')
        {
            await init()
            return
        }

        const result = await service.list(1, 10, text.value, 'name', false)
        result.data.items.map(item => { item.label = item.name; item.value = item.name })
        options.value = result?.data?.items ?? []
    }

    return { options, init, keydownHandler, text, search, select }
}