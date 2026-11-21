import { createI18n } from 'vue-i18n'
import en from './languages/en.json'
import pl from './languages/pl.json'

export const SUPPORT_LOCALES = ['pl', 'en'];
export const DEFAULT_LOCALE = 'pl';

export function set_language(locale) 
{
    i18n.global.locale.value = locale;
    document.querySelector('html').setAttribute('lang', locale);
    localStorage.setItem('lang', locale);
}

export function get_preferred_locale() 
{
    const saved_locale = localStorage.getItem('lang');
    if (saved_locale && SUPPORT_LOCALES.includes(saved_locale)) 
    {
        return saved_locale;
    }

    const browser_locale = navigator.language;
    if (SUPPORT_LOCALES.includes(browser_locale)) 
    {
        return browser_locale;
    }

    const baseLang = browser_locale.split('-')[0];
    if (baseLang === 'pl') return 'pl';
    if (baseLang === 'en') return 'en-US';

    return DEFAULT_LOCALE;
}

function polishPluralizationRule(choice, choicesLength) 
{
    if (choice === 0) 
    {
        return 0
    }

    if (choice === 1) 
    {
        return 1
    }

    const teen = choice % 100 > 10 && choice % 100 < 20
    if (!teen && choice % 10 >= 2 && choice % 10 <= 4) 
    {
        return 2
    }

    return 3
}

const datetimeFormats = 
{
    'en': 
    {
        short: {
            year: 'numeric', month: 'short', day: 'numeric'
        },
        long: {
            year: 'numeric', month: 'long', day: 'numeric', weekday: 'long', hour: 'numeric', minute: 'numeric', second: 'numeric'
        }
    },
    'pl': 
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

export const i18n = createI18n({
    legacy: false,
    locale: DEFAULT_LOCALE,
    pluralRules: 
    {
        pl: polishPluralizationRule
    },
    fallbackLocale: {
        'en': ['en'],
        default: ['pl']
    },
    messages: {
        en,
        pl
    },
    datetimeFormats: datetimeFormats
})
