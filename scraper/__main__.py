import json
import os
import sys
import argparse


from scraper.result import Result
from scraper.twitter_scraper import Twitter_Scraper

try:
    from dotenv import load_dotenv

    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file\n")
except Exception as e:
    print(f"Error loading .env file: {e}")


def main():
    global scraper
    try:
        parser = argparse.ArgumentParser(
            add_help=True,
            usage="python scraper [option] ... [arg] ...",
            description="Twitter Scraper is a tool that allows you to scrape tweets from twitter without using Twitter's API.",
        )

        try:
            parser.add_argument(
                "--mail",
                type=str,
                default=os.getenv("TWITTER_MAIL"),
                help="Your Twitter mail.",
            )

            parser.add_argument(
                "--user",
                type=str,
                default=os.getenv("TWITTER_USERNAME"),
                help="Your Twitter username.",
            )

            parser.add_argument(
                "--phone",
                type=str,
                default=os.getenv("TWITTER_PHONE"),
                help="Your Twitter username.",
            )

            parser.add_argument(
                "--filePath",
                type=str,
                default=None,
                help="Your Save File Path.",
            )

            parser.add_argument(
                "--cookiesPath",
                type=str,
                default=None,
                help="Your Save File Path.",
            )
            parser.add_argument(
                "--password",
                type=str,
                default=os.getenv("TWITTER_PASSWORD"),
                help="Your Twitter password.",
            )

            parser.add_argument(
                "--login",
                action='store_true',
                default=False,
                help="Your Save File Path.",
            )
        except Exception as e:
            print(f"Error retrieving environment variables: {e}")
            sys.exit(1)

        parser.add_argument(
            "-t",
            "--tweets",
            type=int,
            default=50,
            help="Number of tweets to scrape (default: 50)",
        )

        parser.add_argument(
            "-u",
            "--username",
            type=str,
            default=None,
            help="Twitter username. Scrape tweets from a user's profile.",
        )

        parser.add_argument(
            "-ht",
            "--hashtag",
            type=str,
            default=None,
            help="Twitter hashtag. Scrape tweets from a hashtag.",
        )

        parser.add_argument(
            "-ntl",
            "--no_tweets_limit",
            nargs='?',
            default=False,
            help="Set no limit to the number of tweets to scrape (will scrap until no more tweets are available).",
        )

        parser.add_argument(
            "-q",
            "--query",
            type=str,
            default=None,
            help="Twitter query or search. Scrape tweets from a query or search.",
        )

        parser.add_argument(
            "-d",
            "--driver",
            type=str,
            default=None,
            help="Twitter query or search. Scrape tweets from a query or search.",
        )

        parser.add_argument(
            "-f",
            "--firefox",
            type=str,
            default=None,
            help="Twitter query or search. Scrape tweets from a query or search.",
        )

        parser.add_argument(
            "-p",
            "--proxy",
            type=str,
            default=None,
            help="Twitter query or search. Scrape tweets from a query or search.",
        )

        parser.add_argument(
            "-a",
            "--add",
            type=str,
            default="",
            help="Additional data to scrape and save in the .csv file.",
        )

        parser.add_argument(
            "--latest",
            action="store_true",
            help="Scrape latest tweets",
        )

        parser.add_argument(
            "--top",
            action="store_true",
            help="Scrape top tweets",
        )

        args = parser.parse_args()

        USER_MAIL = args.mail
        USER_UNAME = args.user
        USER_PHONE = args.phone
        COOKIES_PATH = args.cookiesPath
        USER_PASSWORD = args.password
        DRIVER_PATH = args.driver
        PROXY = args.proxy
        FIREFOX_PATH = args.firefox
        FILE_PATH = args.filePath or os.getenv("FILE_PATH")
        LOGINT = args.login
        if not FILE_PATH and not LOGINT:
            print(json.dumps(Result.fail_with_msg("File path must be a valid string. Please check your .env file.").to_dict()))
            sys.exit(1)

        # if USER_UNAME is None:
        #     print(json.dumps(Result.fail_with_msg("Twitter Username is None").to_dict()))
        #     sys.exit(1)
        #
        # if USER_PASSWORD is None:
        #     print(json.dumps(Result.fail_with_msg("Twitter Password is None").to_dict()))
        #     sys.exit(1)

        tweet_type_args = []

        if args.username is not None:
            tweet_type_args.append(args.username)
        if args.hashtag is not None:
            tweet_type_args.append(args.hashtag)
        if args.query is not None:
            tweet_type_args.append(args.query)
        if args.login is not None and args.login:
            tweet_type_args.append(args.login)

        additional_data: list = args.add.split(",")

        if len(tweet_type_args) > 1:
            print(json.dumps(
                Result.fail_with_msg("Please specify only one of --username, --hashtag, or --query.").to_dict()))
            sys.exit(1)

        if args.latest and args.top:
            print(json.dumps(Result.fail_with_msg("Please specify either --latest or --top. Not both.").to_dict()))
            sys.exit(1)

        scraper = Twitter_Scraper(
            mail=USER_MAIL,
            username=USER_UNAME,
            password=USER_PASSWORD,
            user_phone=USER_PHONE,
            file_path=os.path.normpath(FILE_PATH) if FILE_PATH is not None else '',
            cookies_path=os.path.normpath(COOKIES_PATH) if FILE_PATH is not None else None,
            proxy=PROXY,
            driver_path=DRIVER_PATH,
            firefox_path=FIREFOX_PATH
        )

        if USER_UNAME is not None and USER_PASSWORD is not None and LOGINT:
            scraper.login()
            if scraper.driver:
                scraper.driver.quit()
        else:
            scraper.scrape_tweets(
                max_tweets=args.tweets,
                no_tweets_limit=args.no_tweets_limit if args.no_tweets_limit is not None else True,
                scrape_username=args.username,
                scrape_hashtag=args.hashtag,
                scrape_query=args.query,
                scrape_latest=args.latest,
                scrape_top=args.top,
                scrape_poster_details="pd" in additional_data,
            )
            scraper.save_to_json()
            if scraper.driver:
                scraper.driver.quit()
    except KeyboardInterrupt:
        print(json.dumps(Result.fail_with_msg("Script Interrupted by user. Exiting...").to_dict()))
        if scraper and scraper.driver:
            scraper.driver.close()
        sys.exit(1)
    except Exception as e:
        print(json.dumps(Result.fail_with_msg(f"Error: {e}").to_dict()))
        if scraper and scraper.driver:
            scraper.driver.close()
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
