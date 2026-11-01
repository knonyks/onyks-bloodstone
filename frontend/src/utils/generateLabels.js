import { degrees, PDFDocument, rgb, StandardFonts, PageSizes } from 'pdf-lib';
import QRCode from 'qrcode'
import { DateTime } from "luxon";
import { ref } from 'vue';
import { i18n } from './localization';

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


    pages.value[page].drawText(toWinAnsi(i18n.global.t('common.uuid')), 
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

    pages.value[page].drawText(toWinAnsi(i18n.global.t('elements.part_name')), 
    {
        x: spacing.value + col*(width.value/2),
        y: positionLift,
        size: size.value,
        color: rgb(0, 0, 0),
        rotate: degrees(0),
        lineHeight: size.value,
        font: helveticaBoldFont,
    })

    pages.value[page].drawText(toWinAnsi(data.part_name), 
    {
        x: spacing.value + col*(width.value/2) + 55,
        y: positionLift,
        size: size.value,
        color: rgb(0, 0, 0),
        rotate: degrees(0),
        lineHeight: size.value
    })

    positionLift += -spacing.value - size.value

    pages.value[page].drawText(toWinAnsi(i18n.global.t('elements.manufacturer')), 
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

    pages.value[page].drawText(toWinAnsi(i18n.global.t('elements.value')), 
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

    pages.value[page].drawText(toWinAnsi(i18n.global.t('elements.description')), 
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

export const labels_generate = async (newData) =>
{
    data.value = newData
    await init()
    await drawBorders()
    await drawQR()
    await drawData()
    await finish()
}