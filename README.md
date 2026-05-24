# Public AI Switzerland website

Source for [publicai.ch](https://publicai.ch) — the marketing site for Public AI Switzerland, a customer-owned cooperative distributing Swiss-made AI.

This is a **static site**: HTML, [Picnic CSS](https://picnicss.com/) (CDN), and custom styles in `assets/style.css`. No build step.

## Local preview

```bash
git clone https://github.com/forpublicai/publicai.ch.git
cd publicai.ch
open index.html
```

Or with a local server:

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Contributing

1. Branch from `main`: `git checkout -b your-change`
2. Edit HTML/CSS; keep internal links relative and images optimized
3. Open a pull request against `main` with a short description of what changed

Style notes: semantic HTML5, 2-space indent, BEM-style class names in `assets/style.css`, minimal vanilla JS only when needed.

## Deployment

Merging to `main` triggers [`.github/workflows/ftp.yml`](.github/workflows/ftp.yml), which syncs the repo to production via FTP. No manual deploy step.

## License

[Apache License 2.0](LICENSE)
