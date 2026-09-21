# daily-quote

A small [Druks](https://github.com/czpython/druks) app. Every day it reads a
page of quotes through a browser you signed into, asks an agent to pick one, and
shows it on its Overview page.

It is a demo app, so it stays small. In about 110 lines it uses a schedule, a
browser session, an agent with a typed contract, its own table and a declared
page.

## What a run does

1. A schedule starts the run at midnight.
2. The run borrows the browser session for `quotes.toscrape.com`, Zyte's
   scraping sandbox, and reads the quotes on page one, leaving out the ones it
   has picked before. Any username and password work there, and you sign in once
   through the Druks login window.
3. An agent answers with the number of the quote it chose, so the wording
   stored is the site's own.
4. The pick is stored.

## What you see

**Overview** shows the newest quote, and every quote before it under
**Earlier**.

The page is declared in Python. The app ships no JavaScript.

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
