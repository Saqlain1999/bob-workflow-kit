# Security and sensitive reports

This repository is a catalogue with a local metadata validator. It is not an installer, model gateway, or security assessment of the projects it links.

The validator uses the Python standard library, makes no network requests, and does not run upstream tools. The included GitHub Actions workflow checks repository content; it does not require Bob credentials or other repository secrets.

## Report a catalogue problem

For an incorrect URL, suspicious replacement repository, or misleading safety claim, open an issue with the entry ID and public evidence. Do not attach credentials, private source, exploit details that expose an affected user, or confidential logs.

For a vulnerability in a linked project, follow that project's advertised security policy. Do not use this catalogue's issue tracker as a substitute for the upstream reporting channel.

If you find a vulnerability in this repository's own tooling, use a private reporting channel if one is advertised on the repository's Security page. Otherwise, open a minimal non-sensitive issue requesting a private channel; do not assume private reporting has been configured.

## Use links deliberately

Review upstream source, installation instructions, dependencies, and permissions before executing a tool. A link or license label does not establish that a package is safe, compatible, or appropriate for a particular environment. Source availability and runtime evidence are recorded separately for this reason.
