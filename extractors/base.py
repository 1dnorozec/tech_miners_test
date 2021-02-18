import concurrent.futures
import json
from itertools import repeat
from typing import Dict, Set

from .utils.validation import validate_response


class BaseExtractor:
    """
    Base Extractor for Github's Graphql data
    """

    # number of workers for nested extractions
    nested_extractor_threads = 1

    def __init__(
        self,
        query_variables: Dict,
        graphql_session,
        tcp,
        parent_extractors: Set,
        run_timestamp: int,
    ):
        # query variables are essential for extractor, it contains information
        # about query variables and state of cursor
        self.query_variables = query_variables
        self.graphql_session = graphql_session
        self.tcp = tcp

        # This part prevents cycles in instantiations in the future.
        # Let's assume that PR has nested extractor for commit, Commit might
        # have nested extractor for User and User might have nested
        # extractor for Pull Request, thanks to this it will remove already
        # extracted data from nested extractors set. Thanks to that we do
        # not end up in infinite loop, and developer doesn't need to
        # remember what is having which extractor
        self.parent_extractors = parent_extractors
        self.parent_extractors.add(type(self))
        self.nested_extractors -= parent_extractors

        self.run_timestamp = run_timestamp

    def extract_data(self):
        has_next_page = True
        while has_next_page:
            formated_query = self.query.format(**self.query_variables)
            resp = self.graphql_session.post(json={"query": formated_query})
            validate_response(resp)
            json_response = resp.json()

            self.save_data(json_response)

            nested_query_variables = self.prepare_nested_query_variables(json_response)

            page_info = self.get_page_info(json_response)

            for nested_extractor in self.nested_extractors:
                with concurrent.futures.ThreadPoolExecutor(
                    max_workers=self.nested_extractor_threads
                ) as executor:
                    executor.map(
                        self.extract_nested,
                        nested_query_variables,
                        repeat(nested_extractor),
                    )

            self.update_query_variables(cursor=f'"{page_info["endCursor"]}"')
            has_next_page = page_info["hasNextPage"]

    def update_query_variables(self, **kwargs):
        """
        Mostry used to update cursor
        """
        self.query_variables.update(**kwargs)

    def save_data(self, data):
        conn = self.tcp.getconn()
        conn.set_session(readonly=False, autocommit=True)
        cur = conn.cursor()

        cur.execute(
            f"""
            INSERT INTO github.{self.target_table} (raw_data, run_timestamp) 
            VALUES (%s, %s)
            """,
            (json.dumps(data), self.run_timestamp),
        )

        self.tcp.putconn(conn)

    def extract_nested(self, query_variables, extractor):
        """
        start extraction for nested data
        """
        _extractor = extractor(
            query_variables,
            self.graphql_session,
            self.tcp,
            self.parent_extractors,
            self.run_timestamp,
        )
        _extractor.extract_data()

    def prepare_nested_query_variables(self, data):
        """
        extraction specific method. Prepares data that will be needed to be
        used as query variables for nested queries.
        """
        raise NotImplementedError

    def get_page_info(self, data):
        """
        extraction specific method. Get information about page info
        """
        raise NotImplementedError

    @property
    def nested_extractors(self):
        raise NotImplementedError

    @property
    def query(self):
        raise NotImplementedError

    @property
    def target_table(self):
        raise NotImplementedError
