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
    common:
    {
        last_added_element: 'Ostatnio dodany element',
        symbols_files: 'Pliki symboli',
        footprints_files: 'Pliki footprintów',
        symbols: 'Symbole',
        footprints: 'Footprinty',
        dashboard: 'Panel główny',
        repository: 'Repozytorium',
        management: 'Zarządzanie',
        settings: 'Ustawienia',
        admin_panel: 'Panel Admina',
        manufacturers: 'Producenci',
        elements: 'Elementy',
        suppliers: 'Dostawcy',
        tables: 'Tabele',
        overview: 'Przegląd',
        add: 'Dodaj',
        remove: 'Usuń',
        edit: 'Edytuj',
        reset: 'Resetuj',
        import: 'Importuj',
        total: 'Łącznie',
        selected: 'Wybrane',
        search_placeholder: 'Szukaj...',
        no_data: 'Brak danych',
        no_tables: 'Brak tabel do wyświetlenia',
        no_manufacturers: 'Brak producentów do wyświetlenia',
        id: 'Identyfikator',
        created_at: 'Utworzono',
        refresh: 'Odśwież',
        user_list: 'Lista użytkowników',
        backup: 'Kopia zapasowa',
        software_in_development: 'Oprogramowanie jest w fazie rozwoju - może być niestabilne',
        enter_name_below: 'Wprowadź nazwę poniżej:',
        enter_new_name_below: 'Wprowadź nową nazwę poniżej:',
        you_editing: "Edytujesz ,,{0}''.",
        trying_to_remove_1: 'Próbujesz usunąć {count} obiekt.',
        trying_to_remove_2: 'Próbujesz usunąć {count} obiekty:',
        confirm: 'Potwierdź',
        removed_x_of_y: 'Usunięto { 0 } z { 1 } obiektów pomyślnie.',   
        removing_result: 'Wynik usuwania',
        some_items_could_not_be_deleted: 'Niektóre obiekty nie mogły zostać usunięte:',
        expand_page: 'Rozszerz stronę',
        uuid: 'Identyfikator',
        details: 'Szczegóły',
        labels: 'Etykiety',
        scan: 'Skanuj',
        duplicate: 'Duplikuj',
        back: 'Powrót',
        create: 'Utwórz',
        edit: 'Edytuj',
        duplicate: 'Duplikuj',
        select: 'Wybierz',
        reset: 'Resetuj',
        datasheets: 'Karty katalogowe',
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
        TABLE_NOT_EMPTY: 'Tabela nie jest pusta.',
        INVALID_DATA_OR_ELEMENT_ALREADY_EXISTS: 'Nieprawidłowe dane wejściowe lub taki element już istnieje.'
    },
    suppliers:
    {
        name: 'Nazwa',
        add: 'Dodaj dostawcę',
        edit: 'Edytuj dostawcę',
        delete: 'Usuń dostawcę',
        added: 'Dostawca został dodany',
        edited: 'Dostawca został zaktualizowany',
        supplier_name: 'Nazwa dostawcy',
        suppliers_code: 'Kod dostawcy'
    },
    manufacturers:
    {
        name: 'Nazwa',
        add: 'Dodaj producenta',
        edit: 'Edytuj producenta',
        delete: 'Usuń producenta',
        added: 'Producent został dodany',
        edited: 'Producent został zaktualizowany',
    },
    tables:
    {
        name: 'Nazwa',
        add: 'Dodaj tabelę',
        edit: 'Edytuj tabelę',
        delete: 'Usuń tabelę',
        added: 'Tabela została dodana',
        edited: 'Tabela została zaktualizowana',
    },
    elements:
    {
        uuid: 'UUID',
        part_name: 'Nazwa',
        manufacturer: 'Producent',
        table: 'Tabela',
        value: 'Wartość',
        description: 'Opis',
        availability: 'Dostępność',
        create: 'Utwórz element',
        edit: 'Edytuj element',
        duplicate: 'Duplikuj element',
        remove: 'Usuń element',
        details: 'Szczegóły elementu',
        creating: 'Tworzenie elementu...',
        duplicating: 'Duplikowanie elementu...',
        editing: 'Edytowanie elementu...',
        created_successfully: 'Element został utworzony pomyślnie.',
        duplicated_successfully: 'Element został zduplikowany pomyślnie.',
        edited_successfully: 'Element został zaktualizowany pomyślnie.',
        basic_information: 'Podstawowe informacje',
        selected: 'Wybrano',
        none: 'Brak',
        symbols_and_footprints: 'Symbole i wzór montażowy',
        symbol: 'Symbol',
        footprint_no_1: 'Wzór montażowy nr 1',
        footprint_no_2: 'Wzór montażowy nr 2',
        footprint_no_3: 'Wzór montażowy nr 3',
        select_symbol: 'Wybierz symbol',
        select_footprint_no: 'Wybierz wzór montażowy nr {0}',
        please_select_symbol: 'Proszę wybrać symbol',
        please_select_footprint: 'Proszę wybrać wzór montażowy',
        other_details: 'Pozostałe szczegóły',
        suppliers_codes: 'Kody dostawców',
        no_suppliers_codes_defined: 'Brak zdefiniowanych kodów dostawców'
    }
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
