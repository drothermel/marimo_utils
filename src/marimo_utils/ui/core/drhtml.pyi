from collections.abc import Callable
from typing import Protocol

import marimo as mo
from dr_widget.inline import ActiveHtml

class HtmlTag:
    html_name: str
    args: tuple[object, ...]
    kwargs: dict[str, object]
    def __init__(self, html_name: str, *args: object, **kwargs: object) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def _repr_html_(self) -> str: ...

class HtmlRenderable(Protocol):
    def __str__(self) -> str: ...

def cn(*values: str | None) -> str: ...
def html_block(fragment: HtmlRenderable) -> mo.Html | ActiveHtml: ...

TagFactory = Callable[..., HtmlTag]

a: TagFactory
p: TagFactory
i: TagFactory
b: TagFactory
h1: TagFactory
h2: TagFactory
h3: TagFactory
h4: TagFactory
h5: TagFactory
h6: TagFactory
div: TagFactory
span: TagFactory
pre: TagFactory
blockquote: TagFactory
q: TagFactory
ul: TagFactory
ol: TagFactory
li: TagFactory
dl: TagFactory
dt: TagFactory
dd: TagFactory
table: TagFactory
thead: TagFactory
tbody: TagFactory
tfoot: TagFactory
tr: TagFactory
th: TagFactory
td: TagFactory
caption: TagFactory
form: TagFactory
label: TagFactory
select: TagFactory
option: TagFactory
textarea: TagFactory
button: TagFactory
fieldset: TagFactory
legend: TagFactory
article: TagFactory
section: TagFactory
nav: TagFactory
aside: TagFactory
header: TagFactory
footer: TagFactory
main: TagFactory
figure: TagFactory
figcaption: TagFactory
strong: TagFactory
em: TagFactory
mark: TagFactory
code: TagFactory
samp: TagFactory
kbd: TagFactory
var: TagFactory
time: TagFactory
abbr: TagFactory
dfn: TagFactory
sub: TagFactory
sup: TagFactory
audio: TagFactory
video: TagFactory
picture: TagFactory
canvas: TagFactory
details: TagFactory
summary: TagFactory
dialog: TagFactory
script: TagFactory
noscript: TagFactory
template: TagFactory
style: TagFactory
html: TagFactory
head: TagFactory
body: TagFactory
svg: TagFactory
g: TagFactory
area: TagFactory
base: TagFactory
br: TagFactory
col: TagFactory
embed: TagFactory
hr: TagFactory
img: TagFactory
input: TagFactory
link: TagFactory
meta: TagFactory
param: TagFactory
source: TagFactory
track: TagFactory
wbr: TagFactory
circle: TagFactory
rect: TagFactory
ellipse: TagFactory
line: TagFactory
polyline: TagFactory
polygon: TagFactory
path: TagFactory
