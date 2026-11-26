# Securomatic: public

What anyone needs to check what Securomatic publishes. Securomatic
assesses the security advisories that scanners report against a
product's container images, and writes OpenVEX documents saying which
ones affect it. Securomatic itself is private; this repository is
public, and is also served at <https://securomatic.dev>.

Each release's VEX document comes with a **basis record**: an in-toto
statement, signed by Securomatic, saying what the document rests on
(the image, the commit, the SBOM, the scan, and hashes of the product
model and rules Securomatic used). The product checks the signature
before attesting the VEX document to its images with its own identity.

| Path | What's in it |
|---|---|
| [keys/](keys/) | Securomatic's public keys, and when each was added or retired |
| [basis/v1.md](basis/v1.md) | The basis record's specification, and how to verify one |
| [brand/](brand/) | Securomatic's avatar |
| [site/](site/) | How securomatic.dev is built from this repository |

More will come: an example workflow for a product to check and attest
the documents Securomatic sends it, and other tools for checking
Securomatic's work.

Securomatic was called autosec until November 2026.

Licensed under the [Apache License 2.0](LICENSE).
