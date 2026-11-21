import { i18n } from './localization';
import { html } from 'lit';
import router from '../router';
// import AvailabilityPlusMinus from '../components/AvailabilityPlusMinus.vue';
// import RemoveItemsDialog from '../components/RemoveItemsDialog.vue';
// import { defineCustomElement } from 'vue';

export const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms))

export const open_datasheet = (uuid) =>
{
    window.open('/files/' + uuid + '.pdf', '_blank');
};

// customElements.define('availability-plus-minus', defineCustomElement(AvailabilityPlusMinus));

const handle_remove = (event, row) =>
{
    event.currentTarget.dispatchEvent(new CustomEvent('remove-element', { detail: row, bubbles: true, composed: true }))
}

export const elements_table_expand_template = (row) =>
{
    return html`
        <style>
            .btn
            {
                min-width: 100px;
            }
        </style>
        <onyks-container gap="m" type="stack" class="elements-table">
            <onyks-container type="group" gap="m">
                <onyks-button class="btn" background="blue" @click=${() => router.push({ name: 'element-edit', params: { uuid: row?.uuid } })} size="s">${i18n.global.t('common.edit')}</onyks-button>
                <onyks-button class="btn" background="yellow" @click=${() => router.push({ name: 'element-duplicate', params: { uuid: row?.uuid } })} size="s">${i18n.global.t('common.duplicate')}</onyks-button>
                <onyks-button class="btn" background="red" size="s" @click=${(e) => handle_remove(e, row)}>${i18n.global.t('common.remove')}</onyks-button>
                <onyks-button class="btn" background="gray" size="s" @click=${() => router.push({ name: 'element-details', params: { uuid: row?.uuid } })}>${i18n.global.t('common.details')}</onyks-button>
            </onyks-container>
            <onyks-container style="grid-template-columns: 500px minmax(0, 1fr);" type="grid" gap="m">
                <onyks-container type="stack" gap="m" cols="1">
                    <onyks-header underline>${i18n.global.t('common.uuid')}</onyks-header>
                    <onyks-text>${row.uuid}</onyks-text>
                    <onyks-header underline>${i18n.global.t('elements.availability')}</onyks-header>
                    <onyks-text>${row.availability || i18n.global.t('common.no_data')}</onyks-text>
                    <onyks-header underline>${i18n.global.t('suppliers.suppliers_codes')}</onyks-header>
                    ${Object.keys(row.suppliers || {}).length > 0 ? html`
                        <onyks-table size="s" style="height: 200px; width: 100%;" .columns=${[{ label: i18n.global.t('suppliers.supplier_name'), key: 'name' }, { label: i18n.global.t('suppliers.suppliers_code'), key: 'value' }]} .data=${Object.values(row.suppliers)}></onyks-table>
                    ` : ''}
                    ${Object.keys(row.suppliers || {}).length === 0 ? html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>` : ''}
                
                </onyks-container>
                <onyks-container type="stack" gap="m" cols="1">
                    <onyks-header underline>${i18n.global.t('elements.description')}</onyks-header>
                    ${row.description != '' ? html`<onyks-text size="s" style="text-align: justify;">${row.description}</onyks-text>` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}
                
                    <onyks-header underline>${i18n.global.t('common.datasheets')}</onyks-header>
                    ${row.datasheets && row.datasheets.length > 0 ? html`
                        <onyks-container type="group" gap="m">
                            ${row.datasheets.map(sheet => html`<onyks-tag icon="F756" size="s" @click=${() => open_datasheet(sheet.uuid)} background="indigo">${sheet.name}</onyks-tag>`)}
                        </onyks-container>
                    ` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}

                    <onyks-header underline>${i18n.global.t('common.tags')}</onyks-header>
                    ${row.tags && row.tags.length > 0 ? html`
                        <onyks-container type="group" gap="m">
                            ${row.tags.map(tag => html`<onyks-tag size="s" background="teal">${tag}</onyks-tag>`)}
                        </onyks-container>
                    ` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}
                </onyks-container>
            </onyks-container>

            <onyks-container style="grid-template-columns: 500px minmax(0, 1fr);" type="grid" gap="m">
                <onyks-container type="stack" gap="s">
                    <onyks-header underline>${i18n.global.t('elements.symbol')}</onyks-header>
                    ${row.library_path != '' && row.library_reference != '' ? html`<onyks-path style="width: 100%; max-width: 100%; min-width: 0; overflow: hidden;" .content=${(row.library_path.split('/')).concat(row.library_reference)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}
                    
                    <onyks-header underline>${i18n.global.t('elements.footprint_no_1')}</onyks-header>
                    ${row.footprint_path_1 != '' && row.footprint_reference_1 != '' ? html`<onyks-path style="width: 100%; max-width: 100%; min-width: 0; overflow: hidden;" .content=${row.footprint_path_1.split('/').concat(row.footprint_reference_1)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}

                </onyks-container>

                <onyks-container type="stack" gap="s">
                    <onyks-header underline>${i18n.global.t('elements.footprint_no_2')}</onyks-header>
                    ${row.footprint_path_2 != '' && row.footprint_reference_2 != '' ? html`<onyks-path style="width: 100%; max-width: 500px; min-width: 0; overflow: hidden;" .content=${row.footprint_path_2.split('/').concat(row.footprint_reference_2)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}
                    <onyks-header underline>${i18n.global.t('elements.footprint_no_3')}</onyks-header>
                    ${row.footprint_path_3 != '' && row.footprint_reference_3 != '' ? html`<onyks-path style="width: 100%; max-width: 500px; min-width: 0; overflow: hidden;" .content=${row.footprint_path_3.split('/').concat(row.footprint_reference_3)} size="s"></onyks-path>` : html`<onyks-text size="s">${i18n.global.t('common.no_data')}</onyks-text>`}
                </onyks-container>
            </onyks-container>
        </onyks-container>
    `
}
