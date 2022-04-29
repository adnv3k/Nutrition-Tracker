class Endpoints:
    def __init__(self):
        self.url = "https://api.nal.usda.gov/fdc/v1/foods/"

    def url(self):
        return self.url

    def end_list(self, api_key, page_size=200, page_number=1, sort_by="lowercaseDescription.keyword", sort_order="desc"):
        if api_key is None:
            return "API Key required."
        payload = {
            "api_key": api_key, page_size: "page_size", "page_number": page_number,
            "sort_by": sort_by, "sort_order": sort_order}
        return f"{self.url}list", payload

    def end_search(self, api_key, query=None, description="SR Legacy"):
        if description is None:
            description = ["Branded", "SR Legacy"]
        if api_key is None:
            return "API Key required."
        payload = {
            "api_key": api_key, "query": query, "description": description
        }
        return f"{self.url}list", payload


if __name__ == '__main__':
    print(Endpoints().end_list(api_key="1"))