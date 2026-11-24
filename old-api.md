# Historical GitHub REST authentication contract

This migration profile applies to githubpy 1.1.1 at commit
`a123f203af68f96ad0fcb858d2754849faf542fe`.

The old SDK constructor accepts username/password credentials and an optional
`access_token`. When both are supplied, username/password takes precedence and
produces HTTP Basic authentication. An `access_token` alone produces token
header authentication. Anonymous public requests are supported.

The legacy implementation builds the Basic header using:

```python
self._authorization = "Basic %s" % userandpass
```

These are paraphrased historical migration notes, not a full API specification.
Repository source: https://github.com/michaelliao/githubpy/tree/a123f203af68f96ad0fcb858d2754849faf542fe
Historical deprecation notice: https://developer.github.com/changes/2/
