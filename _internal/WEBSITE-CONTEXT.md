# Personal Academic Website - Development Context

## Quick Reference

| Item | Value |
|------|-------|
| **Site URL** | https://data-wise.github.io |
| **Repo** | github.com/Data-Wise/data-wise.github.io |
| **Local Path** | ~/projects/dev-tools/data-wise.github.io |
| **Platform** | Quarto (static site) |
| **Theme** | Warm Academic (custom) |
| **Layout** | Layout 1 - Logo Header + Compact Bio |

---

## Owner Information

| Field | Value |
|-------|-------|
| **Name** | Davood Tofighi, Ph.D. |
| **Title** | Associate Professor |
| **Department** | Department of Mathematics & Statistics |
| **Institution** | University of New Mexico |
| **Office** | SMLC 228 |
| **Email** | dtofighi@unm.edu (JS-protected) |

### Profile Links

| Platform | URL |
|----------|-----|
| **UNM Profile** | https://math.unm.edu/people/academic-personnel/davood-tofighi |
| **Google Scholar** | https://scholar.google.com/citations?user=hzQ60YcAAAAJ |
| **ORCID** | https://orcid.org/0000-0001-8523-7776 |
| **GitHub** | https://github.com/Data-Wise |
| **LinkedIn** | https://www.linkedin.com/in/davood-tofighi-b6176ab8/ |

### Research Focus

- Causal inference & mediation analysis (DAGs)
- Sensitivity analysis (statistical & Monte Carlo)
- Generalized linear mixed-effects models
- Machine learning in health data
- Drug delivery optimization (cancer, COVID-19)

### Professional

- Associate Editor: Frontiers in Psychology (Quantitative Psychology section)
- Funding: NASA, NSF, NIH
- Education: Ph.D. Quantitative Methods (ASU), M.A. Educational Psychology, M.Sc./B.Sc. Industrial Engineering

---

## Design System

### Color Palette: Warm Academic

```scss
$cream: #faf8f5;        // Background
$dark-brown: #78350f;   // Header, footer
$amber: #b45309;        // Primary, links
$gold: #d97706;         // Accent, logo
$warm-gray: #3d3d3d;    // Text
$light-cream: #f5f0eb;  // Subtle backgrounds
$tan: #d4a373;          // Borders
```

### Typography

- **Headings**: Playfair Display, Georgia, serif
- **Body**: Source Sans Pro, system fonts

### Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│ [DT] Davood Tofighi    Home | Research | Pubs | ...     │ ← Dark brown header
├─────────────────────────────────────────────────────────┤
│  ┌────┐  Name, Title, Department                        │
│  │ 📷 │  Institution (linked)                           │ ← Compact bio
│  └────┘  Tagline                                        │
│                                                         │
│  ┌─ Highlight Box ─────────────────────────────────┐   │ ← Gold border
│  │ Main intro text                                  │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  [Quick Links as buttons]                               │
│                                                         │
│  Content sections...                                    │ ← Cream background
└─────────────────────────────────────────────────────────┘
```

---

## File Structure

```
~/projects/dev-tools/data-wise.github.io/
├── _quarto.yml              # Site configuration
├── warm-academic.scss       # Custom theme (colors, typography, layout)
├── index.qmd                # Homepage
├── research.qmd             # Research interests
├── publications.qmd         # Publications list
├── software.qmd             # mediationverse & tools
├── teaching.qmd             # Courses & teaching
├── .gitignore
├── README.md
├── assets/
│   ├── logo-placeholder.svg      # "DT" gold box (40x40)
│   ├── logo-placeholder.png      # Copy of SVG
│   └── profile-placeholder.svg   # Silhouette (100x100)
└── .github/
    └── workflows/
        └── publish.yml      # Auto-deploy on push
```

---

## Key Files Content

### _quarto.yml

```yaml
project:
  type: website
  output-dir: _site

website:
  title: "Davood Tofighi"
  navbar:
    background: dark
    logo: "assets/logo-placeholder.svg"
    title: "Davood Tofighi"
    left: [Home, Research, Publications, Software, Teaching]
    right: [GitHub icon, Email icon]
  page-footer:
    background: dark

format:
  html:
    theme:
      light: [default, warm-academic.scss]
      dark: [darkly, warm-academic.scss]
```

### Email Protection (JS Obfuscation)

```html
📧 <a href="#" id="email-link">Enable JavaScript to see email</a>

<script>
document.addEventListener('DOMContentLoaded', function() {
  var el = document.getElementById('email-link');
  var u = 'dtofighi';
  var d = 'unm.edu';
  el.href = 'mailto:' + u + '@' + d;
  el.textContent = u + '@' + d;
});
</script>
```

### Profile Badges

```markdown
[![Google Scholar](https://img.shields.io/badge/Google%20Scholar-4285F4?style=flat&logo=google-scholar&logoColor=white)](https://scholar.google.com/citations?user=hzQ60YcAAAAJ)
[![ORCID](https://img.shields.io/badge/ORCID-A6CE39?style=flat&logo=orcid&logoColor=white)](https://orcid.org/0000-0001-8523-7776)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/Data-Wise)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/davood-tofighi-b6176ab8/)
```

---

## Status

### ✅ Completed

- [x] Repo renamed: data-wise → data-wise.github.io
- [x] Quarto site structure created
- [x] Warm Academic theme implemented
- [x] Layout 1 (Logo Header + Compact Bio)
- [x] All pages created (Home, Research, Publications, Software, Teaching)
- [x] Profile links added (Scholar, ORCID, GitHub, LinkedIn)
- [x] Email JS protection
- [x] GitHub Actions auto-deploy
- [x] Site live at data-wise.github.io

### 📝 Pending / To Add Later

- [ ] **Profile photo**: Replace `assets/profile-placeholder.svg` with actual `profile.jpg`
- [ ] **Logo**: Replace `assets/logo-placeholder.svg` with designed logo
- [ ] **Publications**: Populate full publication list in `publications.qmd`
- [ ] **Google Scholar ID**: Currently correct (hzQ60YcAAAAJ)
- [ ] **CV PDF**: Add downloadable CV to `assets/cv.pdf`

---

## Commands

### Local Development

```bash
cd ~/projects/dev-tools/data-wise.github.io

# Preview
quarto preview

# Build
quarto render

# Open local build
open _site/index.html
```

### Deploy

```bash
git add -A
git commit -m "Update message"
git push
# Auto-deploys via GitHub Actions
```

### Check Deployment

```bash
gh run list --repo Data-Wise/data-wise.github.io --limit 1
```

---

## Related Projects

| Project | Relationship |
|---------|--------------|
| **mediationverse** | R package ecosystem (linked from Software page) |
| **zsh-claude-workflow** | Dev tool (separate MkDocs site, indigo theme) |
| **docs-standards** | Shared documentation configs |

---

## Design Decisions Made

1. **Platform**: Quarto (not MkDocs) — better for academic personal sites
2. **Theme**: Warm Academic — friendly, approachable, distinctive
3. **Layout**: Logo Header + Compact Bio — professional, not photo-dominant
4. **Photo size**: 80px circular — small, not dominant
5. **Logo**: Placeholder "DT" gold box — space for future branding
6. **Email**: JS obfuscation — sufficient protection for academic site
7. **Dark mode**: Supported via Quarto theme toggle
8. **No ResearchGate**: Removed per preference

---

## New Chat Quick Start

To continue development in a new chat, say:

> "I'm continuing work on my personal academic website at data-wise.github.io. 
> Read the context file at ~/projects/dev-tools/data-wise.github.io/_internal/WEBSITE-CONTEXT.md 
> to understand the current state."

Or paste this context document directly.
