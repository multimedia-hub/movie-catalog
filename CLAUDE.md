# Movie Catalog

Static HTML movie guide deployed to GitHub Pages.

## Project structure

- `index.html` — Single-page app with all movie data, styles, and JS inline
- `posters/` — Local poster images (never rely on remote URLs, they expire)
- `.nojekyll` — Prevents Jekyll processing on GitHub Pages

## Deployment

- **Live site:** https://multimedia-hub.github.io/movie-catalog/
- **Remotes:** `org` → `multimedia-hub/movie-catalog` (deploy target), `origin` → `cdcalderon/movie-catalog`
- Push to `org` remote for deployment: `git push org main`
- No build step — static HTML served directly

## Movie data arrays in index.html

| Array | Section | Content |
|-------|---------|---------|
| `movies` | Premiadas (Awards) | International award films (Oscar, Cannes, Venice, Berlin, TIFF, Globes) |
| `latino` | Goya / Ariel / Platino | Spanish & Latin American award films |
| `chingonas` | Chingonas Carlos | Curated picks by genre |
| `discover` | Descubrir | Hidden gems, Asian cinema, world cinema |
| `studios` | Studios Legendarios | A24, NEON, Studio Ghibli catalogs |
| `cinelatam` | Cine España / México | Spanish & Mexican cinema |

## Poster management (CRITICAL)

### Adding a new movie

1. Add the JS object to the appropriate array with `poster: ""`
2. Fetch the poster URL from OMDB: `https://www.omdbapi.com/?t=TITLE&y=YEAR&apikey=trilogy`
3. Download the image to `posters/{slugified-title}-{year}.jpg`
4. Set `poster: "posters/{slugified-title}-{year}.jpg"` in the movie object

### Filename convention

Poster files use slugified title + year: `the-banshees-of-inisherin-2022.jpg`

Slugify rules: lowercase, ASCII-only (strip accents), replace non-alphanumeric with hyphens, trim to 50 chars.

### NEVER do this

- **Never use greedy regex** across movie objects to replace poster URLs — it causes cross-contamination (movie A gets movie B's poster)
- **Never rely on remote Amazon/IMDB URLs** in production — they expire within weeks
- **Never use URL-hash filenames** (e.g., `a90d2f97f7fe.jpg`) — use title-based names for debuggability
- **Never do global find-replace** on poster URLs — always match title→poster within the same movie object

### Batch poster operations

When adding multiple movies, use this per-movie approach:
```
For each movie:
  1. Find title + year
  2. Fetch OMDB → get poster URL
  3. Download to posters/{slug}-{year}.jpg
  4. Assign to that specific movie's poster field
```

Throttle OMDB API calls (0.3s delay) and Amazon image downloads (2s delay) to avoid rate limiting.

### OMDB API

- Working key: `trilogy` (free tier, 1000 requests/day)
- Endpoint: `https://www.omdbapi.com/?t=TITLE&y=YEAR&apikey=trilogy`
- Falls back to search without year if exact match fails
- The JS in index.html has an `onerror` fallback that calls OMDB for any broken images

## Movie object schema

```javascript
{
  title: "Movie Title",
  director: "Director Name",
  year: 2024,
  genre: "Drama, Thriller",
  rt: 95,           // Rotten Tomatoes percentage
  imdb: 8.2,        // IMDb score
  poster: "posters/movie-title-2024.jpg",
  awards: [{ label: "Goya Mejor Pelicula 2025", type: "goya" }],
  tags: ["goya", "platino"],  // Used for filtering
  review: "Review text in Spanish.",
  rec: true          // Optional: recommended flag
}
```

### Award types for badges

`oscar`, `globes`, `cannes`, `venice`, `berlin`, `tiff`, `goya`, `ariel`, `platino`, `nom`, `festival`

### Tag values for filtering

- movies array: `oscar`, `globes`, `cannes`, `venice`, `berlin`, `tiff`, `top`
- latino array: `goya`, `ariel`, `platino`
- chingonas: genre names like `sci-fi`, `comedy`, `drama`, `horror`, etc.
- discover: `hidden`, `asia`, `world`
- studios: `a24`, `neon`, `ghibli`
- cinelatam: `espana`, `mexico`
