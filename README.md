# humanoid.js

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://wa008.github.io/humanoid.js/)
[![Single File](https://img.shields.io/badge/single--file-zero%20deps-informational)](./index.html)

> Zero-dependency, single-file web tool that scores how human-looking a pointer/touch interaction is — and tells you which specific signals gave it away.

**[👉 Live demo](https://wa008.github.io/humanoid.js/)** (or open `index.html` in any browser)

---

## What it does

Every click, long-press, or swipe on the test pad is analyzed in real time across ~30 signals that click-fraud and anti-bot systems actually look at:

| Category              | Signals                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| Event trust           | `isTrusted`, pointer/touch source, `navigator.webdriver`                |
| Pressure              | min / max / avg / stddev, change count, Force Touch                     |
| Contact geometry      | `radiusX`, `radiusY`, `rotationAngle`, width × height                   |
| Trajectory            | straightness, path efficiency, curvature, jitter, Bezier-match          |
| Time profile          | duration, sample interval avg/stddev, pauses                            |
| Advanced              | entropy, angle stddev, speed consistency, coordinate decimal precision  |
| Environment           | WebDriver, HeadlessChrome, Selenium markers, UA / touch mismatch, etc.  |

The output is a **0–100 risk score** (higher = more human-like) plus a list of exactly which rules fired, shown directly on the page.

## Usage

No build step. No dependencies.

```bash
# just open it
open index.html            # macOS
xdg-open index.html        # Linux

# or serve locally
python3 -m http.server 8000
```

Use `?lang=en` or click the `EN / 中文` toggle for language.

## Repository layout

```
.
├── index.html      # the whole app — HTML + CSS + JS, no build
├── LICENSE
└── README.md
```

## Contributing

Issues and PRs welcome. Please keep:
- Single-file (`index.html`) with no build tooling.
- No runtime dependencies.

## License

MIT — see [LICENSE](./LICENSE).

## Disclaimer

For research, testing, and defensive/awareness purposes. Do not use to bypass anti-fraud or anti-abuse systems you are not authorized to test.
