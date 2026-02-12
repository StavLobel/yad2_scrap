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
python scraper.py --api-url "https://gw.yad2.co.il/realestate-feed/rent/map?city=0028&area=12&..."
```

### Options

| Flag | Description |
|------|-------------|
| `--api-url` | Yad2 API URL with search parameters (required) |
| `--clean` | Clear rentals DB before scraping (treat all as new) |
