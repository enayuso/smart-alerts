from beacon.util.postgres_ops import get_database_connection, delete


def flush_tweet_ids():
    query = "DELETE from latest_tweet_id where 1=1"
    conn = get_database_connection()
    delete(conn, query)


def flush_tweet_data():
    query = "DELETE from tweet_data where 1=1"
    conn = get_database_connection()
    delete(conn, query)
