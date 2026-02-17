# Yad2 Smart Scraper

Scrapes Yad2 rental listings and notifies via Telegram when new items appear.

---

## Setup

### GitHub Secrets

Add these secrets in your repo: **Settings → Secrets and variables → Actions**

| Secret | Description |
|--------|-------------|
| `API_TOKEN` | Telegram Bot token from [@BotFather](https://t.me/BotFather) |
| `CHAT_ID` | Your chat ID (use [@userinfobot](https://t.me/userinfobot)) |
| `API_URL` | Yad2 search URL (e.g. `https://gw.yad2.co.il/realestate-feed/rent/map?city=0028&area=12&...`) |

### Schedule

The workflow runs every 10 minutes via GitHub Actions cron.

---

## Usage

### Local

```bash
pip install -r requirements.txt
cp .env.example .env   # add your API_TOKEN, CHAT_ID, API_URL
python scraper.py --api-url "URL"   # or omit if API_URL is in .env
python scraper.py --clean           # clear DB and treat all as new
```

### Options

| Flag | Description |
|------|-------------|
| `--api-url` | Yad2 API URL with search parameters (required) |
| `--clean` | Clear rentals DB before scraping (treat all as new) |
