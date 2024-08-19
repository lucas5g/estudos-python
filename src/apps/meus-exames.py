from PyPDF2 import PdfReader
import re

reader = PdfReader("files/24-07-15.pdf")

len(reader.pages)

text = ''

for page in reader.pages:
    # print(page.extract_text())
    text += page.extract_text()

text
len(text)

regex = r"GLICOSE - JEJUM.*?RESULTADO: (\d+)"

matches = re.findall(regex, text)

matches


