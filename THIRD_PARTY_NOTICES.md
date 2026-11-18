# Third-party notices

This file lists the third-party software and data the project installs, downloads, references or learned from, with the license each one declares. It is a good-faith summary, not legal advice. Licenses were read from the projects' own license files or package metadata when this file was written; check the original sources if it matters to you.

**No third-party source code is copied into this repository.** Nothing listed below is redistributed by this project.

## Runtime dependencies (installed with `pip`, not vendored)

| Package | Version | License |
| --- | --- | --- |
| requests | 2.34.2 | Apache-2.0 |
| cryptography | 50.0.2 | Apache-2.0 OR BSD-3-Clause |
| urllib3 | 2.8.0 | MIT |
| idna | 3.20 | BSD-3-Clause |
| certifi | 2026.10.19 | MPL-2.0 |
| charset-normalizer | 3.5.2 | MIT |
| cffi | 2.1.1 | MIT-0 |
| pycparser | 3.11 | BSD-3-Clause |

The versions of the last six are the ones that were installed when this file was written; `pip` may choose newer compatible ones.

## Development and test dependencies (installed with `pip`, not vendored)

| Package | Version | License |
| --- | --- | --- |
| pytest | 9.2.0 | MIT |
| PyYAML | 6.0.3 | MIT |
| pluggy | 1.7.0 | MIT |
| iniconfig | 2.3.1 | MIT |
| packaging | 26.3 | Apache-2.0 OR BSD-2-Clause |
| Pygments | 2.21.0 | BSD-2-Clause |

## Tools downloaded only by the test workflow (not included, not redistributed)

The test workflow downloads the following release files, checks their SHA-256 hashes against `tools/cores.lock.json` and runs them on the CI machine to validate the generated files. They are stable (non pre-release) releases.

| Tool | Version | License as declared by the project |
| --- | --- | --- |
| Xray-core | v26.3.27 and v26.11.9 | MPL-2.0 |
| sing-box | v1.14.4 | GPL-3.0-or-later with the additional term that no derivative work may use the name or imply association with the application without prior consent |
| Hiddify core | v5.9.8 | GPL-3.0 with Section 7 additional permissions and restrictions (among them: non-commercial use, forks must stay open source and must not use the original name) |
| v2fly geoip data (`geoip.dat`) | 202611080027 | CC BY-SA 4.0 |
| v2fly domain-list-community data (`dlc.dat`, used as `geosite.dat`) | 20261115005626 | MIT |

This project is not a derivative of these tools. It does not use their code and uses their names only to state which versions its output was tested with. It does not use the sing-box or Hiddify names for itself and does not claim any association with them.

## Data referenced by the generated files (downloaded by the user's client, not by this project)

The generated sing-box profile points to rule sets published at `https://raw.githubusercontent.com/Chocolate4U/Iran-sing-box-rules/` (`geosite-ir.srs`, `geoip-ir.srs`), a GPL-3.0 project. The user's own client downloads them from their original location; this project does not copy, host or modify them.

## Projects whose public source or documentation was read for interface facts (no code included)

| Project | License | Used to learn |
| --- | --- | --- |
| Lantern's open-source client backend (`radiance`) and its protocol library (`lantern-box`) | GPL-3.0 | The request format of the service described in `docs/UPSTREAM.md` and the meaning of the protocol options |
| sing-box documentation and source | GPL-3.0-or-later with the additional term above | Configuration syntax and the minimum version of options |
| Xray-core source and Xray-docs-next documentation | MPL-2.0 and CC BY-SA 4.0 | Configuration schema, the absence of a VLESS packet-encoding field, the plain-VLESS safety rule |
| Hysteria | MIT | The URI format and the certificate pin (`pinSHA256`) |
| Hiddify core | GPL-3.0 with additional terms | The behaviour of its link parser (tested with the release binary) |
| v2rayNG | GPL-3.0 | How the pin of a Hysteria2 link is applied (read from its source) |

Facts about a file format or a protocol are not protected code; the implementation in this repository is original. If you believe something is missing or wrong here, please open an issue.

## GitHub Actions used by the workflows

`actions/checkout` and `actions/setup-python` (MIT), pinned to full commit hashes.
