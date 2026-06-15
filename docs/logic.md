- Every article is fetched from sources (`get.py`).
- Every source has a tagging system which may be different from the others, but
nevertheless an article has tags that reflect a function of an article fragment
(`tags.py`).
- Article fragments are used to create class instances ("blocks") that have
a variety of attributes. Some of them are reset upon loading an article, some of
them remain the same. An attribute can carry various information about article
fragments, such as their type, row number, column number and so on (`elems.py`).
- After attributes are set, blocks that are related to block types (such as
subjects, parts of speech and so on, or so called "fixed" columns) become
useless because this information is provided by attributes and are deleted
(`elems.py`).
- Blocks are blocked or prioritized by multiple parameters according to user
settings (`view.py`).
- Row and column numbers are calculated such as to provide a table according to
user settings (`view.py`).
- Logical cells predefined by tags and consisting of one or several blocks are
formatted according to block attributes (`format.py`).
- Final table is drawn. Cells can be navigated using arrows and other hotkeys
(`table.py`).