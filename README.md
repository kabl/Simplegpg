# SimpleGPG

SimpleGPG is a thin wrapper over `OpenPGP` respective the `gpg` command in linux. 
SimpleGPG provides a simple text user interface where it guides the user through.
SimpleGPG implements no crypto functionalities. It's a representation layer 
for the user. OpenPGP is used for the crypto operations. 

OpenPGP is a powerful command line tool. The drawback is, that it has many options. 
Just a simple operation needs a bunch of command line arguments.

Interoperability is a key feature. All crypto operation inputs and outputs are based
on the PGP format. Therefore SimpleGPG can be used in addition to OpenPGP or other PGP
tools.

## Dependencies

Environment:
 - Python 3.8
 - gpg (GnuPG) 2.2.19
 - Ubuntu 20.04.2 LTS.

### Global
```bash
sudo apt install gpg

pip3 install argparse
pip3 install questionary
pip3 install python-gnupg
pip3 install pyperclip
```

### With venv

```bash
# Create venv environment
virtualenv venv

# Activate venv
source venv/bin/activate

# Install requirements
python3 -m pip install -r requirements.txt

# Leave environment
deactivate
```

## Execute

Directly with Python

```bash
python3 simplegpg.py
```

Executable Linux / Requires at least Ubuntu 20.04.2 LTS.

```bash
./dist/simplegpg
```

## Release 

```bash

# Linux bundle
pyinstaller simplegpg.py --onefile --clean --name simplegpg-linux

# Mac bundle
pyinstaller simplegpg.py --onefile --clean --name simplegpg-mac

```

## Issues

Running on a VM may cause some issues with gpg. As gpg will show a window to enter 
the password for the keystore. Workaround:

```bash
GPG_TTY=$(tty)
export GPG_TTY
./dist/simplegpg
```

## TODO
- Delete keys (requires the fingerprint of the key)
- [x] Handling: if homedir does not exist
- [x] Handling: empty key file 
- [x] Catch Exceptions
- [x] Better representation of decrypted messages

## Other Apps

- Password manager / GPG Key manager: seahorse
- GPG Encrypt/Decrypt applet. openpgp-applet

