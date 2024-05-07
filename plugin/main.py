from flox import Flox, clipboard, ICON_COPY
import requests
import urllib.parse
import json

BASE_URL = "https://scrapbox.io/"
MAX_THREADS = 10
DEFAULT_SEARCH_LIMIT = 10
MAX_CACHE_AGE = 600

class SearchScrapbox(Flox):
    def query(self, query):
        if query != '':
            self._results = self.search(query)
        return self._results

    def search(self, query):
        limit = int(50)
        results = getPages(query, max_results=limit).to_dict()
        for item in results:
            self.result(item)
        return self._results

    def result(self, item):
        url = item["url"]
        if not item['description']:
            self._subtitle = ""
        else:
            self._subtitle = item['description'][0]
        self.add_item(
            title=item['title'],
            subtitle=self._subtitle,
            icon="Images/app.png",
            CopyText=url,
            method=self.browser_open,
            parameters=[url],
            context=[url]
        )

    def context_menu(self, data):
        url = data[0]
        self.add_item(
            title='Copy to clipboard',
            subtitle=url,
            icon=ICON_COPY,
            method=self.copy_to_clipboard,
            parameters=[url]
        )

    def copy_to_clipboard(self, url):
        clipboard.put(url)

class getPages:
    BASE_URL = "https://scrapbox.io/"
    BASEAPI_URL = "https://scrapbox.io/api/pages/"

    def __init__(self, search_terms: str, max_results=None):
        self.session = requests.Session()
        self.search_terms = search_terms
        self.max_results = max_results
        self.pages = self._search()

    def _search(self):
        encoded_search = urllib.parse.quote_plus(self.search_terms)
        args_arr = encoded_search.split("+")
        spec_url = f"{self.BASEAPI_URL}{args_arr[0]}"
        json_data = self.session.get(spec_url).text
        cells = self._parse_html(json_data, args_arr)
        if self.max_results is not None and len(cells) > self.max_results:
            return cells[: self.max_results]
        return cells

    def _parse_html(self, json_data, args):
        results = []
        data = json.loads(json_data)
        pages = data.get("pages", "NO KEY")
        if pages == "NO KEY":
            return results
        else:
            if len(args) == 1:
                for page in pages:
                    res = {}
                    res["title"] = page.get("title", None)
                    res["description"] = page.get("descriptions", None)
                    res["url"] = f"{self.BASE_URL}" + data["projectName"] + "/" + res["title"]
                    results.append(res)
                return results
            else:
                pro_name = args[0]
                args.remove(pro_name)
                comb_args = ' '.join(args) # 0番目はプロジェクト名なので事前に除外する
                spec_url = f"{self.BASEAPI_URL}{pro_name}/search/query?q={comb_args}"
                json_data = self.session.get(spec_url).text
                data2 = json.loads(json_data)
                pages2 = data2.get("pages")

                if len(pages2) == 0:
                    res = {}
                    res["title"] = ' '.join(args) # 新規ページ名
                    res["description"] = ["Create new page in the project"]
                    res["url"] = f"{self.BASE_URL}" + pro_name + "/" + res["title"]
                    results.append(res)
                    return results
                else:
                    for page in pages2:
                        res = {}
                        res["title"] = page.get("title", None)
                        res["description"] = page.get("descriptions", None)
                        res["url"] = f"{self.BASE_URL}" + pro_name + "/" + res["title"]
                        results.append(res)
                    return results

    def to_dict(self, clear_cache=True):
        result = self.pages
        if clear_cache:
            self.pages = ""
        return result

    def to_json(self, clear_cache=True):
        result = json.dumps({"pages": self.pages})
        if clear_cache:
            self.pages = ""
        return result

if __name__ == "__main__":
    SearchScrapbox()
