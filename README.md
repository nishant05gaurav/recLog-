# recLog

An automated content sync pipeline that connects a Dev.to blog to a personal portfolio — every new article published on Dev.to is fetched, deduplicated, and injected into the portfolio's HTML automatically, without touching the site manually or triggering a redeployment.

**Live:** [>log(nishant)_](https://nishant05gaurav.github.io/recLog-/) 

## Quick Start

```bash
git clone https://github.com/nishant05gaurav/recLog.git
cd recLog

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Add your Dev.to API key to .env (see Environment Variables below)

python main.py
```


## How It Works

```
Dev.to API  →  fetcher.py  →  summarizer.py  →  injector.py  →  index.html
                                                        ↑
                                              GitHub Actions (cron / push)
```

1. **Fetch** — `fetcher.py` hits the Dev.to REST API and pulls the latest published articles (title, URL, cover image, tags, published date).
2. **Deduplicate** — `main.py` reads the current `index.html` and checks both the article URL and title against existing content. Only genuinely new articles make it through.
3. **Summarize** — `summarizer.py` generates a short description for each new article card.
4. **Inject** — `injector.py` parses the HTML with BeautifulSoup4 and inserts the new article cards into the articles section in-place.
5. **Deploy** — GitHub Actions runs the pipeline on schedule (or on push), commits the updated `index.html` back to the repo, and the site reflects the new content automatically.


## Demo / Preview

![recLog Hero](/assets/preview.png)

The portfolio loads with a full-bleed hero section, a terminal-style brand mark (`>log(nishant)_`), and an Articles page that stays current without any manual updates.

Before this pipeline: publishing on Dev.to meant separately updating the portfolio. After: push to Dev.to, done.


## Problem & Purpose

Stale portfolios are a common problem — developers write regularly but forget to reflect that work on their personal site. This project eliminates that gap entirely. The portfolio is always in sync with the blog, with zero manual intervention after setup.

It also demonstrates something more interesting than a static site: an actual CI/CD-integrated content pipeline where Python, the Dev.to API, HTML parsing, and GitHub Actions work together as a complete automated system.


## Highlights

- **Dual-key deduplication** — the pipeline checks both the article `url` and `title` against the existing HTML before injecting. This prevents duplicate cards even across edge cases like URL changes or re-runs on the same content.
- **In-place HTML injection** — `injector.py` uses BeautifulSoup4 to locate the exact insertion point in `index.html` and surgically adds new cards without reformatting or corrupting the surrounding markup.
- **Serverless CI/CD with GitHub Actions** — `.github/workflows/main.yml` defines the full pipeline. No server, no manual deploy, no build tool. The workflow runs the Python script, commits the result, and the site updates.
- **Separation of concerns** — fetch, summarize, and inject are three independent modules. The pipeline in `main.py` orchestrates them cleanly, making each step easy to test or replace independently.
- **Environment-isolated credentials** — the Dev.to API key lives in `.env` and never touches the source code. The GitHub Actions workflow reads it from repository secrets.


## Features

- Fetches latest articles from Dev.to via REST API
- Deduplicates by URL and title — no duplicate cards ever appear
- Dynamically injects new article cards into portfolio HTML
- Fully automated via GitHub Actions — triggered on schedule or push
- Environment variable-based API key management
- Zero manual steps after initial setup


## Tech Stack

| Layer | Tools |
---|---
| Language | Python 3.11 |
| HTML Parsing & Injection | BeautifulSoup4 |
| API Integration | Dev.to REST API, `requests` |
| Automation | GitHub Actions |
| Frontend | HTML5, CSS3 |
| Config | `.env`, `python-dotenv` |


## Project Structure

```
recLog/
├── .github/
│   └── workflows/
│       └── main.yml        # GitHub Actions pipeline definition
├── fetcher.py              # Dev.to API → article list
├── summarizer.py           # Generates article card descriptions
├── injector.py             # BeautifulSoup4 HTML injection logic
├── main.py                 # Orchestrator — dedup + pipeline flow
├── index.html              # Portfolio frontend (auto-updated)
├── style.css               # Site styles
├── requirements.txt
├── .env                    # API credentials (not committed)
└── .gitignore
```


## Environment Variables

Create a `.env` file in the project root:

```env
DEVTO_API_KEY=your_dev_to_api_key_here
```

Get your Dev.to API key from: **Dev.to → Settings → Account → DEV Community API Keys**

For GitHub Actions, add `DEVTO_API_KEY` as a repository secret under **Settings → Secrets and variables → Actions**.


## GitHub Actions Workflow

The pipeline in `.github/workflows/main.yml` runs automatically. To trigger it manually or adjust the schedule, edit the `on:` block:

```yaml
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 */6 * * *'    # Runs every 6 hours — adjust as needed
```

After the script runs, the workflow commits the updated `index.html` back to the repo with a timestamped commit message. The site stays current without any manual step.


## License

MIT License: Use it, Fork it, Build on it.


## Author

Built by [Nishant Gaurav](https://github.com/nishant05gaurav)  

[GitHub](https://github.com/nishant05gaurav) · [LinkedIn](https://shorturl.at/kWLs5) · [nishant05gaurav@gmail.com](mailto:nishant05gaurav@gmail.com)