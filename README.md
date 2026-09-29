# signing

Container image signing CI/CD test

https://docs.sigstore.dev/quickstart/quickstart-ci/

## How it works - github

Create `.github/workflows/container.yml`

The important part for keyless signing is:
```
permissions:
  id-token: write
```
GitHub supplies an OIDC identity token to the job, and Cosign uses it with Sigstore/Fulcio to obtain an ephemeral signing certificate.
`docker/build-push-action` exposes the resulting image digest as `${{ steps.build.outputs.digest }}` so the signature is attached to the digest not to the named tag.

## How it works - gitlab

Create `.gitlab-ci.yml`

GitLab's OIDC configuration is:
```
id_tokens:
  SIGSTORE_ID_TOKEN:
    aud: sigstore
```
Cosign automatically uses that token when it is available as `SIGSTORE_ID_TOKEN`
Add these as masked/protected CI/CD variables: `GHCR_USERNAME` and `GHCR_TOKEN`.
`GHCR_TOKEN` needs permission to write packages to the relevant GHCR namespace.

# Verify the signature

cosign verify \
  ghcr.io/myorg/myimage@sha256:... \
  --certificate-identity-regexp='https://github.com/myorg/myrepo/.*' \
  --certificate-oidc-issuer='https://token.actions.githubusercontent.com'

For GitLab, use the GitLab project/configuration identity and https://gitlab.com as the issuer, as shown in GitLab's verification documentation. 

# github

# gitlab.com

See https://docs.gitlab.com/ci/yaml/signing_examples/

# gitlab self-hosted (ecdf or eidf)

GitLab Self-Managed installations require a self-hosted Sigstore/Fulcio/Rekor setup.

See https://docs.gitlab.com/ci/yaml/signing_self_hosted/
