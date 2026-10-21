import { degrees, PDFDocument, rgb, StandardFonts, PageSizes } from 'pdf-lib';
import QRCode from 'qrcode'
import { DateTime } from "luxon";
import { services } from './api';
import { reactive } from 'vue'
import { ref } from 'vue';
import { watch } from 'vue';
import { OnyksToastContainer } from 'onyks-web-ui-system'
import { computed } from 'vue';
import { unref } from 'vue';
import { html } from 'lit';

export const useRepository = (_filter = (e) => e.type === 'dir' || e.type === 'schlib' || e.type === 'pcblib' || e.type === 'footprint' || e.type === 'symbol') =>
{
    const path = ref([])
    const filter = ref(_filter)
    const content = ref([])
    const currentSelected = ref('')

    const init = async () =>
    {
        path.value = [(await services.repository.info()).data.name]
        let temp = Array.from((await services.repository.content('/')).data)
        temp = temp.filter(e => filter.value(e))
        content.value = temp
    }

    const pathChange = async (e) =>
    {
        path.value = e.detail.path
        let temp = Array.from((await services.repository.content(e.detail.path.slice(1).join('/'))).data)
        temp = temp.filter(e => filter.value(e))
        content.value = temp
        currentSelected.value = { type: '', name: '' }
    }

    const enterFolder = async (e) =>
    {
        path.value = [...path.value, e.detail.folder.name]
        let temp = Array.from((await services.repository.content(path.value.slice(1).join('/'))).data)
        temp = temp.filter(e => filter.value(e))
        content.value = temp
        currentSelected.value = { type: '', name: '' }
    }

    const refresh = async () =>
    {
        let temp = Array.from((await services.repository.content(path.value.slice(1).join('/'))).data)
        temp = temp.filter(e => filter.value(e))
        content.value = temp
    }

    const handleSelect = (e) =>
    {
        currentSelected.value = e.detail.items[0]
    }

    return { path, filter, content, currentSelected, init, pathChange, enterFolder, refresh, handleSelect }
}

export const useBasicTable = (_service, _columns, _expandable = false, _expandedTemplate = (row) => html`
    ${row ? JSON.stringify(row) : ''}
`) =>
{
    const columns = ref(_columns)
    const data = ref([{name: 'xx'}])
    const service = _service
    const page = ref(1)
    const total = ref(0)
    const limit = ref(100)
    const searchPhrase = ref('')
    const sortBy = ref('id')
    const sortDesc = ref(false)
    const selected = ref(0)
    const expandable = ref(_expandable)
    const expandedTemplate = ref(_expandedTemplate)

    const init = async () =>
    {
        const result = await service.list(page.value, limit.value, searchPhrase.value, sortBy.value, sortDesc.value)
        data.value = result?.data?.items ?? []
        data.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    const checkboxClick = (details) =>
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

    const pageChange = async (index) =>
    {
        data.value = (await service.list(index, limit.value, searchPhrase.value, sortBy.value, sortDesc.value))?.data?.items ?? []
        data.value.map((item) => item.selected = false)
        if (index == null) return;
        page.value = index;
    }

    const search = async () =>
    {
        page.value = 1
        const result = await service.list(page.value, limit.value, searchPhrase.value, sortBy.value, sortDesc.value)
        data.value = result?.data?.items ?? []
        data.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    return { columns, data, page, limit, total, searchPhrase, sortBy, sortDesc, selected, expandable, expandedTemplate, init, checkboxClick, pageChange, search }
}

export const useAddItemDialog = (_service = null, _title = '', _handleEnd = () => {}) =>
{
    const open = ref(false)
    const name = ref('')
    const error = ref('')
    const title = ref(_title) 
    const isLoading = ref(false)

    const handleOK = async () =>
    {
        if(isLoading.value) return
        isLoading.value = true
        try
        {
            await _service.create(name.value)
            name.value = ''
            error.value = ''
            open.value = false
            _handleEnd()
        }
        catch (e)
        {
            error.value = e?.response?.data?.detail?.error_code || e?.message || 'An error occurred'
        }
        finally
        {
            isLoading.value = false
        }
    }

    return { open, name, error, title, isLoading, handleOK }
}

export const useEditItemDialog = (_service = null, _title = '', _handleEnd = () => {}, _item = (() => null)) =>
{
    const open = ref(false)
    
    const error = ref('')
    const title = ref(_title) 
    const isLoading = ref(false)
    const item = computed(() => unref(typeof _item === 'function' ? _item() : _item))
    const name = ref(item.value?.name || '')
    // watch(item, value => { name.value = value?.name || '' }, { immediate: true })
    
    const handleOK = async () =>
    {
        if(isLoading.value) return
        isLoading.value = true
        try
        {
            await _service.edit(item.value.id, name.value)
            name.value = ''
            error.value = ''
            open.value = false
            _handleEnd()
        }
        catch (e)
        {
            console.dir(e)
            error.value = e?.response?.data?.detail?.error_code || e?.message || 'An error occurred'
        }
        finally
        {
            isLoading.value = false
        }
    }

    return { open, name, error, title, isLoading, handleOK, item }
}

export const useDeleteItemsDialog = (_service = null, _title = '', _handleEnd = () => {}, _items = (() => [])) =>
{
    const firstOpen = ref(false)
    const secondOpen = ref(false)

    const items = computed(() => unref(typeof _items === 'function' ? _items() : _items))
    const isLoading = ref(false)

    const title = ref(_title)
    const counter = ref(0)
    const errorCodes = ref([])
    const succesCounter = ref(0)
    const errorCounter = ref(0)
    const handleEnd = _handleEnd

    const handleDelete = async () =>
    {
        succesCounter.value = 0
        errorCounter.value = 0
        errorCodes.value = []
        if(isLoading.value) return
        isLoading.value = true

        try
        {
            for(const item of items.value)
            {
                try
                {
                    await _service.delete(item.id)
                    counter.value++ 
                    succesCounter.value++
                    errorCodes.value.push([item.name, 'ITEM_DELETE_SUCCESS'])
                }
                catch (e)
                {

                    errorCodes.value.push([item.name, e?.response?.data?.detail?.error_code || e?.message || 'An error occurred'])
                    errorCounter.value++
                }
            }
        }
        catch (e)
        {
            errorCodes.value.push(['Unknown item', e?.response?.data?.detail?.error_code || e?.message || 'An error occurred'])
        }
        finally
        {
            isLoading.value = false

            firstOpen.value = false
            secondOpen.value = true
        }
    }

    return { firstOpen, secondOpen, items, isLoading, handleDelete, title, counter, errorCodes, succesCounter, errorCounter, handleEnd }
}

export const useRepositoryModelDialog = (_title = '', _filter = (() => true), _handleOk = () => {}, _handleReset = () => {}) =>
{
    const open = ref(false)
    const title = ref(_title)
    const repository = reactive(useRepository(_filter))
    const error = ref('')
    const init = () => { repository.init() }

    const handleOk = _handleOk
    const handleReset = _handleReset

    watch(repository, () => { error.value = '' })

    return { open, title, repository, init, handleOk, error }
}

export const useValueSelector = (_service, _handleChange = () => {}) =>
{
    const items = ref([])
    const total = ref(0)
    const service = _service
    const page = ref(1)
    const limit = ref(100)
    const searchPhrase = ref('')
    const sortBy = ref('id')
    const sortDesc = ref(false)

    const init = async () =>
    {
        const result = await service.list(page.value, limit.value, searchPhrase.value, sortBy.value, sortDesc.value)
        items.value = result?.data?.items ?? []
        items.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    const handleScrollEnd = async () =>
    {
        page.value++
        const result = await service.list(page.value, limit.value, searchPhrase.value, sortBy.value, sortDesc.value)
        items.value = items.value.concat(result?.data?.items ?? [])
        items.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    const handleChange = _handleChange

    const search = async () =>
    {
        page.value = 1
        const result = await service.list(page.value, limit.value, searchPhrase.value, sortBy.value, sortDesc.value)
        items.value = result?.data?.items ?? []
        items.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    return { items, total, page, limit, searchPhrase, sortBy, sortDesc, init, handleScrollEnd, handleChange, search }
}

export const useSupplierSelector = (_service, _handleChange = () => {}) =>
{
    const items = ref([])
    const total = ref(0)
    const service = _service
    const page = ref(1)
    const limit = ref(100)
    const searchPhrase = ref('')
    const sortBy = ref('id')
    const sortDesc = ref(false)

    const init = async () =>
    {
        const result = await service.list(page.value, limit.value, searchPhrase.value, sortBy.value, sortDesc.value)
        items.value = result?.data?.items ?? []
        items.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    const handleScrollEnd = async () =>
    {
        page.value++
        const result = await service.list(page.value, limit.value, searchPhrase.value, sortBy.value, sortDesc.value)
        items.value = items.value.concat(result?.data?.items ?? [])
        items.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    const handleChange = _handleChange

    const search = async () =>
    {
        page.value = 1
        const result = await service.list(page.value, limit.value, searchPhrase.value, sortBy.value, sortDesc.value)
        items.value = result?.data?.items ?? []
        items.value.map((item) => item.selected = false)
        total.value = result?.data?.total ?? 0
    }

    return { items, total, page, limit, searchPhrase, sortBy, sortDesc, init, handleScrollEnd, handleChange, search }
}

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

    const keydownHandler = (event) =>
    {
        // if (event.key === 'Backspace')
        // {
        //     if(text.value === '')
        //         tags.value.pop();
        // }
        if (event.key === 'Enter')
        {
            if (text.value.trim() !== '')
            {
                const tag = text.value.trim().toLowerCase()
                if (!tags.value.some(existing => existing.trim().toLowerCase() === tag))
                    tags.value.push(tag)
            }
            text.value = ''            
        }
    }

    const select = (event) =>
    {
        const option = event.detail.name
        if (!tags.value.some(existing => existing.trim().toLowerCase() === option.trim().toLowerCase()))
            tags.value.push(option)
        text.value = ''
    }

    const search = async () =>
    {
        const result = await service.list(1, 10, text.value, 'name', false)
        result.data.items.map(item => { item.label = item.name; item.value = item.name })
        options.value = result?.data?.items ?? []
    }

    return { options, init, keydownHandler, text, search, select }
}

export const addToast = (message, duration = 3000, closable = true, size = 'm', type = 'info') =>
{
    const toastContainer = document.querySelector('.toast-container-content')
    if (toastContainer)
    {
        toastContainer.appendChild(OnyksToastContainer.addToast(message, duration, closable, size, type))
    }
}



export class LabelsDoc
{
    constructor(labelsAmount)
    {
        this.columns = 2
        this.rows = 6
        this.spacing = 7
        this.normalSize = 8
        this.bigSize = 12
        this.labelsAmount = labelsAmount
        this.width = PageSizes.A4[0]
        this.height = PageSizes.A4[1]
        this.widthStep = this.width / this.columns
        this.heightStep = this.height / this.rows
    }

    async addLogo(logoUrl)
    {
        this.logoBytes = await fetch(logoUrl).then((res) => res.arrayBuffer())
        this.logoImg = await this.pdf.embedPng(this.logoBytes)
        this.logoDims = await this.logoImg.scale(0.01)
    }

    async init()
    {
        this.pdf = await PDFDocument.create()
        for(let i=0; i<Math.ceil(this.labelsAmount/(this.columns*this.rows)); i++)
        {
            await this.pdf.addPage(PageSizes.A4)
        }
        this.pages = await this.pdf.getPages()
    }

    async drawBorders()
    {
        for(let i=0; i<this.labelsAmount; i++)
        {
            await this.__drawBorder(i)
        }
    }

    async __drawBorder(index)
    {
        let settings = 
        {
            thickness: 1,
            color: rgb(0, 0, 0),
            opacity: 0.5,
        }

        let col = index % this.columns
        let row = Math.floor((index % (this.rows * this.columns)) / 2)
        let page = Math.floor(index / (this.rows*this.columns))

        settings.start = { x: (this.width/2)*col, y: this.height - this.heightStep*(row + 1) }
        settings.end = { x: col == 0? this.width/2:this.width, y: this.height - this.heightStep*(row + 1) }

        await this.pages[page].drawLine(settings)

        if(col == 0)
        {
            settings.start = { x: this.width/2, y: this.height - this.heightStep*(row) }
            settings.end = { x: this.width/2, y: this.height - this.heightStep*(row + 1) }
            await this.pages[page].drawLine(settings)
        }
    }

    async drawData(index, data)
    {
        let col = index % this.columns
        let row = Math.floor((index % (this.rows * this.columns)) / 2)
        let page = Math.floor(index / (this.rows*this.columns))

        let positionLift = this.height - this.spacing - this.normalSize - this.heightStep * row

        this.pages[page].drawText(`UUID:\t${data.uuid}`, 
        {
            x: this.spacing + col*(this.width/2),
            y: positionLift,
            size: this.normalSize,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: this.normalSize
        })

        positionLift += -this.spacing - this.bigSize

        this.pages[page].drawText(`Part Name:\t${data.partName}`, 
        {
            x: this.spacing + col*(this.width/2),
            y: positionLift,
            size: this.bigSize,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: this.normalSize
        })

        positionLift += -this.spacing - this.bigSize

        this.pages[page].drawText(`Manufacturer:\t${data.manufacturer}`, 
        {
            x: this.spacing + col*(this.width/2),
            y: positionLift,
            size: this.normalSize,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: this.normalSize
        })

        positionLift += -this.spacing - this.normalSize

        this.pages[page].drawText(`Value:\t${data.value}`, 
        {
            x: this.spacing + col*(this.width/2),
            y: positionLift,
            size: this.normalSize,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: this.normalSize
        })

        positionLift += -this.spacing - this.normalSize

        this.pages[page].drawText(`Created at:\t${data.createdAt}`, 
        {
            x: this.spacing + col*(this.width/2),
            y: positionLift,
            size: this.normalSize,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: this.normalSize
        })

        positionLift += -this.spacing - this.normalSize

        this.pages[page].drawText(`Description:\t${data.description}`, 
        {
            x: this.spacing + col*(this.width/2),
            y: positionLift,
            size: this.normalSize,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            maxWidth: 200,
            lineHeight: this.normalSize
        })
    }

    async drawQR(index, uuid)
    {
        let col = index % this.columns
        let row = Math.floor((index % (this.rows * this.columns)) / 2)
        let page = Math.floor(index / (this.rows*this.columns))

        let qr = await QRCode.toDataURL(uuid)
        const qrImage = await this.pdf.embedPng(qr)
        const qrDims = await qrImage.scale(0.5)

        await this.pages[page].drawImage(qrImage, 
        {
            x: (this.width/2)*(col + 1) - qrDims.width - this.spacing + 5,
            y: this.height + this.spacing - (row + 1)*this.heightStep + 58,
            width: qrDims.width,
            height: qrDims.height,
        })
    }

    async drawLogo(index)
    {
        let col = index % this.columns
        let row = Math.floor((index % (this.rows * this.columns)) / 2)
        let page = Math.floor(index / (this.rows*this.columns))

        await this.pages[page].drawImage(this.logoImg, 
        {
            x: (this.width/2)*(col + 1) - this.logoDims.width - 3*this.spacing,
            y: this.height + 2*this.spacing - (row + 1)*this.heightStep + 95,
            width: this.logoDims.width,
            height: this.logoDims.height,
        })
    }

    async finish()
    {
        const pdfBytes = await this.pdf.save()
        const blob = new Blob([pdfBytes], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.href = url
        link.download = `onyks_bloodstone_label_${DateTime.now().setZone('Europe/Warsaw').toFormat('yyyy-MM-dd_HH-mm-ss')}.pdf`;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
}