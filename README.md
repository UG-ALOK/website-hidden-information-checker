# Website Hidden Information Checker (WHIC)

A Python-based website reconnaissance and information inspection tool.

Website Hidden Information Checker (WHIC) helps users inspect configured website paths and review HTTP response information for authorized website administration and defensive security testing.

Features

- Inspect configured website paths.
- Display HTTP response status codes.
- Identify responses such as "200 OK", "401 Unauthorized", and "403 Forbidden".
- Display request errors and unreachable-path results.
- Provide readable terminal output.
- Support compatible Python environments, including Termux and Linux.

«Note: An HTTP status code alone does not confirm that a path is an admin panel, that sensitive information is exposed, or that a vulnerability exists.»

Requirements

- Python 3
- Git
- Termux or a compatible Linux environment
- Internet connectivity for remote website checks

Installation

Clone the repository:
```bash
git clone https://github.com/UG-ALOK/website-hidden-information-checker.git
```
Open the project directory:
```bash
cd website-hidden-information-checker
```
For Termux, install the required system packages:
```bash
bash install.sh
```
Usage

Run the actual Python entry-point script included in the repository:
```bash
python WHIC.py
```
Replace "WHIC.py" with the existing script's filename.

Responsible Use

- Test only websites you own or have explicit permission to assess.
- Respect authentication, access controls, and website policies.
- Do not use this tool for unauthorized access or unlawful activity.
- Verify results manually before drawing security conclusions.

Disclaimer

This project is provided for educational and authorized testing purposes. Use of the software is subject to the terms in "DISCLAIMER.md" (DISCLAIMER.md).

Contributing

Contributions that improve documentation, reliability, compatibility, and legitimate defensive security use are welcome.

License

No license is specified by default. A suitable license must be added before the project is distributed under specific open-source licensing terms.
