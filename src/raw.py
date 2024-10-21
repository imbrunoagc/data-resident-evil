from scrapy.collect import collect
from scrapy.paramns import COOKIES, HEADERS

print(HEADERS, COOKIES)

FILE_PATH = './data/raw/raw_characters.json'
collect(COOKIES, HEADERS).run_collect(FILE_PATH)