import { ref } from 'vue'

export const useSuppliersSelector = (_service, _handle_change = () => {}) =>
{
    const items = ref([])
    const total = ref(0)
    const service = _service
    const page = ref(1)
    const limit = ref(100)
    const search_phrase = ref('')
    const sort_by = ref('id')
    const sort_desc = ref(false)
    const item = ref([])

    const init = async () =>
    {
        const result = await service.list(page.value, limit.value, search_phrase.value, sort_by.value, sort_desc.value)
        items.value = result?.data?.items ?? []
        items.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    const handle_scroll_end = async () =>
    {
        page.value++
        const result = await service.list(page.value, limit.value, search_phrase.value, sort_by.value, sort_desc.value)
        items.value = items.value.concat(result?.data?.items ?? [])
        items.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    const handle_change = ref((value) =>
    {
        item.value = []
        if(value.selected)
            item.value.push(value.value)
        _handle_change(value)
    })

    const search = async () =>
    {
        page.value = 1
        const result = await service.list(page.value, limit.value, search_phrase.value, sort_by.value, sort_desc.value)
        items.value = result?.data?.items ?? []
        items.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    return { items, total, page, limit, search_phrase, sort_by, sort_desc, init, handle_scroll_end, handle_change, search, item }
}
