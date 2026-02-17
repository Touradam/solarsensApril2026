# Solar Sense — Design tokens

Shared dark + gold theme for the landing page and Streamlit dashboard. Use these values for new pages or components so the product stays visually consistent.

## Colors (from styles.css)

| Token            | Hex       | Use |
|------------------|-----------|-----|
| bg-deep          | `#0d1117` | Main background |
| bg-charcoal      | `#161b22` | Sidebar, secondary panels |
| bg-card          | `#1c2128` | Cards, elevated surfaces |
| bg-elevated      | `#21262d` | Hover / raised UI |
| text-primary     | `#f0f6fc` | Primary text |
| text-secondary   | `#8b949e` | Secondary text, captions |
| text-muted       | `#6e7681` | Muted text |
| accent-amber     | `#d4a012` | Amber accent |
| accent-gold      | `#e6b422` | Gold accent (primary buttons, metrics) |
| accent-warm      | `#f0c14b` | Lighter gold highlight |
| border           | `#30363d` | Borders, dividers |

## Where they’re used

- **Landing page**: [styles.css](styles.css) `:root` and components.
- **Streamlit dashboard**: [.streamlit/config.toml](.streamlit/config.toml) theme + custom CSS in [app.py](app.py).
