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

```bash
sudo apt install gpg

pip3 install argparse
pip3 install questionary
pip3 install gnupg
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
pyinstaller simplegpg.py --onefile
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
- Handling: if homedir does not exist
- Handling: empty key file 
- Catch Exceptions
- Better representation of decrypted messages

## Other Apps

- Password manager / GPG Key manager: seahorse
- GPG Encrypt/Decrypt applet. openpgp-applet

