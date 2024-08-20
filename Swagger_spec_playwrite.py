import requests
from playwright.sync_api import sync_playwright
import json

def find_api_docs_url(page):
    api_docs_url = None
    search_terms = ['api-docs', 'swagger.json', 'openapi.json']

    def handle_request(request):
        nonlocal api_docs_url
        if request.resource_type in ['xhr', 'fetch']:
            for term in search_terms:
                if term in request.url:
                    api_docs_url = request.url
                    break

    page.on('request', handle_request)
    page.goto('https://betaapi.gemecosystem.com/testExecution/swagger-ui/index.html')
    page.wait_for_timeout(5000)
    return api_docs_url

def fetch_openapi_spec(url):
    try:
        return requests.get(url).json()
    except requests.RequestException as e:
        print(f"Error fetching OpenAPI spec: {e}")
        return None

def save_spec_to_file(spec, filename='openapi_spec.json'):
    if spec:
        with open(filename, 'w') as file:
            json.dump(spec, file, indent=2)
        print(f"OpenAPI specification saved to {filename}.")
    else:
        print("No specification to save.")

def main():
    with sync_playwright() as p:
        page = p.chromium.launch(headless=True).new_page()
        api_docs_url = find_api_docs_url(page)
        if api_docs_url:
            spec = fetch_openapi_spec(api_docs_url)
            save_spec_to_file(spec)
        page.context.browser.close()

if __name__ == "__main__":
    main()
