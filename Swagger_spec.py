from seleniumwire import webdriver
import requests
import json
from selenium.webdriver.chrome.options import Options
import time

def find_api_docs_url(driver):
    api_docs_url = None

    # Open the target URL
    # driver.get('https://betaapi.gemecosystem.com/testExecution/swagger-ui/index.html')
    driver.get('https://petstore.swagger.io/index.html')
    time.sleep(5)

    # Iterate through the requests captured by Selenium Wire
    for request in driver.requests:
        if request.response and request.url.endswith(('api-docs', 'swagger.json', 'openapi.json')):
            api_docs_url = request.url
            break
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
    # Initialize the Selenium Wire browser (headless)
    # options = Options()
    options=Options()
    options.add_argument('--headless')  # Run in headless mode

    driver = webdriver.Chrome(options=options)

    try:
        api_docs_url = find_api_docs_url(driver)
        if api_docs_url:
            spec = fetch_openapi_spec(api_docs_url)
            save_spec_to_file(spec)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
