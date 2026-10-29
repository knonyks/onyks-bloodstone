import { ref, watch } from 'vue'

export const useBasicTable = (_service = undefined, _columns = [], _sort_by = 'id', _format_data = (item) => item, _expanded_template = (row) => html`${row ? JSON.stringify(row) : ''}`) =>
{
    const columns = ref(_columns)
    const data = ref([])
    const service = ref(_service)
    const page = ref(1)
    const total = ref(0)
    const limit = ref(100)
    const search_phrase = ref('')
    const sort_by = ref(_sort_by)
    const sort_desc = ref(false)
    const selected = ref(0)
    const expandable = ref(false)
    const format_data = ref(_format_data)
    const expanded_template = ref(_expanded_template)

    const init = async () =>
    {
        const result = await service.value.list(page.value, limit.value, search_phrase.value, sort_by.value, sort_desc.value)
        data.value = result?.data?.items ?? []
        data.value = data.value.map((item) => format_data.value(item))
        total.value = result?.data?.total ?? 0
    }

    const checkbox_click = (details) =>
    {
        if(details.type === 'row')
        {
            const row = data.value[details.rowIndex];
            if (row) row.selected = details.checked;
        }
        else
        {
            data.value.forEach((item) => item.selected = details.checked)
        }
        selected.value = data.value.filter((item) => item.selected).length
    }

    watch(() => data.value, (newItems) => 
    {
        selected.value = (newItems || []).filter((item) => item.selected).length
    });

    const page_change = async (index) =>
    {
        data.value = (await service.value.list(index, limit.value, search_phrase.value, sort_by.value, sort_desc.value))?.data?.items ?? []
        data.value = data.value.map((item) => format_data.value(item))
        if (index == null) return;
        page.value = index;
    }

    const search = async () =>
    {
        page.value = 1
        const result = await service.value.list(page.value, limit.value, search_phrase.value, sort_by.value, sort_desc.value)
        data.value = result?.data?.items ?? []
        data.value = data.value.map((item) => format_data.value(item))
        total.value = result?.data?.total ?? 0
    }

    return { columns, data, service, page, total, limit, search_phrase, sort_by, sort_desc, selected, expandable, format_data, expanded_template, init, checkbox_click, page_change, search }
}