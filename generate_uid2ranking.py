from lxml import html
import requests


def extract_reputation(uid):
    """Lookup a user's reputation.

    Args:
        uid: StackOverflow user id.

    Return:
        That user's reputation.
    """

    page = requests.get('http://stackoverflow.com/users/%d' % uid)
    tree = html.fromstring(page.content)
    return int(tree.xpath('//div[@title="reputation"]/text()')[0].strip())


