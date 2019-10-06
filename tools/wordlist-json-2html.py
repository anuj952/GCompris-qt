#!/usr/bin/python
#
# GCompris - wordlist-json-2html.py
#
# Copyright (C) 2018 Johnny Jazeix <jazeix@gmail.com>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <https://www.gnu.org/licenses/>.

import json

wordsFile="../src/activities/lang/resource/words.json"

with open(wordsFile) as data_file:
    try:
        data = json.load(data_file)
        print("Processing OK " + wordsFile)
    except ValueError as e:
        print(dir(e))
        print("Processing KO " + wordsFile)
        print("Parser error: {0}".format(e.message))

header="""<html dir=\"ltr\" lang=\"fr\">
<head>
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">
</head>
<body>
  <a name=\"words_by_section\" href=\"words_by_section.html\"/>Same list of words by section</a>
  <p></p>
  <a name=\"empty json\" href=\"words.json\"/>Empty json data file ready to be translated</a>
  <hr>
"""

footer= """
</body>
</html>"""

orderedData = {}

with open("words_by_section.html", "w") as section_file:
    section_file.write("""<html dir=\"ltr\" lang=\"fr\">

<head>
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">
</head>
<body>

""")
    for chapter in data:
        for lesson in chapter["content"]:
            lessonName = lesson["name"];
            if lessonName == "otherLesson":
                lessonName = "other"
            section_file.write("  <h1>" + lessonName + "</h1>\n")
            for content in lesson["content"]:
                # store the info for words.html
                orderedData[content["description"]] = {
                    "image": content["image"],
                    "section": lessonName
                    };
                # write in the file
                section_file.write("""      <a name=\""""+content["description"]+"""\" href=\"lang/""" + content["image"] + """\"><img src=\"lang/"""+content["image"] + """\"/></a>
      <p>"""+content["description"]+"""</p>
      <hr/>
""")
    section_file.write(footer)

with open("words.html", "w") as words_file:
    words_file.write(header)
    for key in sorted(orderedData):
        words_file.write("  <a name=\""+key+"\" href=\"lang/"+orderedData[key]["image"]+"\"><img src=\"lang/"+orderedData[key]["image"]+"\"/></a><p>"+key+" ("+orderedData[key]["section"]+")</p><hr/>\n")
    words_file.write(footer)
