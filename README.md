# trustifi: Google-trusted Root CA Certificates
[![Version](https://img.shields.io/pypi/v/trustifi?style=flat&logo=pypi&label=Trustifi)](https://pypi.org/project/trustifi) [![Downloads](https://static.pepy.tech/personalized-badge/trustifi?period=month&units=none&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/trustifi)

trustifi provides **Google-trusted Root CA certificates** for TLS verification.
It is intended as a **drop-in replacement for [certifi](https://pypi.org/project/certifi)**, using Google’s **TLS-only** trust model instead of Mozilla’s **general-purpose** root store.

It is currently used by [**RedC**](https://github.com/AYMENJD/redc).

## Installation

`trustifi` can be installed using `pip`:
```bash
pip install trustifi
```

## Usage

To reference the installed certificate authority (CA) bundle, you can use the
built-in function:

```python
>>> import trustifi
>>> trustifi.where()
'/usr/local/lib/python3.7/site-packages/trustifi/cacert.pem'
```

Or from the command line:

```bash
python -m trustifi
/usr/local/lib/python3.7/site-packages/trustifi/cacert.pem
```
