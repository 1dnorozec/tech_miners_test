import argparse
import os
from datetime import datetime

from psycopg2.pool import ThreadedConnectionPool

from utils.github_graphql_client import GithubGrapqhlClient
from extractors.pull_requests import PullRequestsExtractor

MAX_WORKERS = 32
GITHUB_GRAPHQL_URL = 'https://api.github.com/graphql'


def main():
    with GithubGrapqhlClient(GITHUB_GRAPHQL_URL, auth_token) as session:

        query_variables = {
            'owner': owner,
            'repository': repo,
            'cursor': 'null'
        }

        pr_extractor = PullRequestsExtractor(
            query_variables,
            session,
            tcp,
            set(),
            run_timestamp
        )

        pr_extractor.extract_data()



if __name__ == '__main__':

    # pass owner and repository as arguments to file
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", type=str)
    parser.add_argument("--repo", type=str)

    args = parser.parse_args()

    owner = args.owner
    repo = args.repo

    # Database info and github auth token should be stored as env variables
    auth_token = os.environ["AUTH_TOKEN"]
    host = os.environ["HOST"]
    port = os.environ["PORT"]
    database = os.environ["DATABASE"]
    user = os.environ["USER"]
    password = os.environ["PASSWORD"]

    # create threaded connections pool
    tcp = ThreadedConnectionPool(1, MAX_WORKERS, host=host, port=port,
                               user=user, password=password)

    # timestamp of run as integer
    run_timestamp = datetime.now().timestamp()

    main()