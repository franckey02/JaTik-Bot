try:
    import undetected_chromedriver as uc
    from colorama import Fore, init, Style
    import ctypes, platform, os, time
    import selenium, requests, webbrowser

except ImportError:
    input("You do not have all of the modules required installed.")
    os._exit(1)

text = """
 ███████ ███████ ███████  ██████  ██    ██ 
    ███  ██      ██      ██    ██  ██  ██  
   ███   █████   █████   ██    ██   ████   
  ███    ██      ██      ██    ██    ██    
 ███████ ███████ ██       ██████     ██    """

# Inicializar colorama
init()


class zefoy:

    def __init__(self):
        # Configurar opciones de Chrome para bloquear notificaciones
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.media_stream": 2,
        })

        # Iniciar driver con opciones personalizadas
        self.driver = uc.Chrome(options=chrome_options)
        self.captcha_box = '/html/body/div[5]/div[2]/form/div/div'
        self.clear = "clear"

        if platform.system() == "Windows":
            self.clear = "cls"

        self.color = Fore.BLUE
        self.sent = 0
        self.xpaths = {
            "followers": "/html/body/div[6]/div/div[2]/div/div/div[2]/div/button",
            "hearts": "/html/body/div[6]/div/div[2]/div/div/div[3]/div/button",
            "comment_hearts": "/html/body/div[6]/div/div[2]/div/div/div[4]/div/button",
            "views": "/html/body/div[6]/div/div[2]/div/div/div[5]/div/button",
            "shares": "/html/body/div[6]/div/div[2]/div/div/div[6]/div/button",
            "favorites": "/html/body/div[6]/div/div[2]/div/div/div[7]/div/button",
        }

    def handle_alert(self):
        """Manejar alertas emergentes si aparecen"""
        try:
            alert = self.driver.switch_to.alert
            print(f"{Fore.YELLOW}[ALERT] Detected and dismissed: {alert.text}")
            alert.dismiss()
        except:
            pass

    def main(self):
        os.system(self.clear)
        self.change_title("TikTok Automator using zefoy.com | Github: @xtekky")

        print(self.color + text)
        print("\n" + self._print("Waiting for Zefoy to load... 502 Error = Blocked country or VPN is on"))

        self.driver.get("https://zefoy.com") 

        # Manejar alerta antes de buscar CAPTCHA
        self.handle_alert()

        self.wait_for_xpath(self.captcha_box)

        print(self._print("Site loaded, enter the CAPTCHA to continue."))
        print(self._print("Waiting for you..."))

        self.wait_for_xpath(self.xpaths["followers"])
        os.system(self.clear)
        status = self.check_status()

        print(self.color + text)
        print()
        print(self._print(f"Join our {self.color}Discord Server{Fore.WHITE} for exclusive FREE tools."))
        print(self._print(f"You can also get updates when Zefoy updates the bots and more."))
        print(self._print(f"Select your option below." + "\n"))

        counter = 1
        for thing in status:
            print(self._print(f"{thing} {status[thing]}", counter))
            counter += 1

        print(self._print(f"Discord / Support", "7"))
        option = int(input("\n" + self._print(f"")))

        if option == 1:
            div = "7"
            self.driver.find_element("xpath", self.xpaths["followers"]).click()

        elif option == 2:
            div = "8"
            self.driver.find_element("xpath", self.xpaths["hearts"]).click()

        elif option == 3:
            div = "9"
            self.driver.find_element("xpath", self.xpaths["comment_hearts"]).click()

        elif option == 4:  # Views
            div = "10"
            self.driver.find_element("xpath", self.xpaths["views"]).click()

        elif option == 5:
            div = "11"
            self.driver.find_element("xpath", self.xpaths["shares"]).click()

        elif option == 6:
            div = "12"
            self.driver.find_element("xpath", self.xpaths["favorites"]).click()

        elif option == 7:
            webbrowser.open('discord.gg/onlp')
            os._exit(1)

        else:
            os._exit(1)

        video_url_box = f'/html/body/div[{div}]/div/form/div/input'
        search_box = f'/html/body/div[{div}]/div/form/div/div/button'
        vid_info = input("\n" + self._print(f"Username/VideoURL: "))

        self.send_bot(search_box, main_xpath=video_url_box, vid_info=vid_info, div=div)

    def send_bot(self, search_button, main_xpath, vid_info, div):
        element = self.driver.find_element('xpath', main_xpath)
        element.clear()
        element.send_keys(vid_info)
        self.driver.find_element('xpath', search_button).click()
        time.sleep(3)

        ratelimit_seconds, full = self.check_submit(div)
        if "(s)" in str(full):
            self.main_sleep(ratelimit_seconds)
            self.driver.find_element('xpath', search_button).click()
            time.sleep(2)

        time.sleep(3)

        send_button = f'/html/body/div[{div}]/div/div/div[1]/div/form/button'
        self.driver.find_element('xpath', send_button).click()
        self.sent += 1
        print(self._print(f"Sent {self.sent} times."))

        time.sleep(4)
        self.send_bot(search_button, main_xpath, vid_info, div)

    def main_sleep(self, delay):
        while delay != 0:
            time.sleep(1)
            delay -= 1
            self.change_title(f"TikTok Zefoy Automator using Zefoy.com | Cooldown: {delay}s | Github: @useragents")

    def convert(self, min, sec):
        seconds = 0

        if min != 0:
            answer = int(min) * 60
            seconds += answer

        seconds += int(sec) + 5
        return seconds

    def check_submit(self, div):
        remaining = f"/html/body/div[{div}]/div/div/h4"

        try:
            element = self.driver.find_element("xpath", remaining)
        except:
            return None, None

        if "READY" in element.text:
            return True, True

        if "seconds for your next submit" in element.text:
            output = element.text.split("Please wait ")[1].split(" for")[0]
            minutes = element.text.split("Please wait ")[1].split(" ")[0]
            seconds = element.text.split("(s) ")[1].split(" ")[0]
            sleep_duration = self.convert(minutes, seconds)

            return sleep_duration, output

        return element.text, None

    def check_status(self):
        statuses = {}

        for thing in self.xpaths:
            value = self.xpaths[thing]
            try:
                element = self.driver.find_element('xpath', value)
                if not element.is_enabled():
                    statuses.update({thing: f"{Fore.RED}[OFFLINE]"})
                else:
                    statuses.update({thing: f"{Fore.GREEN}[WORKS]"})
            except:
                statuses.update({thing: f"{Fore.RED}[ERROR]"})

        return statuses

    def _print(self, msg, status="-"):
        return f" {Fore.WHITE}[{self.color}{status}{Fore.WHITE}] {msg}"

    def change_title(self, arg):
        if self.clear == "cls":
            ctypes.windll.kernel32.SetConsoleTitleW(arg)

    def wait_for_xpath(self, xpath):
        while True:
            try:
                self.handle_alert()  # Manejar cualquier alerta antes de buscar el elemento
                f = self.driver.find_element('xpath', xpath)
                return True
            except selenium.common.exceptions.NoSuchElementException:
                time.sleep(1)


if __name__ == "__main__":
    obj = zefoy()
    obj.main()
    input()
