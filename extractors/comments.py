from .base import BaseExtractor


class CommentsExtractor(BaseExtractor):
    nested_extractors = set()
    nested_extractor_threads = 1
    target_table = "comment_raw"

    def prepare_nested_query_variables(self, data):
        return []

    def get_page_info(self, data):
        return data["data"]["organization"]["repository"]["pullRequest"]["comments"]

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
         comments (first: 75, after: {cursor}) {{
          pageInfo {{
            endCursor
            hasNextPage
          }}
          edges {{
            node {{
              author {{
                login
              }}
              authorAssociation
              body
              bodyHTML
              bodyText
              createdAt
              createdViaEmail
              databaseId
            }}
          }}
        }}
      }}
    }}
  }}
}}"""
