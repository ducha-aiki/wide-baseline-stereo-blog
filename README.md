# Wide baseline stereo meets deep learning

Source of [ducha-aiki.github.io/wide-baseline-stereo-blog](https://ducha-aiki.github.io/wide-baseline-stereo-blog) —
a blog about wide baseline stereo, local features, RANSAC, image matching and
the Image Matching Challenges, by [Dmytro Mishkin](https://dmytro.ai).

Originally written with [fastpages](https://github.com/fastai/fastpages) (Jekyll),
migrated to [Quarto](https://quarto.org) in 2024. The old `/YYYY/MM/DD/slug` URLs
are kept alive through the `aliases` in each post's front matter.

## Layout

| path | what it is |
| --- | --- |
| `posts/*.ipynb` | one Jupyter notebook per post, front matter in the first raw cell |
| `index.qmd`, `about.qmd` | home (post listing) and about pages |
| `_quarto.yml` | site config |
| `scripts/post_render.py` | post-render pass: makes the old-URL redirect stubs work without JavaScript, and copies the feed to the pre-migration `/feed.xml` path |
| `docs/` | rendered site — **committed on purpose**, see below |

## Building and publishing

GitHub Pages serves this repo from the **`master` branch, `/docs` folder**, so the
rendered output has to be committed for anything to go live:

```bash
quarto render          # writes to docs/ ; notebooks are not re-executed
git add -A docs && git commit -m "rebuild" && git push
```

The `gh-pages` branch is a leftover of the Jekyll setup and is not served.
