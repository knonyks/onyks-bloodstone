import { degrees, PDFDocument, rgb, StandardFonts, PageSizes } from 'pdf-lib';
import QRCode from 'qrcode'
import { DateTime } from "luxon";
import { services } from './api';
import { reactive } from 'vue'
import { ref } from 'vue';
import { watch } from 'vue';
import { computed } from 'vue';
import { unref } from 'vue';
import { html } from 'lit';
import { i18n } from './localization';

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
`, formatData = (item) => item) =>
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
        data.value.map((item) => formatData(item))
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
        data.value.map((item) => formatData(item))
        if (index == null) return;
        page.value = index;
    }

    const search = async () =>
    {
        page.value = 1
        const result = await service.list(page.value, limit.value, searchPhrase.value, sortBy.value, sortDesc.value)
        data.value = result?.data?.items ?? []
        data.value.map((item) => formatData(item))
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
            // error.value = e?.response?.data?.detail?.error_code || e?.message || 'An error occurred'
            error.value = i18n.global.t(`error_codes.${e?.response?.data?.detail?.error_code}`) || e?.message || 'An error occurred'
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
            // error.value = e?.response?.data?.detail?.error_code || e?.message || 'An error occurred'
            error.value = i18n.global.t(`error_codes.${e?.response?.data?.detail?.error_code}`) || e?.message || 'An error occurred'
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

export const useLabels = () =>
{
    const columns = ref(2)
    const rows = ref(6)
    const data = ref([])
    const pdf = ref(null)
    const pages = ref([])
    const width = ref(PageSizes.A4[0])
    const height = ref(PageSizes.A4[1])
    const spacing = ref(5)
    const size = ref(8)

    const init = async () =>
    {
        pdf.value = await PDFDocument.create()
        for(let i=0; i<Math.ceil(data.value.length/(columns.value*rows.value)); i++)
        {
            await pdf.value.addPage(PageSizes.A4)
        }
        pages.value = await pdf.value.getPages()
    }

    const __drawBorder = async (index) =>
    {
        let settings = 
        {
            thickness: 1,
            color: rgb(0, 0, 0),
            opacity: 0.2,
            dashArray: [10, 20]
        }
        let col = index % columns.value
        let row = Math.floor((index % (rows.value * columns.value)) / columns.value)
        let page = Math.floor(index / (rows.value*columns.value))

        // is the end of the page?
        if(row != rows.value - 1)
        {
            if(col == 0)
            {
                settings.start = { x: 0 , y:  height.value - (height.value / rows.value)*(row + 1) }
                settings.end = { x: width.value/2, y:  height.value - (height.value / rows.value)*(row + 1) }
                await pages.value[page].drawLine(settings)
            }
            else
            {
                settings.start = { x: width.value/2 , y:  height.value - (height.value / rows.value)*(row + 1) }
                settings.end = { x: width.value, y:  height.value - (height.value / rows.value)*(row + 1) }
                await pages.value[page].drawLine(settings)
            }
        }

        // is the right edge of the page?
        if(col == 0)
        {
            settings.start = { x: width.value/2 , y:  height.value - (height.value / rows.value)*(row + 1) }
            settings.end = { x: width.value/2, y:  height.value - (height.value / rows.value)*row}
            await pages.value[page].drawLine(settings)
        }
    }

    const drawBorders = async () =>
    {
        for(let i=0; i<data.value.length; i++)
        {
            await __drawBorder(i)
        }
    }
    
    const __drawQR = async (index, uuid) =>
    {
        let col = index % columns.value
        let row = Math.floor((index % (rows.value * columns.value)) / columns.value)
        let page = Math.floor(index / (rows.value*columns.value))

        let qr = await QRCode.toDataURL(uuid)
        const qrImage = await pdf.value.embedPng(qr)
        const qrDims = await qrImage.scale(0.5)

        await pages.value[page].drawImage(qrImage, 
        {
            x: (width.value/2)*(col + 1) - qrDims.width,
            y: height.value - qrDims.height - row*(height.value / rows.value),
            width: qrDims.width,
            height: qrDims.height,
        })
    }

    const __cutText = (text, maxLength) =>
    {
        if(!text) return ''
        if(text.length <= maxLength) return text
        return text.substring(0, maxLength) + '...'
    }

    const drawQR = async () =>
    {
        for(let i=0; i<data.value.length; i++)
        {
            await __drawQR(i, data.value[i].uuid)
        }
    }

    // const drawLogo = async (index) =>
    // {
    //     let col = index % columns.value
    //     let row = Math.floor((index % (rows.value * columns.value)) / rows.value)
    //     let page = Math.floor(index / (rows.value*columns.value))

    //     await pages.value[page].drawImage(logoImg.value, 
    //     {
    //         x: (width.value/2)*(col + 1) - logoDims.value.width - 3*spacing.value,
    //         y: height.value + 2*spacing.value - (row + 1)*heightStep.value + 95,
    //         width: logoDims.value.width,
    //         height: logoDims.value.height,
    //     })
    // }

    // const addLogo = async (logoUrl) =>
    // {
    //     logoBytes.value = await fetch(logoUrl).then((res) => res.arrayBuffer())
    //     logoImg.value = await pdf.value.embedPng(logoBytes.value)
    //     logoDims.value = await logoImg.value.scale(0.01)
    // }

    const __drawData = async (index, data) =>
    {
        const toWinAnsi = (text) => String(text ?? '')
            .replace(/[łŁ]/g, (character) => character === 'ł' ? 'l' : 'L')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')

        let col = index % columns.value
        let row = Math.floor((index % (rows.value * columns.value)) / columns.value)
        let page = Math.floor(index / (rows.value*columns.value))

        let positionLift = height.value - spacing.value - size.value - (height.value / rows.value) * row
        const helveticaBoldFont = await pdf.value.embedFont(StandardFonts.HelveticaBold);


        pages.value[page].drawText(toWinAnsi(i18n.global.t('other.labels.uuid')), 
        {
            x: spacing.value + col*(width.value/2),
            y: positionLift,
            size: size.value,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: size.value,
            font: helveticaBoldFont,
            bold: true
        })

        
        pages.value[page].drawText(toWinAnsi(data.uuid), 
        {
            x: spacing.value + col*(width.value/2) + 55,
            y: positionLift,
            size: size.value,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: size.value
        })

        positionLift += -spacing.value - size.value

        pages.value[page].drawText(toWinAnsi(i18n.global.t('other.labels.partName')), 
        {
            x: spacing.value + col*(width.value/2),
            y: positionLift,
            size: size.value,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: size.value,
            font: helveticaBoldFont,
        })

        pages.value[page].drawText(toWinAnsi(data.partName), 
        {
            x: spacing.value + col*(width.value/2) + 55,
            y: positionLift,
            size: size.value,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: size.value
        })

        positionLift += -spacing.value - size.value

        pages.value[page].drawText(toWinAnsi(i18n.global.t('other.labels.manufacturer')), 
        {
            x: spacing.value + col*(width.value/2),
            y: positionLift,
            size: size.value,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: size.value,
            font: helveticaBoldFont
        })

        pages.value[page].drawText(toWinAnsi(data.manufacturer), 
        {
            x: spacing.value + col*(width.value/2) + 55,
            y: positionLift,
            size: size.value,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: size.value
        })


        positionLift += -spacing.value - size.value

        pages.value[page].drawText(toWinAnsi(i18n.global.t('other.labels.value')), 
        {
            x: spacing.value + col*(width.value/2),
            y: positionLift,
            size: size.value,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: size.value,
            font: helveticaBoldFont
        })

        pages.value[page].drawText(toWinAnsi(__cutText(data.value, 35)), 
        {
            x: spacing.value + col*(width.value/2) + 55,
            y: positionLift,
            size: size.value,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            lineHeight: size.value
        })

        positionLift += -spacing.value - size.value

        pages.value[page].drawText(toWinAnsi(i18n.global.t('other.labels.description')), 
        {
            x: spacing.value + col*(width.value/2),
            y: positionLift,
            size: size.value,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            maxWidth: 200,
            lineHeight: size.value,
            font: helveticaBoldFont
        })

        positionLift += -spacing.value - size.value

        pages.value[page].drawText(toWinAnsi(__cutText(data.description, 512-128)), 
        {
            x: spacing.value + col*(width.value/2),
            y: positionLift,
            size: size.value,
            color: rgb(0, 0, 0),
            rotate: degrees(0),
            maxWidth: 205,
            lineHeight: size.value
        })
    }

    const drawData = async () =>
    {
        for(let i=0; i<data.value.length; i++)
        {
            await __drawData(i, data.value[i])
        }
    }

    const finish = async () =>
    {
        const pdfBytes = await pdf.value.save()
        const blob = new Blob([pdfBytes], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.href = url
        link.download = `labels_${DateTime.now().setZone('Europe/Warsaw').toFormat('yyyy-MM-dd_HH-mm-ss')}.pdf`;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    const generate = async (newData) =>
    {
        data.value = newData
        await init()
        await drawBorders()
        await drawQR()
        await drawData()
        await finish()
    }

    return { generate }
}