"""
Endpoints related to pages.

https://xtools.readthedocs.io/en/stable/api/page.html
"""

from . import base


def article_info(project: str, article: str):
    """
    Return basic information about an article, such as page views, watchers, edits counts; author; assessment.

    https://xtools.readthedocs.io/en/stable/api/page.html#article-info

    :param project:
    :param article:
    :return:
    """
    return base.get("/page/articleinfo/%s/%s" % (project, article))