import os
import base64
import argparse
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_aes_cbc_pkcs7(encrypted, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted), AES.block_size)

# path_to_encrypted_files = "/Users/reedsterz/Desktop/problemahthisash/files"

# path_to_decrypted_files = "/Users/reedsterz/Desktop/problemahthisash/out/"

# # from keychain.plist with key "ppv_dateHash"
# aes_key_b64 = "PKMwf3Q0lvR/WX3pFajAG8w2NCNvNLWbdZ1bZ7KF6Pk="

def decrypt_file(path_to_encrypted_files, path_to_decrypted_files, aes_key_b64):

    if not os.path.exists(path_to_decrypted_files):
        os.mkdir(path_to_decrypted_files)

    aes_key = base64.b64decode(aes_key_b64)

    for file_name in os.listdir(path_to_encrypted_files):
        print(file_name)

        with open(os.path.join(path_to_encrypted_files, file_name), "rb") as f:
            input_data = f.read()

            # The IV is located at offset 0x2 and is 16 bytes long.
            iv = input_data[2:18]

            # Header is 18 bytes (0x0 for version, 0x1 for options, and 0x2 for 16 bytes IV)
            header_length = 18

            # Last 32 bytes used for HMAC stuff.
            cipher_text = input_data[header_length:-32]

            decrypted_data = decrypt_aes_cbc_pkcs7(cipher_text, aes_key, iv)
            with open(os.path.join(path_to_decrypted_files, file_name), "wb") as out_file:
                out_file.write(decrypted_data)

def main():
    parser = argparse.ArgumentParser(description = "Decrypt PhotoVault v10.8")
    required_args = parser.add_argument_group("required args")
    required_args.add_argument("-i", required=True, help="path to encrypted files")
    required_args.add_argument("-o", required=True, help="path to decrypted files")
    required_args.add_argument("-k", required=True, help="ppv_dateHash value in base64")
    args = parser.parse_args()

    path_to_encrypted_files = args.i
    path_to_decrypted_files = args.o
    aes_key_b64 = args.k

    decrypt_file(path_to_encrypted_files, path_to_decrypted_files, aes_key_b64)

if __name__ == "__main__":
    main()