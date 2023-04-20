import os
from datetime import datetime

import html2text
from atlassian import Confluence
from atlassian.errors import ApiValueError
from langchain.document_loaders.confluence import ConfluenceLoader
from requests import HTTPError
from utils.indexer import confluence as confluence_indexer
from utils.indexer import indexer

confluence_format = "%Y-%m-%dT%H:%M:%S.%fZ"
cql_format = "%Y/%m/%d %H:%M"
filename = "last_updated.txt"

loader = ConfluenceLoader(
    url="https://mercari.atlassian.net/wiki",
    username=os.environ.get("CONFLUENCE_USERNAME"),
    api_key=os.environ.get("CONFLUENCE_API_KEY")
)

confluence = Confluence(
    url="https://mercari.atlassian.net/wiki",
    username=os.environ.get("CONFLUENCE_USERNAME"),
    password=os.environ.get("CONFLUENCE_API_KEY")
)


def iterate_latest_pages():
    indexer = confluence_indexer.ConfluenceIndexer()
    load(indexer)


def iterate_spaces():
    limit = 50
    start = 0
    pages = confluence.get_all_spaces(start=start, limit=limit, space_type='global')
    while len(pages['results']) > 0:
        start += limit
        for page in pages['results']:
            load(space_key=page['key'])
        pages = confluence.get_all_spaces(start=start, limit=limit, space_type='global')
    return pages


def load(indexer: indexer.Indexer, space_key: str = None):
    limit = 10
    start = 0

    docs = []
    metadata_array = []
    page_content_array = []

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_images = True

    if space_key:
        try:
            pages = loader.confluence.get_all_pages_from_space(space=space_key, start=start, limit=limit,
                                                               expand="body.storage.value,history,version")
        except Exception as e:
            print('some error occurred during page procession {}'.format(e))
            return

        while len(pages) > 0:
            try:
                start += limit
                for page in pages:
                    try:
                        doc = loader.process_page(page, include_attachments=True, text_maker=text_maker)
                        doc.metadata['createdBy'] = page['history']['createdBy']['displayName']
                        doc.metadata['createdAt'] = page['history']['createdDate']
                        doc.metadata['space'] = space_key
                        docs.append(doc)
                    except Exception as e:
                        print('some error occurred during page procession {}'.format(e))
                print('calling structurize api for docs')
                # confluence_indexer.ConfluenceIndexer.create_documents(page_content_array, metadata_array)
                docs = []
                pages = loader.confluence.get_all_pages_from_space(space=space_key, limit=10, start=start,
                                                                   expand="body.storage.value,history,version")
            except Exception as e:
                print('some error occurred during pages iteration {}'.format(e))
        return
    else:
        time_resp = read_string_from_file(file_name=filename)
        last_updated = time_resp
        time_object = datetime.strptime(time_resp, confluence_format)
        cql_time = time_object.strftime(cql_format)
        cql = 'type=page+AND+space.type=global+AND+lastmodified>"{}"+ORDER+BY+lastmodified+ASC'.format(cql_time)
        try:
            pages = exec_cql(start=start, limit=limit,
                             expand="body.storage.value,history,version", cql=cql,
                             include_archived_spaces=True)['results']
        except Exception as e:
            print('some error occurred during page procession {}'.format(e))
            return

        while len(pages) > 0:
            try:
                start += limit
                for page in pages:
                    try:
                        doc = loader.process_page(page, include_attachments=True, text_maker=text_maker)
                        doc.metadata['createdBy'] = page['history']['createdBy']['displayName']
                        doc.metadata['createdAt'] = page['history']['createdDate']
                        doc.metadata['space'] = space_key
                        last_updated = page['version']['when']
                        rewrite_file_with_string(file_name=filename, new_string=last_updated)
                        # '2022-09-14T05:43:13.030Z'
                        metadata_array.append(doc.metadata)
                        page_content_array.append(doc.page_content)
                    except Exception as e:
                        print('some error occurred during page procession {}'.format(e))
                print('calling structurize api for docs')
                indexer.create_documents(page_content_array, metadata_array)
                metadata_array = []
                page_content_array = []
                pages = exec_cql(start=start, limit=limit,
                                 expand="body.storage.value,history,version", cql=cql,
                                 include_archived_spaces=True)['results']
                rewrite_file_with_string(file_name=filename, new_string=last_updated)
            except Exception as e:
                print('some error occurred during pages iteration {}'.format(e))
        return


def rewrite_file_with_string(file_name, new_string):
    with open(file_name, 'w') as file:
        file.write(new_string)


def read_string_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            string = file.read().strip()
        return string
    except FileNotFoundError:
        print("File '{}' does not exist. Creating file...".format(file_name))
        with open(file_name, 'w') as file:
            file.write("2010-12-19T16:05:53.910Z")
        return None


def exec_cql(
        cql,
        start=0,
        limit=None,
        expand=None,
        include_archived_spaces=None,
        excerpt=None,
):
    """
    Get results from cql search result with all related fields
    Search for entities in Confluence using the Confluence Query Language (CQL)
    :param cql:
    :param start: OPTIONAL: The start point of the collection to return. Default: 0.
    :param limit: OPTIONAL: The limit of the number of issues to return, this may be restricted by
                    fixed system limits. Default by built-in method: 25
    :param excerpt: the excerpt strategy to apply to the result, one of : indexed, highlight, none.
                    This defaults to highlight
    :param expand: OPTIONAL: the properties to expand on the search result,
                    this may cause database requests for some properties
    :param include_archived_spaces: OPTIONAL: whether to include content in archived spaces in the result,
                                this defaults to false
    :return:
    """
    params = {}
    if start is not None:
        params["start"] = int(start)
    if limit is not None:
        params["limit"] = int(limit)
    if expand is not None:
        params["expand"] = expand
    if cql is not None:
        params["cql"] = cql
    if include_archived_spaces is not None:
        params["includeArchivedSpaces"] = include_archived_spaces
    if excerpt is not None:
        params["excerpt"] = excerpt

    try:
        response = confluence.get("rest/api/content/search", params=params)
    except HTTPError as e:
        if e.response.status_code == 400:
            raise ApiValueError("The query cannot be parsed", reason=e)

        raise

    return response
