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

For tikz diagrams, just manually convert them to SVGs for now, e.g.:

```bash
cd _diagrams/annulus-is-more/
latex annulus.tex && dvisvgm -Z2 annulus.dvi && cp annulus.svg ../../assets/
```

(`-Z2` is zoom)

### Build

```bash
. .venv/bin/activate.fish
bundle exec jekyll build
```
