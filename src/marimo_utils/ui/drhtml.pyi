from collections.abc import Callable
from enum import StrEnum
from typing import Protocol

import marimo as mo
from dr_widget.inline import ActiveHtml

class HtmlTag:
    html_name: str
    args: tuple[object, ...]
    kwargs: dict[str, object]
    def __init__(
        self, html_name: str, *args: object, **kwargs: object
    ) -> None: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

TagFn = Callable[..., HtmlTag]

class HtmlRenderable(Protocol):
    def __str__(self) -> str: ...

def cn(*values: str | StrEnum | None) -> str: ...

def html_block(fragment: HtmlRenderable) -> mo.Html | ActiveHtml: ...

a: TagFn
p: TagFn
i: TagFn
b: TagFn
h1: TagFn
h2: TagFn
h3: TagFn
h4: TagFn
h5: TagFn
h6: TagFn
div: TagFn
span: TagFn
pre: TagFn
blockquote: TagFn
q: TagFn
ul: TagFn
ol: TagFn
li: TagFn
dl: TagFn
dt: TagFn
dd: TagFn
table: TagFn
thead: TagFn
tbody: TagFn
tfoot: TagFn
tr: TagFn
th: TagFn
td: TagFn
caption: TagFn
form: TagFn
label: TagFn
select: TagFn
option: TagFn
textarea: TagFn
button: TagFn
fieldset: TagFn
legend: TagFn
article: TagFn
section: TagFn
nav: TagFn
aside: TagFn
header: TagFn
footer: TagFn
main: TagFn
figure: TagFn
figcaption: TagFn
strong: TagFn
em: TagFn
mark: TagFn
code: TagFn
samp: TagFn
kbd: TagFn
var: TagFn
time: TagFn
abbr: TagFn
dfn: TagFn
sub: TagFn
sup: TagFn
audio: TagFn
video: TagFn
picture: TagFn
canvas: TagFn
details: TagFn
summary: TagFn
dialog: TagFn
script: TagFn
noscript: TagFn
template: TagFn
style: TagFn
html: TagFn
head: TagFn
body: TagFn
svg: TagFn
g: TagFn
area: TagFn
base: TagFn
br: TagFn
col: TagFn
embed: TagFn
hr: TagFn
img: TagFn
input: TagFn
link: TagFn
meta: TagFn
param: TagFn
source: TagFn
track: TagFn
wbr: TagFn
circle: TagFn
rect: TagFn
ellipse: TagFn
line: TagFn
polyline: TagFn
polygon: TagFn
path: TagFn
