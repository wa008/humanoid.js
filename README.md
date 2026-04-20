# humanoid.js

> Zero-dependency, single-file web tool that scores how human-looking a pointer/touch interaction is — and tells you which specific signals gave it away.

**[👉 Live demo: open `index.html` in any browser](./index.html)**

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

The output is a **0–100 risk score** (higher = more human-like) plus a list of exactly which rules fired.

## Why "LLM-friendly"?

A common question: *"If I automate my clicks with Puppeteer / ADB / a CDP driver, will they look human?"*

humanoid.js answers this with a **stable, structured JSON report** that any LLM agent or automation script can consume to iterate on its click strategy.

### Programmatic API

```js
// Latest analysis (plain object) — after the user releases the pointer
window.humanoid.getReport();

// Last 50 analyses
window.humanoid.getHistory();

// Latest analysis as a JSON string
window.humanoid.getReportJSON();

// Listen for new analyses
window.addEventListener('humanoid:analysis', (e) => {
    console.log(e.detail.risk.score, e.detail.risk.reasons);
});
```

For environments where you can only read the DOM (no script eval), the most recent report is also mirrored into an inline `<script type="application/json" id="humanoid-report-json">` tag, ready to parse.

### Report shape

```json
{
  "timestamp": 1710000000000,
  "pointerType": "touch",
  "isTrusted": true,
  "duration": 312,
  "samples": 18,
  "displacement": 142.6,
  "pathLength": 151.2,
  "pressure":     { "min": 0.21, "max": 0.74, "avg": 0.48, "std": 0.13, "changeCount": 11, "forceTouchSupported": false },
  "contactArea":  { "avgWidth": 22.4, "avgHeight": 22.4 },
  "velocity":     { "avg": 486.3, "std": 112.7 },
  "interval":     { "avg": 12.4, "std": 3.1, "pauseCount": 0 },
  "trajectory":   { "straightness": 94.3, "pathEfficiency": 94.3, "curvature": 1.82, "jitter": 0.91, "bezierMatch": 42.1, "directionChanges": 2 },
  "advanced":     { "entropy": 3.112, "angleStd": 8.43, "speedConsistency": 72.5, "coordPrecision": 2 },
  "risk":         { "score": 92, "level": "low", "verdict": "likely-human", "reasons": [] },
  "environment":  { "userAgent": "...", "webdriver": false, "maxTouchPoints": 5, "devicePixelRatio": 2 }
}
```

### Typical LLM-driven loop

1. Agent drives a synthetic click/swipe on the pad.
2. Agent reads `window.humanoid.getReport()`.
3. If `risk.verdict !== 'likely-human'`, agent inspects `risk.reasons` and adjusts (add jitter, randomize interval, fake pressure, etc.).
4. Repeat until the score is acceptable.

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
├── adb_click/      # companion shell/Python tools for simulating Android clicks
├── LICENSE
└── README.md
```

## Contributing

Issues and PRs welcome. Please keep:
- Single-file (`index.html`) with no build tooling.
- No runtime dependencies.
- New signals should feed into both the dashboard and the JSON report.

## License

MIT — see [LICENSE](./LICENSE).

## Disclaimer

For research, testing, and defensive/awareness purposes. Do not use to bypass anti-fraud or anti-abuse systems you are not authorized to test.
