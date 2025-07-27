import json
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class GoogleImagesCookieExtractor:
    def __init__(self, remote_addr=None, headless=True, timeout=30):
        self.driver = None
        self.remote_addr = remote_addr
        self.headless = headless
        self.timeout = timeout
        self.is_remote = remote_addr is not None

    def setup_driver(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
        options.add_argument('--lang=zh-CN')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        if self.headless:
            options.add_argument('--headless=new')
        
        if self.is_remote:
            try:
                self.driver = webdriver.Remote(
                    command_executor=self.remote_addr,
                    options=options
                )
                self.driver.set_page_load_timeout(self.timeout)
                self.driver.set_script_timeout(self.timeout)
                self.driver.implicitly_wait(0)
                try:
                    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                except Exception:
                    pass
            except Exception:
                sys.exit(1)
        else:
            self.driver = webdriver.Chrome(options=options)
            self.driver.set_page_load_timeout(self.timeout)
            self.driver.set_script_timeout(self.timeout)
            self.driver.implicitly_wait(0)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def wait_page_ready(self):
        try:
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except Exception:
            pass

    def handle_cookie_consent(self):
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "button"))
            )
            for btn in self.driver.find_elements(By.TAG_NAME, "button"):
                if btn.text.strip() in ("全部接受", "Accept all"):
                    btn.click()
                    break
        except Exception:
            pass

    def extract_cookie(self):
        cookies = self.driver.get_cookies()
        cookie_str = '; '.join(f"{c['name']}={c['value']}" for c in cookies)
        return cookie_str

    def quick_run(self):
        self.setup_driver()
        self.driver.get('https://images.google.com')
        self.wait_page_ready()
        self.handle_cookie_consent()
        search_url = "https://lens.google.com/uploadbyurl?url=https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png"
        self.driver.get(search_url)
        self.wait_page_ready()
        cookie = self.extract_cookie()
        self.driver.quit()
        
        if cookie:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            return {"time": now, "cookie": cookie}
        return None

def main():
    remote_addr = None  # 默认使用本地模式
    # 如果需要使用远程模式，取消下面的注释并设置地址
    # remote_addr = 'http://localhost:4444/wd/hub'
    extractor = GoogleImagesCookieExtractor(
        remote_addr=remote_addr,
        headless=True, 
        timeout=30
    )
    result = extractor.quick_run()
    if result:
        print("cookie获取成功！")
        fname = "google_images_cookie_result.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        print("cookie获取失败 ...")

if __name__ == "__main__":
    main()
