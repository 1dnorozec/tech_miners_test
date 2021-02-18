from .base import BaseExtractor


class CommitsExtractor(BaseExtractor):
    nested_extractors = set()
    nested_extractor_threads = 1
    target_table = "commit_raw"

    def prepare_nested_query_variables(self, data):
        return []

    def get_page_info(self, data):
        return data["data"]["organization"]["repository"]["pullRequest"]["commits"]

    @property
    def query(self):
        return """
{{
	organization(login: "{owner}") {{
    id
    repository(name: "{repository}") {{
    	id
      pullRequest(number: {pr_number}) {{
         id
         commits (first: 100, after: {cursor}) {{
          pageInfo {{
            endCursor
            hasNextPage
          }}
          edges {{
            node {{
              commit {{
                abbreviatedOid
                additions
                changedFiles
              }}
            }}
          }}
        }}
      }}
    }}
  }}
}}
"""
