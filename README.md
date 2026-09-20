# daily-quote

A small [Druks](https://github.com/czpython/druks) app. Every morning it reads a
page of quotes through a browser you signed into, asks an agent to pick one, and
shows it on its Overview page.

It is a demo app, so it stays small. In about 120 lines it uses a schedule, a
browser session, an agent with a typed contract, its own table, two declared
pages, and the activity feed.

## What a run does

1. A schedule starts the run each morning.
2. The run borrows the browser session for `quotes.toscrape.com`, Zyte's
   scraping sandbox, and reads the quotes on page one. Any username and password
   work there, and you sign in once through the Druks login window.
3. An agent picks one quote and writes one short reason.
4. The quote is stored for that day and announced on the activity feed.

## What you see

- **Overview** shows today's quote, its author and the reason it was picked.
- **History** lists the quotes before today.

Both pages are declared in Python. The app ships no JavaScript.

## Install

```bash
uv pip install git+https://github.com/czpython/druks-daily-quote
```

Installing the package registers the app: Druks finds it through the
`druks.apps` entry point. Then open Settings, connect the browser session, and
sign in to Quotes to Scrape.

## Settings

`Quotes to consider` sets how many quotes from page one reach the agent.
The default is 5.
