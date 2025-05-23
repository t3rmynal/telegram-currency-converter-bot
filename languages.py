# languages.py
LANGUAGES = ["en", "ru"]

MESSAGES = {
    "en": {
        "start": "Welcome! Please choose your language:",
        "choose_language": "Please choose your language:",
        "language_selected": "Language selected: English.",
        "menu": "Main menu:",
        "select_platform": "Select platform:",
        "fiat": "Fiat",
        "crypto": "Crypto",
        "custom": "FPIBank",
        "favorites": "Favorites",
        "change_language": "Change language",
        "enter_conversion_fiat": "Enter conversion (e.g., 100 USD to EUR):",
        "enter_conversion_crypto": "Enter crypto conversion (e.g., 2 BTC to USD):",
        "enter_conversion_custom": "Enter conversion using FPIBank currency (e.g., 10 FPI to USD):",
        "invalid_format": "Invalid format. Use: <amount> <currency_from> to <currency_to>.",
        "unknown_currency": "Unknown currency or format. Please try again.",
        "conversion_result": "Result: {amount} {from_currency} = {result:.6f} {to_currency}.",
        "added_favorite": "Added to favorites.",
        "already_favorite": "This pair is already in favorites.",
        "choose_favorite": "Your favorite conversions:",
        "no_favorites": "No favorites yet.",
        "prompt_amount_for_favorite": "Enter amount to convert for {from_currency} -> {to_currency}:",
        "chart_button": "📈 7-day Chart",
        "add_favorite_button": "⭐ Add to favorites",
        "chart_generated": "7-day chart for {from_currency}->{to_currency}:",
        "conversion_error": "Error retrieving conversion. Please try again later.",
        "help": "Help: Choose a platform to start currency conversion."
    },
    "ru": {
        "start": "Добро пожаловать! Пожалуйста, выберите язык:",
        "choose_language": "Выберите язык:",
        "language_selected": "Язык установлен: Русский.",
        "menu": "Главное меню:",
        "select_platform": "Выберите платформу:",
        "fiat": "Фиат",
        "crypto": "Крипто",
        "custom": "FPIБанк",
        "favorites": "Избранное",
        "change_language": "Сменить язык",
        "enter_conversion_fiat": "Введите запрос на конвертацию (например: 100 USD to EUR):",
        "enter_conversion_crypto": "Введите криптоконвертацию (например: 2 BTC to USD):",
        "enter_conversion_custom": "Введите конвертацию с валютой FPIBank (например: 10 FPI to USD):",
        "invalid_format": "Неверный формат. Используйте: <количество> <валюта_от> to <валюта_в>.",
        "unknown_currency": "Неизвестная валюта или формат. Попробуйте снова.",
        "conversion_result": "Результат: {amount} {from_currency} = {result:.6f} {to_currency}.",
        "added_favorite": "Добавлено в избранное.",
        "already_favorite": "Эта пара уже в избранном.",
        "choose_favorite": "Ваши избранные конвертации:",
        "no_favorites": "Пока нет избранного.",
        "prompt_amount_for_favorite": "Введите количество для конвертации {from_currency} -> {to_currency}:",
        "chart_button": "📈 7-дневный график",
        "add_favorite_button": "⭐ Добавить в избранное",
        "chart_generated": "7-дневный график для {from_currency}->{to_currency}:",
        "conversion_error": "Ошибка получения данных. Повторите попытку позже.",
        "help": "Справка: Выберите платформу для конвертации валют."
    }
}
