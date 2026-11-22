# autosec-public

What anyone needs to check what autosec publishes. autosec assesses
the security advisories that scanners report against a product's
container images, and writes OpenVEX documents saying which ones affect
it. autosec itself is private; this repository is public.

Each release's VEX document comes with a **basis record**: an in-toto
statement, signed by autosec, saying what the document rests on (the
image, the commit, the SBOM, the scan, and hashes of the product model
and rules autosec used). The product checks the signature before
attesting the VEX document to its images with its own identity.

| Path | What's in it |
|---|---|
| [keys/](keys/) | autosec's public keys, and when each was added or retired |
| [basis/v1.md](basis/v1.md) | The basis record's specification, and how to verify one |

More will come: an example workflow for a product to check and attest
the documents autosec sends it, and other tools for checking autosec's
work.

Licensed under the [Apache License 2.0](LICENSE).
