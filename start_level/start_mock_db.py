url_database = {
    #empty for now
}

def add_to_url_db(key: str, value: str):
    # just using type hints for fun here
    url_database[key] = value


def get_url_database() -> dict: # return type hinting
    return url_database