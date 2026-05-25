# Security and Secrets

If sensitive information (API keys, passwords, private keys) is accidentally committed, follow these steps immediately:

1. Revoke the exposed credential(s) (rotate the key) from the provider (OpenWeatherMap, AWS, etc.).
2. Remove the secret from the repository and history.
3. Force-push the cleaned history (this is destructive) or recreate the repo.
4. Add secrets to GitHub repository Secrets or environment variables for CI.

This repository should never contain a `.env` file or any plaintext secrets in commits.

## Preventive measures

- Add `.env` to `.gitignore` (already present).
- Use a pre-commit hook to block committing files matching common secret patterns.
- Store secrets in GitHub Secrets and reference them in CI workflows.
