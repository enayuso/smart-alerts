create database twitter;

CREATE TABLE twitter.latest_tweet_id (
    id SERIAL PRIMARY KEY,  -- Auto-incrementing ID
    tweet_id TEXT,
    tweet_user_id VARCHAR(255),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (tweet_id, tweet_user_id)  -- Unique constraint on the combination of tweet_id and user_name
);

CREATE TABLE twitter.tweet_data (
    id SERIAL PRIMARY KEY,          -- Auto-incrementing ID for the table
    tweet_id TEXT UNIQUE,         -- Stores the Twitter ID of the tweet
    tweet_text TEXT NOT NULL,       -- Stores the full text of the tweet
    generated_response TEXT,        -- Stores LLM generated response
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() -- Timestamp of when the row is added
);
-- mock tables for dev testing
CREATE TABLE twitter.latest_tweet_id_mock (
    id SERIAL PRIMARY KEY,  -- Auto-incrementing ID
    tweet_id BIGINT,
    tweet_user_id VARCHAR(255),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (tweet_id, tweet_user_id)  -- Unique constraint on the combination of tweet_id and user_name
);

CREATE TABLE twitter.tweet_data_mock (
    id SERIAL PRIMARY KEY,          -- Auto-incrementing ID for the table
    tweet_id BIGINT UNIQUE,         -- Stores the Twitter ID of the tweet
    tweet_text TEXT NOT NULL,       -- Stores the full text of the tweet
    generated_response TEXT,        -- Stores LLM generated response
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() -- Timestamp of when the row is added
);

