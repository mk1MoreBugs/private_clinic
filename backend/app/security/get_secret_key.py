def get_secret_key():
    # run command in .backend/ folder:
    # openssl rand -hex 32 > app/security/secret_key.txt
    with open('app/security/secret_key.txt', encoding="utf-8") as f:
        return f.readline()[0:-2]