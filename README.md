# Koure Forms

**Structural Design • 3D Visualization • Creative Builds**
*Where vision takes form.*

Website for Koure Forms: decks, yurt platforms and DIY blueprints in the Hickory / Charlotte, NC area.

- Phone (call or text): 828-270-8000
- Email: Koureforms@gmail.com

## What's in this repo

| Path | What it is |
|---|---|
| `index.html` | The full website as one file, with every photo built in. This is what you host. |
| `src/site.src.html` | Editable source of the page. Photos are referenced from `src/img/`. |
| `src/img/` | Original photos, blueprint pages and logo files. |
| `src/build.py` | Rebuilds `index.html` from the source and photos. |

## Site sections

- **Home:** slideshow of builds and blueprint pages
- **What we do:** services
- **Deck sizes:** 4'×5', 5'×5', 4'×10', 5'×10' drawn to scale, with prices, *Order – pickup* and *Order – delivery* buttons, a section calculator and a photo gallery
- **Yurt platforms:** 16', 20', 24', 30' round bases drawn to scale, with prices, 50% deposit amounts, order buttons and an 8-photo gallery
- **DIY blueprints:** sample blueprint pages
- **Custom crafts, How we work, About the company, Pricing, Contact**
- **Quote / order page:** fills in from whichever button was tapped, shows an estimate, requires dates at least 3 days out, and lets the customer email, text or copy the request

## Prices

| Deck | Price | | Yurt platform | OSB top | Deck boards |
|---|---|---|---|---|---|
| 4' × 5' | $599 | | 16' round | $3,295 | $4,195 |
| 5' × 5' | $669 | | 20' round | $4,895 | $6,295 |
| 4' × 10' | $929 | | 24' round | $6,795 | $8,795 |
| 5' × 10' | $1,079 | | 30' round | $10,395 | $13,495 |

Yurt orders take a 50% deposit. Delivery and setup are quoted separately.

## Host it on your own domain

**Netlify (simplest):**
1. Sign in at netlify.com → **Add new site → Import an existing project → GitHub** → pick this repo.
2. Leave the build command empty and set the publish directory to `/`. Deploy.
3. **Domain management → Add a domain** to connect your domain.

**Vercel** works the same way: import the repo, framework preset **Other**, no build command.

**GitHub Pages:** repo **Settings → Pages → Deploy from a branch → `main` / root**.

## Connect Stripe payment links

Pickup and yurt order buttons open the quote page until payment links are added.
To send them straight to Stripe checkout, paste each link into the `PAY` list in
`src/site.src.html`, then rebuild:

```js
var PAY = {
  deck: ["", "", "", ""],                      // 4x5, 5x5, 4x10, 5x10 (full price, pickup)
  yurt: [{ osb: "", boards: "" }, ...]         // 16', 20', 24', 30' (50% deposit)
};
```

## Rebuild after editing

```bash
pip install pillow
python src/build.py
```

This regenerates `index.html`. Commit both files.
