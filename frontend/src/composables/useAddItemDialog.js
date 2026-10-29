import { ref } from 'vue'
import { i18n } from '@/utils/localization'

export const useAddItemDialog = (_service = null, _title = '', _handle_end = () => {}) =>
{
    const open = ref(false)
    const name = ref('')
    const error = ref('')
    const title = ref(_title)
    const is_loading = ref(false)

    const handle_ok = async () =>
    {
        if(is_loading.value) return
        is_loading.value = true
        try
        {
            await _service.create(name.value)
            name.value = ''
            error.value = ''
            open.value = false
            _handle_end()
        }
        catch (e)
        {
            error.value = i18n.global.t(`error_codes.${e?.response?.data?.detail?.error_code}`) || e?.message || 'An error occurred'
        }
        finally
        {
            is_loading.value = false
        }
    }

    return { open, name, error, title, is_loading, handle_ok }
}
