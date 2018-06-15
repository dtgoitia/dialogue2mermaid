import json
import re


def remove_comments(src: str) -> str:
    comment_regex_pattern = re.compile('\s*[^:]\/\/[^\\n]*\\n')
    return re.sub(comment_regex_pattern, '', src)


def load_dialogue(path: str):
    with open(path) as fd:
        content = remove_comments(fd.read())
        return json.loads(content)
