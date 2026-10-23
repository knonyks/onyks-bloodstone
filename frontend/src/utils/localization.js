import { createI18n } from 'vue-i18n'


const en = 
{
    dashboard:
    {
        title: 'Dashboard',
        overview: 'Overview',
        lastAddedElement: 'Last added element',
        partName: 'Part name',
        manufacturer: 'Manufacturer',
        table: 'Table',
        createdAt: 'Created at',
        repository: 'Repository',
        symbolsFiles: 'Symbols files',
        footprintsFiles: 'Footprints files',
        symbols: 'Symbols',
        footprints: 'Footprints',
        elements: 'Elements',
        tables: 'Tables',
        manufacturers: 'Manufacturers',
        suppliers: 'Suppliers',
        noTables: 'There are no tables to show.',
        noManufacturers: 'There are no manufacturers to show.'
    },
    warningAlert:
    {
        title: 'This software is in development. It can be unstable.'
    }
}

const pl = 
{
    views:
    {
        RepositoryView:
        {
            title: 'Repozytorium'
        },
        DashboardView:
        {
            title: 'Panel główny',
            noData: 'Brak danych',
            overview: 'Przegląd',
            lastAddedElement: 'Ostatnio dodany element',
            partName: 'Nazwa części',
            manufacturer: 'Producent',
            table: 'Tabela',
            createdAt: 'Utworzono',
            repository: 'Repozytorium',
            symbolsFiles: 'Pliki symboli',
            footprintsFiles: 'Pliki footprintów',
            symbols: 'Symbole',
            footprints: 'Footprinty',
            elements: 'Elementy',
            tables: 'Tabele',
            manufacturers: 'Producenci',
            suppliers: 'Dostawcy',
            noTables: 'Brak tabel do wyświetlenia.',
            noManufacturers: 'Brak producentów do wyświetlenia.'
        },
        ManagerView:
        {
            nav:
            {
                dashboard: 'Panel główny',
                management: 'Zarządzanie',
                repository: 'Repozytorium',
                settings: 'Ustawienia',
                admin: 'Panel Admina'
            }
        },
        ManagementView:
        {
            title: 'Zarządzanie',
            expandPage: 'Rozszerz stronę',
            titles:
            {
                elements: 'Elementy',
                tables: 'Tabele',
                manufacturers: 'Producenci',
                suppliers: 'Dostawcy'
            },
            btns:
            {
                add: 'Dodaj',
                edit: 'Edytuj',
                duplicate: 'Duplikuj',
                delete: 'Usuń',
                details: 'Szczegóły',
                labels: 'Etykiety',
                scan: 'Skanuj'
            },
            columns:
            {
                selected: 'Wybrano',
                id: 'ID',
                name: 'Nazwa',
                createdAt: 'Utworzono',
                partName: 'Nazwa części',
                manufacturer: 'Producent',
                table: 'Tabela',
                symbol: 'Symbol',
                availability: 'Dostępność',
                value: 'Wartość',
                description: 'Opis',
                tags: 'Tagi',
                uuid: 'UUID',
                suppliers: 'Dostawcy',
                footprints: 'Footprinty',
                datasheets: 'Karty danych',
                footprintNo1: 'Footprint nr 1',
                footprintNo2: 'Footprint nr 2',
                footprintNo3: 'Footprint nr 3',
                noData: 'Brak danych'
            },
            dialogs:
            {
                suppliers:
                {
                    add: 'Dodaj dostawcę',
                    edit: 'Edytuj dostawcę',
                    delete: 'Usuń dostawcę'
                },
                manufacturers:
                {
                    add: 'Dodaj producenta',
                    edit: 'Edytuj producenta',
                    delete: 'Usuń producenta'
                },
                tables:
                {
                    add: 'Dodaj tabelę',
                    edit: 'Edytuj tabelę',
                    delete: 'Usuń tabelę'
                }
            },
            toasts:
            {
                supplierAdded: 'Dostawca został dodany pomyślnie.',
                supplierEdited: 'Dostawca został edytowany pomyślnie.',
                manufacturerAdded: 'Producent został dodany pomyślnie.',
                manufacturerEdited: 'Producent został edytowany pomyślnie.',
                tableAdded: 'Tabela została dodana pomyślnie.',
                tableEdited: 'Tabela została edytowana pomyślnie.'
            }
        },
        ElementView:
        {
            titles:
            {
                details: 'Szczegóły elementu',
                create: 'Dodaj element',
                edit: 'Edytuj element',
                duplicate: 'Duplikuj element'
            }
        }
    },
    components:
    {
        WarningAlert:
        {
            title: 'To oprogramowanie jest w fazie rozwoju. Może zawierać błędy.'
        },
        RepositoryExplorer:
        {
            refresh: 'Odśwież'
        },
        BasicSearch:
        {
            search: 'Szukaj...'
        },
        BasicTable:
        {
            selected: 'Wybrano',
            total: 'Wszystkich'
        },
        AddItemDialog:
        {
            subtitle: 'Wprowadź nazwę poniżej:',
        },
        EditItemDialog:
        {
            subtitle1: 'Obecna nazwa:',
            subtitle2: 'Wprowadź nową nazwę poniżej:',
        },
        DeleteItemsDialog:
        {
            subtitle1: 'Próbujesz usunać {count} obiekt.',
            subtitle2: 'Próbujesz usunąć {count} obiekty:',
            confirm: 'Potwierdź',
            deleted: 'Usunięto { counter } z { length } obiektów pomyślnie.',   
            result: 'Wynik',
            someItemsCouldNotBeDeleted: 'Niektóre obiekty nie mogły zostać usunięte:'
        }
    },
    error_codes:
    {
        INVALID_DATA_OR_SUPPLIER_ALREADY_EXISTS: 'Nieprawidłowe dane lub taki dostawca już istnieje.',
        EMPTY_SUPPLIER_NAME: 'Nazwa dostawcy nie może być pusta.',
        ITEM_DELETE_SUCCESS: 'Pomyślnie usunięto.',
        SUPPLIER_NOT_FOUND: 'Dostawca nie został znaleziony.',
        INVALID_DATA_OR_MANUFACTURER_ALREADY_EXISTS: 'Nieprawidłowe dane lub taki producent już istnieje.',
        EMPTY_MANUFACTURER_NAME: 'Nazwa producenta nie może być pusta.',
        INVALID_DATA_OR_TABLE_ALREADY_EXISTS: 'Nieprawidłowe dane lub taka tabela już istnieje.',
        TABLE_EMPTY_NAME: 'Nazwa tabeli nie może być pusta.',
        TABLE_NOT_EMPTY: 'Tabela nie jest pusta.'
    }
    // pages:
    // {
    //     titles:
    //     {
    //         dashboard: 'Panel główny',
    //         management: 'Zarządzanie',
    //         repository: 'Repozytorium',
    //         settings: 'Ustawienia',
    //         admin: 'Panel Admina',
    //         createElement: 'Dodaj element',
    //         elementDetails: 'Szczegóły elementu',
    //         editElement: 'Edytuj element',
    //         duplicateElement: 'Duplikuj element'
    //     }
    // },
    // nav:
    // {
    //     dashboard: 'Panel główny',
    //     management: 'Zarządzanie',
    //     repository: 'Repozytorium',
    //     settings: 'Ustawienia',
    //     admin: 'Panel Admina'
    // },
    // dashboard:
    // {
    //     title: 'Panel główny',
    //     none: 'Brak',
    //     overview: 'Przegląd',
    //     lastAddedElement: 'Ostatnio dodany element',
    //     partName: 'Nazwa części',
    //     manufacturer: 'Producent',
    //     table: 'Tabela',
    //     createdAt: 'Utworzono',
    //     repository: 'Repozytorium',
    //     symbolsFiles: 'Pliki symboli',
    //     footprintsFiles: 'Pliki footprintów',
    //     symbols: 'Symbole',
    //     footprints: 'Footprinty',
    //     elements: 'Elementy',
    //     tables: 'Tabele',
    //     manufacturers: 'Producenci',
    //     suppliers: 'Dostawcy',
    //     noTables: 'Brak tabel do wyświetlenia.',
    //     noManufacturers: 'Brak producentów do wyświetlenia.'
    // },
    // repository:
    // {
    //     title: 'Repozytorium'
    // },
}

const datetimeFormats = 
{
    'en-US': 
    {
        short: {
            year: 'numeric', month: 'short', day: 'numeric'
        },
        long: {
            year: 'numeric', month: 'long', day: 'numeric', weekday: 'long', hour: 'numeric', minute: 'numeric', second: 'numeric'
        }
    },
    'en-GB': 
    {
        short: {
            year: 'numeric', month: 'short', day: 'numeric'
        },
        long: {
            year: 'numeric', month: 'long', day: 'numeric', weekday: 'long', hour: 'numeric', minute: 'numeric', second: 'numeric'
        }
    },
    'pl-PL': 
    {
        short: 
        {
            year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric'
        },
        long: {
            year: 'numeric', month: 'long', day: 'numeric', weekday: 'long', hour: 'numeric', minute: 'numeric', second: 'numeric'
        }
    }
}

export const i18n = createI18n(
{
    locale: 'pl-PL',
    fallbackLocale: 'pl-PL',
    messages: 
    {
        en: en,
        'pl-PL': pl
    },
    datetimeFormats: datetimeFormats
},)
