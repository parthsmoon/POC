from aloe import world, after, before
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from time import sleep
from zapv2 import ZAPv2
from pprint import pprint

@before.all
def start_program():
    connect_to_zap()
    firefox_profile = prepare_firefox_profile()
    open_drivers(firefox_profile)
    sleep(5)

def connect_to_zap():
    world.zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'})

def prepare_firefox_profile():
    zap_proxy_host = "127.0.0.1"
    zap_proxy_port = 8080
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("network.proxy.type", 1)
    firefox_profile.set_preference("network.proxy.http", zap_proxy_host)
    firefox_profile.set_preference("network.proxy.http_port", int(zap_proxy_port))
    firefox_profile.set_preference("network.proxy.ssl",zap_proxy_host)
    firefox_profile.set_preference("network.proxy.ssl_port", int(zap_proxy_port))
    firefox_profile.set_preference("browser.startup.homepage", "about:blank")
    firefox_profile.set_preference("startup.homepage_welcome_url", "about:blank")
    firefox_profile.set_preference("startup.homepage_welcome_url.additional", "about:blank")
    firefox_profile.set_preference("webdriver_assume_untrusted_issuer", False)
    firefox_profile.set_preference("accept_untrusted_certs", True)
    firefox_profile.update_preferences()
    return firefox_profile


def open_drivers(firefox_profile):
    sleep(10)
    world.driver = get_firefox(firefox_profile)
    world.driver.set_page_load_timeout(20)
    world.driver.implicitly_wait(20)
    world.driver.maximize_window()

def get_firefox(firefox_profile):
    try:
        driver = webdriver.Firefox(firefox_profile=firefox_profile)
    except Exception:
        my_local_firefox_bin = "/usr/bin/firefox"
        firefox_binary = FirefoxBinary(my_local_firefox_bin)
        driver = webdriver.Firefox(firefox_binary=firefox_binary)
    return driver

@after.all
def close_program():
    #print(f"Total {total.scenarios_passed} of {total.scenarios_ran} scenarios passed!")
    close_drivers()
    do_some_zap_stuff()

def close_drivers():
    if world.driver:
        world.driver.quit()

def do_some_zap_stuff():
    target = "http://google-gruyere.appspot.com"
    print("opening target: " + target)
    world.zap.urlopen(target)
    sleep(2.5)
    print("starting spider scan")
    world.zap.spider.scan(target)
    while(int(world.zap.spider.status()) < 100):
        print("spider scan progress %: " + world.zap.spider.status())
        sleep(1)
    #print("starting active scan")
    #world.zap.ascan.scan(target)
    #sleep(2.5)
    #while(int(world.zap.ascan.status()) < 100):
    #    print("active scan progress %: "+ world.zap.ascan.status())
    #    sleep(1)
    #pprint(world.zap.core.alerts())
    report_type = 'xml'
    report_file = 'gruyere.xml'
    with open(report_file, 'a') as f:
        xml = world.zap.core.xmlreport()
        f.write(xml)
        print('Success: {1} report saved to {0}'.format(report_file, report_type.upper()))
    world.zap.core.shutdown()



