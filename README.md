# Fish Finder

The fastest way to locate dining hall fish at the University of Michigan
---
## Setup

Just clone, `pipenv install`, then run `python3 -m src.generate` (or something similar). It should create `index.html` in the `out` directory.

I would reccomend just pointing to the out folder, and the running `generate.py` every once in a while (maybe hourly)

Checks up to 15 days into the future.

---
#### Note
The university made a change that uses a cert not in the default requests bundle.

This program assumes you've loaded their [intermediate cert](https://its.umich.edu/computing/web-mobile/certificate-services/incommon) (2032 InCommon RSA Server CA 2) into your system bundle and that it's located at `/etc/ssl/certs/ca-certificates.crt`

