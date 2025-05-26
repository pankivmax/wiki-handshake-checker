Вот пример README для твоего скрипта на GitHub — лаконично и понятно:

---

# Wikipedia Six Degrees of Separation Checker

This Python script checks the "Six Degrees of Separation" theory on Wikipedia by finding a chain of Wikipedia article links connecting two given articles.

---

## Description

The script analyzes links in the main content and the References section of Wikipedia articles (on the same language Wikipedia) and attempts to find a path of up to 5 clicks connecting two articles:

* Both input URLs must be from the same Wikipedia language edition.
* Only considers links within the main content and references.
* Only follows links to other Wikipedia articles of the same language.
* Implements rate limiting to avoid making more than a specified number of requests per second.
* Searches both from `url1` to `url2` and from `url2` to `url1`.

---

## Usage

1. Clone the repository or download the script file:

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. Run the script:

```bash
python wiki_six_degrees.py
```

3. Enter the input values when prompted:

* First Wikipedia article URL (e.g. `https://en.wikipedia.org/wiki/Six_degrees_of_separation`)
* Second Wikipedia article URL (e.g. `https://en.wikipedia.org/wiki/American_Broadcasting_Company`)
* Rate limit (max requests per second, e.g. `10`)

4. The script will output the found path(s) or inform if no path was found within 5 hops.

---

## Example

**Input:**

```
https://en.wikipedia.org/wiki/Six_degrees_of_separation
https://en.wikipedia.org/wiki/American_Broadcasting_Company
10
```

**Output:**

```
https://en.wikipedia.org/wiki/American_Broadcasting_Company => [https://en.wikipedia.org/wiki/...] => https://en.wikipedia.org/wiki/Six_degrees_of_separation
https://en.wikipedia.org/wiki/Six_degrees_of_separation => [https://en.wikipedia.org/wiki/...] => https://en.wikipedia.org/wiki/American_Broadcasting_Company
```

---

## Requirements

* Python 3.x
* `requests` library
* `beautifulsoup4` library

Install dependencies with:

```bash
pip install requests beautifulsoup4
```

---

## Notes

* The script respects rate limiting to avoid overloading Wikipedia servers.
* Only Wikipedia internal links (starting with `/wiki/` and without colons or anchors) are followed.
* Paths longer than 5 clicks are not considered.
* Works only with articles from the same language Wikipedia.

---

## License

MIT License


