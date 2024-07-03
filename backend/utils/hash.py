import bcrypt


def hash(val: str) -> str:
    # Generate a salt and hash the password
    return bcrypt.hashpw(val.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_hash(plain_val: str, hashed_val: str) -> bool:
    # Check if the given password matches the hashed password
    return bcrypt.checkpw(plain_val.encode('utf-8'), hashed_val.encode('utf-8'))
