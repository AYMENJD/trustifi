# trustifi: Google-trusted Root CA Certificates for Python

trustifi provides **Google-trusted Root CA certificates** for TLS verification.
It is intended as a **drop-in replacement for [certifi](https://pypi.org/project/certifi)**, using Google’s trust
program and policies instead of Mozilla’s.

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
