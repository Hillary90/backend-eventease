# Deploying Backend to Render (Docker) — Secrets & Steps

This document lists the repository secrets needed and shows how the GitHub Actions workflow writes your Firebase service account file and triggers Render.

Required repository secrets

- `RENDER_API_KEY` (optional): Render API key with permission to trigger deploys. Used by the workflow to call Render's deploy API.
- `RENDER_SERVICE_ID` (optional): Render service ID for your backend service. Required for deploy trigger.
- `DATABASE_URL`: The database connection string for production (e.g. `postgres://user:pass@host:5432/dbname`). If omitted, the app uses local SQLite (not recommended for production).
- `FIREBASE_SERVICE_ACCOUNT` or `FIREBASE_SERVICE_ACCOUNT_BASE64` (optional but recommended): The Firebase service account JSON used for `firebase-admin` initialization.
  - `FIREBASE_SERVICE_ACCOUNT`: raw JSON contents of the `serviceAccountKey.json` file.
  - `FIREBASE_SERVICE_ACCOUNT_BASE64`: base64-encoded contents of the `serviceAccountKey.json`. The workflow prefers this if both are present.
- `GITHUB_TOKEN` (provided by GitHub Actions): used to publish to GitHub Container Registry (GHCR). No additional token required unless your org restricts it.

Optional secrets

- `GHCR_PAT`: Personal Access Token for GHCR (if you need explicit PAT instead of `GITHUB_TOKEN`).

How the workflow uses the secrets

- The GitHub Actions workflow `/.github/workflows/docker-publish.yml` checks out the repository, then attempts to write `serviceAccountKey.json` in the workspace:
  - If `FIREBASE_SERVICE_ACCOUNT_BASE64` is provided, it decodes it and writes the file.
  - Else if `FIREBASE_SERVICE_ACCOUNT` is provided, it writes the raw JSON contents.
  - Otherwise, it skips writing the file.
- The Docker build then runs and will include `serviceAccountKey.json` in the build context if it exists.
- After building the image, the workflow pushes it to GHCR and optionally triggers a Render deploy using `RENDER_API_KEY` and `RENDER_SERVICE_ID`.

Runtime handling on Render

- The Docker image now uses an entrypoint script `start.sh` which, at container start, will check for either `FIREBASE_SERVICE_ACCOUNT_BASE64` or `FIREBASE_SERVICE_ACCOUNT` environment variables and write a `serviceAccountKey.json` file into the container filesystem. This means you should set one of those env vars in Render's dashboard (or via `render.yaml`) rather than trying to bake the file into the image.

Setting secrets on Render

- In your Render service settings (Environment > Environment Variables) add:
  - `DATABASE_URL` = your Postgres URL (Render provides with managed DB)
  - `FIREBASE_SERVICE_ACCOUNT_BASE64` = base64(serviceAccountKey.json) OR `FIREBASE_SERVICE_ACCOUNT` = raw JSON
  - `PORT` = `8000` (optional; default is 8000)

Deploying to Render using Docker

1. Create a new Web Service in Render.
2. For "Environment", choose "Docker".
3. Connect the repository `backend-eventease` and choose the branch (`main` or `final-intergration`).
4. (Optional) Provide a `render.yaml` or configure the service in the Render UI. Ensure Environment Variables above are set.
5. Trigger a deploy — Render will build the container and run it. On startup the container will write `serviceAccountKey.json` from the env and start the app.

Notes

- Avoid storing `serviceAccountKey.json` directly in the repo. Use secrets.
- If you prefer not to use the entrypoint copy method, Render also supports adding files via Start Command or mounting from a private store; the entrypoint method is the simplest.

How to add secrets in GitHub

1. Go to your repository on GitHub.
2. Settings -> Secrets -> Actions -> New repository secret.
3. Add each secret using the names above.

Notes and security

- Prefer storing the service account JSON as a base64-encoded value in `FIREBASE_SERVICE_ACCOUNT_BASE64` to avoid accidental newline/quoting issues.
- Limit the `RENDER_API_KEY` scope to the minimal permissions required for deploys.
- Do not check `serviceAccountKey.json` into source control.

Local testing

- For local testing you can create a `serviceAccountKey.json` in the project root and run Docker build locally:

```bash
# Build locally (from backend-eventease/)
docker build -t backend-eventease:local .
```

- To run the container locally:

```bash
docker run -p 8000:8000 -e DATABASE_URL="sqlite:///./eventease.db" backend-eventease:local
```

If you want, I can also add a GitHub Actions step to scrub or remove `serviceAccountKey.json` at the end of the job, or create a short Render-specific `render.yaml` to connect your service directly. Let me know which you'd prefer.
