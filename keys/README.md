# autosec's public keys

autosec signs basis records with these keys (ECDSA P-256). A key's id
is the sha256 of its DER-encoded SubjectPublicKeyInfo, given as the
`hint` in a basis record's bundle. Each file is named for the first 12
characters of its id.

A product should trust the key it has pinned on its own protected
branch; this list is for finding a key and checking it from outside.

| Key | Id | Added | Retired |
|---|---|---|---|
| [ea0c34b47c83.pem](ea0c34b47c83.pem) | `ea0c34b47c83b8f63295104ab6ca3d3045511501d55a8abbd17e43c2ae18f971` | 2026-11-21 | |

To check a key's id:

```sh
openssl pkey -pubin -in ea0c34b47c83.pem -outform DER | shasum -a 256
```
