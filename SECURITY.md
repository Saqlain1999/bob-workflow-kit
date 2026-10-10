# Reporting sensitive issues

This kit writes a small set of user configuration files. It does not need credentials or execute remote code during installation. Unexpected writes, traversal, unsafe removal, or unintended disclosure are appropriate security reports.

If the public repository has GitHub private vulnerability reporting enabled, use **Security → Report a vulnerability**. If that channel is unavailable, open an issue requesting a private reporting contact without publishing sensitive details or a working exploit against other users.

For non-sensitive defects, a minimal reproduction using temporary directories is ideal. Include the package version, OS/Python version, relevant command, expected result, and observed result. Replace user-specific paths and secrets with harmless examples.

The project does not currently promise a response SLA or a supported-version maintenance window. Release status and known limitations belong in [compatibility](docs/compatibility.md) and [validation](VALIDATION.md).
