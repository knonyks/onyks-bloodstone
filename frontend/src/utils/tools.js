import { degrees, PDFDocument, rgb, StandardFonts, PageSizes } from 'pdf-lib';
import QRCode from 'qrcode'
import { DateTime } from "luxon";
import { services } from './api';
import { reactive } from 'vue'
import { ref } from 'vue';
import { watch } from 'vue';
import { computed } from 'vue';
import { unref } from 'vue';
import { i18n } from './localization';
import { html } from 'lit';
import router from '@/router';
import RemoveItemsDialog from '@/components/RemoveItemsDialog.vue';
import { createApp } from 'vue';
import { useRemoveItemsDialog } from '@/composables/useRemoveItemsDialog';

export const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

export const open_datasheet = (uuid) =>
{
    window.open('/files/' + uuid + '.pdf', '_blank');
};

export const elements_table_expand_template = (row) =>
{
    return html`
        <onyks-container gap="m" type="stack" class="elements-table">
            <onyks-container type="group" gap="m">
                <onyks-tag style="cursor: pointer; width: 75px; text-align: center;" background="blue" icon="" style="width: 75px; text-align: center;" @click=${() => router.push(`elements/edit/${row?.uuid}`)}>${i18n.global.t('common.edit')}</onyks-tag>
                <onyks-tag style="cursor: pointer; width: 75px; text-align: center; " background="yellow" icon="" style="width: 75px; text-align: center;" @click=${() => router.push(`elements/duplicate/${row?.uuid}`)}>${i18n.global.t('common.duplicate')}</onyks-tag>
                <onyks-tag style="cursor: pointer; width: 75px; text-align: center;" background="red" icon="" style="width: 75px; text-align: center;" @click=${
                    (event) =>
                    {
                        event.currentTarget.dispatchEvent(new CustomEvent('remove-element', { detail: row, bubbles: true, composed: true }))
                    }
                }>${i18n.global.t('common.remove')}</onyks-tag>
                <onyks-tag style="cursor: pointer; width: 75px; text-align: center;" background="green" icon="" style="width: 75px; text-align: center;" @click=${() => router.push(`elements/details/${row?.uuid}`)}>${i18n.global.t('common.details')}</onyks-tag>
            </onyks-container>
        
            <onyks-container style="grid-template-columns: 500px minmax(0, 1fr);" type="grid" gap="m">
                <onyks-container type="stack" gap="m" cols="1"> 
                    
                    <onyks-header level="6">${i18n.global.t('elements.uuid')}</onyks-header>
                    <onyks-text size="s">${row?.uuid}</onyks-text>

                    <onyks-header level="6">${i18n.global.t('suppliers.suppliers_codes')}</onyks-header>

                    ${Object.keys(row.suppliers || {}).length > 0 ? html`
                        <onyks-table size="s" style="height: 200px; width: 100%;" .columns=${[{ label: i18n.global.t('suppliers.supplier_name'), key: 'name' }, { label: i18n.global.t('suppliers.suppliers_code'), key: 'value' }]} .data=${Object.values(row.suppliers)}></onyks-table>
                    ` : ''}
                    ${Object.keys(row.suppliers || {}).length === 0 ? html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>` : ''}
                



                </onyks-container>
                <onyks-container type="stack" gap="m">
                     <onyks-header level="6">${i18n.global.t('elements.description')}</onyks-header>
                    ${row.description != '' ? html`<onyks-text size="s" style="text-align: justify;">${row.description}</onyks-text>` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}
                
                    <onyks-header level="6">${i18n.global.t('common.datasheets')}</onyks-header>
                    ${row.datasheets && row.datasheets.length > 0 ? html`
                        <onyks-container type="group" gap="m">
                            ${row.datasheets.map(sheet => html`<onyks-tag size="s" @click=${() => open_datasheet(sheet.uuid)} background="blue">${sheet.name}</onyks-tag>`)}
                        </onyks-container>
                    ` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}

                    <onyks-header level="6">${i18n.global.t('common.tags')}</onyks-header>
                    ${row.tags && row.tags.length > 0 ? html`
                        <onyks-container type="group" gap="m">
                            ${row.tags.map(tag => html`<onyks-tag size="s"background="yellow">${tag}</onyks-tag>`)}
                        </onyks-container>
                    ` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}
                </onyks-container>
            </onyks-container>
            
            <onyks-container style="grid-template-columns: 500px minmax(0, 1fr);" type="grid" gap="m">
                <onyks-container type="stack" gap="m">
                                        <onyks-header level="6">${i18n.global.t('elements.symbol')}</onyks-header>
                    ${row.library_path != '' && row.library_reference != '' ? html`<onyks-path style="width: 100%; max-width: 100%; min-width: 0; overflow: hidden;" .content=${(row.library_path.split('/')).concat(row.library_reference)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}
                    
                    <onyks-header level="6">${i18n.global.t('elements.footprint_no_1')}</onyks-header>
                    ${row.footprint_path_1 != '' && row.footprint_reference_1 != '' ? html`<onyks-path style="width: 100%; max-width: 100%; min-width: 0; overflow: hidden;" .content=${row.footprint_path_1.split('/').concat(row.footprint_reference_1)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}

                </onyks-container>

                <onyks-container type="stack" gap="m">
                    <onyks-header level="6">${i18n.global.t('elements.footprint_no_2')}</onyks-header>
                    ${row.footprint_path_2 != '' && row.footprint_reference_2 != '' ? html`<onyks-path style="width: 100%; max-width: 500px; min-width: 0; overflow: hidden;" .content=${row.footprint_path_2.split('/').concat(row.footprint_reference_2)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}
                    <onyks-header level="6">${i18n.global.t('elements.footprint_no_3')}</onyks-header>
                    ${row.footprint_path_3 != '' && row.footprint_reference_3 != '' ? html`<onyks-path style="width: 100%; max-width: 500px; min-width: 0; overflow: hidden;" .content=${row.footprint_path_3.split('/').concat(row.footprint_reference_3)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}
                </onyks-container>
            </onyks-container>

        </onyks-container>
    `
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
