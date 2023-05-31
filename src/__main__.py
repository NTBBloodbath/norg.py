from src.parser import NorgParser

# Test it out
data = """
* Heading 1
This i sosme information here
** Heading 2
- List item 1
-- List item 2
Plain text
(x) Task 1
- Task 2
~ Label 1
~ Label 2
"""

parser = NorgParser()
result = parser.parse(data)
for r in result:
    print(r)
