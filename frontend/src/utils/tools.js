import { i18n } from './localization';
import { html } from 'lit';
import router from '../router';
import AvailabilityPlusMinus from '../components/AvailabilityPlusMinus.vue';
import { defineCustomElement } from 'vue';



const AvailabilityPlusMinusElement = defineCustomElement(AvailabilityPlusMinus);

customElements.define('availability-plus-minus', AvailabilityPlusMinusElement);

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
                    
                    <onyks-header level="6">${i18n.global.t('elements.availability')}</onyks-header>
                    <availability-plus-minus></availability-plus-minus>

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
                            ${row.datasheets.map(sheet => html`<onyks-tag icon="F756" size="s" @click=${() => open_datasheet(sheet.uuid)} background="blue">${sheet.name}</onyks-tag>`)}
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
