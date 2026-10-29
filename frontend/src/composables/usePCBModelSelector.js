import { ref, reactive, watch } from 'vue'
import { useRepositoryExplorer } from './useRepositoryExplorer'


export const usePCBModelSelector = (_title = '', _filter = (() => true), _handle_ok = () => {}, _handle_reset = () => {}) =>
{
    const open = ref(false)
    const title = ref(_title)
    const repository = reactive(useRepositoryExplorer())
    repository.filter = _filter
    const error = ref('')
    const init = repository.init

    const handle_ok = _handle_ok
    const handle_reset = _handle_reset

    watch(repository, () => { error.value = '' })

    return { open, title, repository, init, handle_ok, handle_reset, error }
}