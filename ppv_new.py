import sqlite3, argparse, os, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def decrypt(ciphertext, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    return aes.decrypt(pad(ciphertext, 16))

def getRecords(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e) 

    c = conn.cursor()
    c.execute("""
    select
    modifiedDate, createdDate, syncId, encryptionKey, trashedDate, fileType
    from
    ecdPersistentMediaItem
    """)

    records = c.fetchall()
    dict_ppv = {}

    for record in records:
        dict_ppv[record["syncId"]] =  {}
        dict_ppv[record["syncId"]]["fileType"] = record["fileType"]
        dict_ppv[record["syncId"]]["encryptionKey"] = record["encryptionKey"]
        dict_ppv[record["syncId"]]["createdDate"] = record["createdDate"]
        dict_ppv[record["syncId"]]["modifiedDate"] = record["modifiedDate"]
        dict_ppv[record["syncId"]]["trashedDate"] = record["trashedDate"]

    return dict_ppv

def output_file(input_path, dict_ppv, path_to_decrypted_files):

    # Get a list of files in the directory
    encrypted_file_list = os.listdir(input_path)

    for file in encrypted_file_list:
        filename, ext = file.split('.')
        
        if('_' in filename):
            filename, size = file.split('_')
        else:
            size = ""

        key = base64.b64decode(dict_ppv[filename]["encryptionKey"])

        full_path = "{}/{}".format(input_path, file)
        data = open(full_path, mode='rb').read()
        iv = data[0:16] 
        cipherText = data[16:]

        plaintext = decrypt(cipherText, key, iv)

        full_output_path = "{}/{}".format(path_to_decrypted_files, file)
        f = open(full_output_path, 'wb')
        f.write(plaintext)
        f.close()

def main():
    parser = argparse.ArgumentParser(description = "Decrypt PhotoVault v14.6")
    required_args = parser.add_argument_group("required args")
    required_args.add_argument("-i", required=True, help="path to encrypted files")
    required_args.add_argument("-o", required=True, help="path to decrypted files")
    required_args.add_argument("-k", required=True, help="path to ppv.ecd database")
    args = parser.parse_args()

    path_to_encrypted_files = args.i
    path_to_decrypted_files = args.o
    ppv_ecd_db = args.k

    dict_ppv = getRecords(ppv_ecd_db)
    output_file(path_to_encrypted_files, dict_ppv, path_to_decrypted_files)

if __name__ == "__main__":
    main()