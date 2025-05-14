# Telegram Currency Conversion Bot

This is a Telegram bot that allows users to convert fiat currencies, cryptocurrencies, and custom units. The bot provides real-time conversion rates, allows users to save favorite conversion pairs, and generates currency exchange charts. It supports multiple languages for a better user experience.

## Features

- Real-time currency and cryptocurrency conversion.
- Ability to save favorite conversion pairs for quick access.
- Generate charts for exchange rate trends.
- Multi-language support.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/t3rmynal/telegram-currency-converter-bot.git
   ```

2. Navigate to the project directory:

   ```bash
   cd telegram-currency-converter-bot
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure your bot settings by editing `config.py`:

   ```python
   # config.py

   BOT_TOKEN = "your-telegram-bot-token"
   EXCHANGERATE_API_URL = "your-exchangerate-api-url"
   COINGECKO_API_URL = "your-coingecko-api-url"
   ```

   Replace the placeholders with your actual Telegram bot token and API URLs for exchange rates.

## Running the Bot

To run the bot, use the following command:

```bash
python bot.py
```

## Commands

* `/start` — Start the bot and choose your preferred language.
* Users can choose between fiat currencies, cryptocurrencies, or custom units for conversion in telegram bot menu interface.
* Favorite conversion pairs can be saved for quicker access in the menu.

## Configuration

All sensitive settings, such as your bot token and API keys, should be stored in the `config.py` file.

## License

This project is licensed under the MIT License.
