import { ref, computed, unref } from 'vue'
import { delay } from '../utils/tools'

export const useRemoveItemsDialog = (_service = null, _title = '', _keys = ['id', 'name'], _handle_end = () => {}, _items = (() => [])) =>
{
    const first_open = ref(false)
    const second_open = ref(false)

    const items = computed(_items)
    const is_loading = ref(false)

    const title = ref(_title)
    const counter = ref(0)
    const error_codes = ref([])
    const success_counter = ref(0)
    const error_counter = ref(0)
    const keys = ref(_keys)
    const handle_end = _handle_end
    const corner_close = ref(true)

    const handle_delete = async () =>
    {
        success_counter.value = 0
        error_counter.value = 0
        error_codes.value = []
        if(is_loading.value) return
        is_loading.value = true
        corner_close.value = false
        try
        {
            for(const item of items.value)
            {
                try
                {
                    await _service.delete(item[keys.value[0]])
                    counter.value++ 
                    success_counter.value++
                    error_codes.value.push([item[keys.value[1]], 'ITEM_DELETE_SUCCESS'])
                    await delay(250)
                }
                catch (e)
                {
                    error_codes.value.push([item[keys.value[1]], e?.response?.data?.detail?.error_code || e?.message || 'An error occurred'])
                    error_counter.value++
                    await delay(250)
                }
            }
        }
        catch (e)
        {
            console.error(e)
            error_codes.value.push(['Unknown item', e?.response?.data?.detail?.error_code || e?.message || 'An error occurred'])
        }
        finally
        {
            is_loading.value = false
            first_open.value = false
            second_open.value = true
            corner_close.value = true
        }
    }

    return { first_open, second_open, items, is_loading, handle_delete, title, counter, error_codes, success_counter, error_counter, handle_end, keys, corner_close }
}