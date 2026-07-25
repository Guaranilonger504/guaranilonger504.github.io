# Shiori Route

A minimal bilingual Hugo site with an automated arXiv paper radar.

## Local setup

Requirements:

- Docker
- [uv](https://docs.astral.sh/uv/)

```bash
uv sync
uv run pytest
docker compose up
```

The site is available at <http://localhost:1313>.

## Writing

Regular posts:

```text
content/posts/my-post.en.md
content/posts/my-post.zh.md
```

English is the default language. Chinese pages are published under `/zh/`.

## Paper radar

The radar fetches recent arXiv papers, filters them against the research profile,
and uses OpenAI Structured Outputs to generate bilingual recommendations.

All analysis is based only on titles and abstracts. It may be inaccurate; always
check the original paper.

Configuration is stored in:

```text
config/paper-radar.yaml
```

Edit this file to change arXiv categories, research topics, models, thresholds,
batch sizes, and cost limits.

Useful commands:

```bash
# Fetch and plan without OpenAI or file writes
uv run python scripts/paper_radar.py --dry-run

# Fetch without OpenAI or file writes
uv run python scripts/paper_radar.py --fetch-only

# Run the complete pipeline
export OPENAI_API_KEY="your-key"
uv run python scripts/paper_radar.py --analyze
```

Generated files:

```text
content/papers/YYYY-MM-DD.en.md
content/papers/YYYY-MM-DD.zh.md
static/data/paper-radar/YYYY-MM-DD.json
static/paper-radar.xml
data/processed_papers.json
```

The state file prevents the same arXiv version from being analyzed twice.

## GitHub Actions

Add `OPENAI_API_KEY` under:

**Settings → Secrets and variables → Actions**

`Daily paper radar` runs every day at `21:17 UTC` (`06:17 JST` the next day).
It can also be started manually from the Actions tab.

The workflow tests the project, generates new content, commits changes, and
reuses the existing Pages workflow for deployment.

Set the Pages source to **GitHub Actions** under **Settings → Pages**.

## RSS

Subscribe to:

```text
https://your-domain.example/paper-radar.xml
```

Update `site.base_url` in `config/paper-radar.yaml` after configuring the final
domain.

