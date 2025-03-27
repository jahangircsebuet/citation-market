from urllib.parse import urlencode

# build cited by url 
def build_cited_by_url_with_days_info(paper_id):
    base_url = "https://scholar.google.com/scholar"
    params = {
        "hl": "en",
        "as_sdt": "5,44",
        "cites": paper_id,
        "scipsc": "",
        "q": "",
        "scisbd": "1"
    }

    full_url = f"{base_url}?{urlencode(params)}"
    return full_url

if __name__ == "__main__":
    paper_id = "9579430514940149198"
    url = build_cited_by_url_with_days_info(paper_id)
    print(url)