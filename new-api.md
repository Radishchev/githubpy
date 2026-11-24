# GitHub REST token authentication migration

GitHub.com no longer accepts account passwords for REST API authentication.
Use a personal access token, OAuth token, or GitHub App token in an Authorization
header. Token header authentication continues to work. Anonymous public requests
remain supported.

For this SDK migration, preserve the existing constructor signature for callers:

- If `access_token` is supplied, use it even when obsolete username/password
  arguments are also supplied. A supported header is `Authorization: token TOKEN`.
- If username or password is supplied without `access_token`, raise ValueError
  with a message telling the caller to provide `access_token`. Never send an
  account password to the REST API.
- With no authentication arguments, keep anonymous requests working.
- Preserve response parsing, request paths, and the token-only constructor.
- Update password-based usage examples in the Python module to use access_token.

The old Basic-header assignment must be removed:

```python
self._authorization = "Basic %s" % userandpass
```

The fail-fast constructor policy is this benchmark's application requirement;
it is not a claim that GitHub defines a Python exception type.

Sources:
https://github.blog/changelog/2020-11-13-token-authentication-required-for-api-operations/
https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api
