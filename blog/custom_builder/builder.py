from bs4 import BeautifulSoup
import markdown
import sys
import os 
import re
from collections import defaultdict
from typing import List, Dict, Optional
from jinja2 import Environment, Template, FileSystemLoader, select_autoescape

FP_ROOT_SRC = os.path.abspath(os.path.dirname(__file__))
FP_ROOT_BUILD = os.path.join(FP_ROOT_SRC,'..')
FP_ROOT_LIVE = os.path.join(FP_ROOT_BUILD,'..')
LIVE_URL = 'https://github.com/Benno4president/Benno4president.github.io/blob/main/blog'

env = Environment(
    loader=FileSystemLoader(FP_ROOT_SRC+'/html'),
    autoescape=select_autoescape()
)

class WebObject:
    __current_id = -1
    @classmethod 
    def __next_id(cls):
        cls.__current_id += 1
        return cls.__current_id  
    def __init__(self, img_filename: Optional[str] = None) -> None:
        self._img_name_live = LIVE_URL + '/input/' + (img_filename or 'shrek.jpg') + '?raw=true'
        self._id = self.__next_id()
        self.name: str = ''
        self.date: str = ''
        self.page: str = ''
        self.description: str = ''
        self.content: List[str] = []

class Webpage:
    def __init__(self) -> None:
        self.components: List[WebObject] = []
    def add_component(self, com:WebObject):
        self.components.append(com)

def build():
    """     
    """
    out = Webpage()

    files: List[List[str]] = []
    for fp in os.scandir(FP_ROOT_BUILD+'/input'):
        if not fp.name.endswith('.md'):
            continue
        file_lines = open(fp,'r').readlines()
        files.append(file_lines)
    
    """
    1. !PAGE [Name] -> appended to page by that name
    2. ![xx](yy) for img
    """
    for fil in files:
        component = WebObject()
        try:
            meta_i = fil.index('|||\n', 1)
        except ValueError as e:
            print(e, f"""
                |||
                name: Chaos
                date: 2023-12-27
                page: About
                |||
                Use format for metadata in all md docs.

                {fil[:6]}
                """)
            exit()
        _meta = fil[:meta_i]
        def _meta_get(key:str):
            for x in _meta:
                if x.startswith(f'{key}: '):
                    return x[x.index(' '):].strip()
        component.name = _meta_get('name')
        component.date = _meta_get('date')
        component.page = _meta_get('page')
        component.description = _meta_get('description')
        component.content = fil[meta_i:]

        out.add_component(component)
            

    template: Template = env.get_template("test_2.html.jinja")
    html = template.render(webpage=out)

    css_str = open(FP_ROOT_SRC+'/css/test_1.css').read()

    doc = html.replace('</head>', f'\n<style>\n{css_str}\n</style/\n</head>\n')

    with open(FP_ROOT_LIVE+'/test.html', 'w') as fp:
        fp.write(doc)
        print('wrote to file')
    return doc


if __name__ == '__main__':
    html = build()
    #print(html)