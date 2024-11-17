from beacon.util.postgres_ops import get_database_connection, execute_query


def tweet_id_table(mock: bool) -> str:
    _tweet_id_table = "latest_tweet_id"
    return _tweet_id_table if not mock else _tweet_id_table + "_mock"


def tweet_data_table(mock: bool) -> str:
    _tweet_data_table = "tweet_data"
    return _tweet_data_table if not mock else _tweet_data_table + "_mock"


def get_latest_tweet_id(tweet_user_id, mock):

    conn = get_database_connection()
    query = f"""
        SELECT tweet_id FROM {tweet_id_table(mock)}
        where tweet_user_id = %s
        ORDER BY id DESC
        LIMIT 1
    """
    values = (tweet_user_id,)

    with conn.cursor() as cur:
        cur.execute(query, values)
        result = cur.fetchone()
        if result:
            return result[0]  # Extract the tweet_id from the tuple
        else:
            return None  # Return none if nothing is returned


def persist_disaster_event(tweet_id, tweet, gen_text, mock):
    """Inserts disaster-related tweet data into the database."""
    conn = get_database_connection()
    query = f"""
        INSERT INTO {tweet_data_table(mock)} (tweet_id, tweet_text, generated_response)
        VALUES (%s, %s, %s)
        ON CONFLICT (tweet_id) DO NOTHING
        """
    values = (tweet_id, tweet, gen_text)
    execute_query(conn, query, values)


def persist_latest_tweet_id(tweet_id, tweet_user_id, mock):
    """Inserts or updates the latest tweet ID."""
    conn = get_database_connection()
    query = f"""
        INSERT INTO {tweet_id_table(mock)} (tweet_id, tweet_user_id)
        VALUES (%s, %s)
        ON CONFLICT (tweet_id, tweet_user_id) DO NOTHING
        """
    values = (tweet_id, tweet_user_id)  # Note the comma to ensure a tuple
    execute_query(conn, query, values)
