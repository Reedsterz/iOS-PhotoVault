# Photo Vault v 10.8

This repository contains the code for decrypt files in Photo Vault iOS app version 10.8

## Relevant Files
- './ppv_old.py': script to decrypt photovault files

## How to run

* Requires python3 installed.
* Packages: pip install 'pycryptodome'
* Arguments:
    * -k : refer to the key 'ppv_dateHash' from the keychain in **base64** format
    * -i: the encrypted files are found in /mobile/Containers/Data/Application/com.enchantedcloud.photovault/Library/PPV_Pics
    * -o: path of the decrypted files

### ppv_old.py
```
python ppv_old.py -i <path to encrypted file> -o <path to decrypted file> -k <ppv_dateHash>'
```
