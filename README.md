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

Based on Python 3.

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

Executable Linux / Ubuntu distro

```bash
./dist/simplegpg
```

## Release 

```bash
pyinstaller simplegpg.py --onefile
```

## TODO
- Handling: if homedir does not exist
- Handling: empty key file 
- Catch Exceptions
- Better representation of decrypted messages


