# Tech newsletter crew

A Researcher searches with Serper and hands three sourced stories to a Writer
through the second task's context. The Writer has no tools. The final newsletter
has exactly five lines: a headline, three numbered stories, and one "Why it
matters" line. Verbose agent logs appear before the newsletter.

## Setup and run

Use Python 3.10 or later, activate a virtual environment, and install:

```sh
pip install 'crewai[tools]'
```

Set `OPENAI_API_KEY` and `SERPER_API_KEY` in your environment. Get a Serper key
from [serper.dev](https://serper.dev/). Optionally set `MODEL` to a CrewAI
OpenAI model name; it defaults to `gpt-4o-mini`.

```sh
export OPENAI_API_KEY="your-openai-key"
export SERPER_API_KEY="your-serper-key"
# Optional: export MODEL="gpt-4o-mini"
python news_crew.py
```

In PowerShell, use `$env:OPENAI_API_KEY = "your-openai-key"` and
`$env:SERPER_API_KEY = "your-serper-key"` instead of `export`. Keep keys out
of source control. API calls may incur charges.

The local date is supplied on each run; search results and model output can vary.
If fewer than three current stories can be verified, the Writer identifies the
gap instead of inventing a story. To complete the assignment, capture a screenshot
of a full run showing the search and newsletter, and compare runs on different
days. Changing stories is not guaranteed.
