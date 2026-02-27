#!/usr/bin/env python3
"""Post a thread to X/Twitter from a text file or stdin.

Usage:
  python3 post_thread.py thread.txt        # post from file (one tweet per blank-line-separated block)
  python3 post_thread.py --dry-run thread.txt  # preview without posting
  python3 post_thread.py --single "Just a single tweet"
"""

import os
import sys
import time
from pathlib import Path

import tweepy
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")


def get_client():
    return tweepy.Client(
        consumer_key=os.environ["X_CONSUMER_KEY"],
        consumer_secret=os.environ["X_CONSUMER_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )


def parse_thread(filepath):
    """Parse a thread file: tweets separated by lines containing only '---'."""
    text = Path(filepath).read_text().strip()
    tweets = [block.strip() for block in text.split("\n---\n") if block.strip()]
    return tweets


def post_thread(tweets, dry_run=False):
    if dry_run:
        for i, tweet in enumerate(tweets, 1):
            chars = len(tweet)
            status = "OK" if chars <= 280 else f"TOO LONG ({chars})"
            print(f"--- Tweet {i}/{len(tweets)} [{chars} chars] {status} ---")
            print(tweet)
            print()
        return

    client = get_client()
    previous_id = None

    for i, tweet in enumerate(tweets, 1):
        if len(tweet) > 280:
            print(f"ABORT: Tweet {i} is {len(tweet)} chars (max 280)")
            sys.exit(1)

        if previous_id is None:
            response = client.create_tweet(text=tweet)
        else:
            response = client.create_tweet(text=tweet, in_reply_to_tweet_id=previous_id)

        previous_id = response.data["id"]
        print(f"Posted {i}/{len(tweets)}: {previous_id}")

        if i < len(tweets):
            time.sleep(1)

    print(f"\nThread posted. First tweet: https://x.com/a_e_deal/status/{tweets and response.data['id']}")


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if "--single" in args:
        idx = args.index("--single")
        text = args[idx + 1] if idx + 1 < len(args) else ""
        if dry_run:
            print(f"[DRY RUN] Would post: {text} [{len(text)} chars]")
        else:
            client = get_client()
            r = client.create_tweet(text=text)
            print(f"Posted: https://x.com/a_e_deal/status/{r.data['id']}")
        return

    filepath = args[0]
    tweets = parse_thread(filepath)
    print(f"Found {len(tweets)} tweets in {filepath}\n")
    post_thread(tweets, dry_run=dry_run)


if __name__ == "__main__":
    main()
