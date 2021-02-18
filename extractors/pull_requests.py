from copy import deepcopy

from .base import BaseExtractor
from .comments import CommentsExtractor
from .commits import CommitsExtractor

class PullRequestsExtractor(BaseExtractor):
    nested_extractors = {CommitsExtractor, CommentsExtractor}
    nested_extractor_threads = 16
    target_table = 'pr_raw'

    def prepare_nested_query_variables(self, data):
        for pr in data['data']['search']['edges']:
            query_variables = deepcopy(self.query_variables)
            query_variables['cursor'] = 'null'
            query_variables['pr_number'] = pr['node']['number']
            yield query_variables

    def get_page_info(self, data):
        return data['data']['search']['pageInfo']

    @property
    def query(self):
        return """
{{
  search(query: "repo:{owner}/{repository} is:pr", type: ISSUE, first: 75, 
  after: {cursor}) {{
    pageInfo {{
      startCursor
      endCursor
      hasNextPage
      hasPreviousPage
    }}
    edges {{
      node {{
        ... on PullRequest {{
          ...prFields
        }}
      }}
    }}
  }}
}}

fragment prFields on PullRequest {{
  activeLockReason
  additions
  author {{
    ...actor
  }}
  authorAssociation
  autoMergeRequest {{
    authorEmail
    commitBody
  }}
  baseRefName
  baseRefOid
  body
  bodyHTML
  bodyText
  changedFiles
  checksResourcePath
  checksUrl
  closed
  closedAt
  createdAt
  createdViaEmail
  databaseId
  deletions
  editor {{
    ...actor
  }}
  headRefName
  headRefOid
  hovercard {{
    contexts {{
      message
      octicon
    }}
  }}
  id
  includesCreatedEdit
  isCrossRepository
  isDraft
  lastEditedAt
  locked
  maintainerCanModify
  mergeCommit {{
    ...commit
  }}
  mergeable
  merged
  mergedAt
  mergedBy {{
    ...actor
  }}
  milestone {{
    ...milestone
  }}
  number
  permalink
  potentialMergeCommit {{
    ...commit
  }}
  publishedAt
  resourcePath
  revertResourcePath
  revertUrl
  reviewDecision
  state
  suggestedReviewers {{
    isAuthor
    isCommenter
    reviewer {{
      id
    }}
  }}
  title
  updatedAt
  url
}}

fragment commit on Commit {{
  abbreviatedOid
  additions
  author {{
    name
  }}
  authoredByCommitter
}}

fragment milestone on Milestone {{
  closed
  closedAt
  createdAt
  creator {{
    ...actor
  }}
  description
  dueOn
  id
  number
  progressPercentage
  resourcePath
  title
  updatedAt
  url
}}

fragment actor on Actor {{
  login
}}
"""