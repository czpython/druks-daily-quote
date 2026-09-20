# daily-quote

A small [Druks](https://github.com/czpython/druks) app. Every morning it reads a
page of quotes through a browser you signed into, asks an agent to pick one, and
waits for you to keep it or skip it.

It is a demo app, so it stays small. In about 140 lines it uses a schedule, a
browser session, an agent with a typed contract, a human gate, its own table and
subject, and the activity feed.

## What a run does

1. A schedule starts the run each morning.
2. The run borrows the browser session for `quotes.toscrape.com`, Zyte's
   scraping sandbox, and reads the quotes on page one. Any username and password
   work there, and you sign in once through the Druks login window.
3. An agent picks one quote and writes one short reason.
4. The run waits at a gate: keep this quote, or skip it.
5. If you keep it, the quote is stored and announced on the activity feed.

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
