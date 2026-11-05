import { ref } from 'vue'
import { services } from '../utils/api'

export const useRepositoryExplorer = () =>
{
    const path = ref([])
    const filter = ref((e) => e.type === 'dir' || e.type === 'schlib' || e.type === 'pcblib' || e.type === 'footprint' || e.type === 'symbol')
    const content = ref([])
    const current_selected = ref({})

    const init = async () =>
    {
        path.value = [(await services.repository.info()).data.name]
        let temp = Array.from((await services.repository.content('/')).data)
        temp = temp.filter(e => filter.value(e))
        content.value = temp
    }

    const path_change = async (e) =>
    {
        path.value = e.detail.path
        let temp = Array.from((await services.repository.content(e.detail.path.slice(1).join('/'))).data)
        temp = temp.filter(e => filter.value(e))
        content.value = temp
        current_selected.value = { type: '', name: '' }
    }

    const enter_folder = async (e) =>
    {
        path.value = [...path.value, e.detail.folder.name]
        let temp = Array.from((await services.repository.content(path.value.slice(1).join('/'))).data)
        temp = temp.filter(e => filter.value(e))
        content.value = temp
        current_selected.value = { type: '', name: '' }
    }

    const refresh = async () =>
    {
        let temp = Array.from((await services.repository.content(path.value.slice(1).join('/'))).data)
        temp = temp.filter(e => filter.value(e))
        content.value = temp
    }

    const handle_select = (e) =>
    {
        current_selected.value = e.detail.items[0]
    }

    return { path, filter, content, current_selected, init, path_change, enter_folder, refresh, handle_select }
}