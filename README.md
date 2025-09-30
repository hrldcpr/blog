### Setup

```bash
asdf install  # reads .tool-versions
bundle install
python -m venv .venv
. .venv/bin/activate.fish
pip install -r _scripts/requirements.txt
```

### Develop

```bash
. .venv/bin/activate.fish
bundle exec jekyll serve
```

For drafts, make a file in \_drafts/ without a date in the filename, and add `--drafts` to the `serve` command.

### Build

```bash
. .venv/bin/activate.fish
bundle exec jekyll build
```
