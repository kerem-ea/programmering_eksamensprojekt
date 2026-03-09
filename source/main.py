import tkinter as tk
import math, colorsys
from rsa import RSA

class App:
    def __init__(self, root):
        # Initialiserer app med tomt partikel-system og ingen RSA nøgler endnu
        self.root = root
        self.root.title("RSA Nøglegenerator")
        self.root.configure(bg="#0a0a0f")
        self.mouse_data = []
        self.particles  = []
        self.rsa        = None
        self.hue        = 0
        self._build_ui()
        self._animate()

    def _build_ui(self):
        # Bygger hele UI (canvas øverst, knapper i midten, output nederst)
        self.canvas = tk.Canvas(self.root, bg="#050508", highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=12, pady=(12, 4))
        self.canvas.bind("<Motion>", self._record_mouse)

        self.mouse_label = tk.Label(self.root, text="Bevæg musen i boksen...",
                                    bg="#0a0a0f", fg="#555577", font=("Courier", 9))
        self.mouse_label.pack()

        btn_frame = tk.Frame(self.root, bg="#0a0a0f")
        btn_frame.pack(fill=tk.X, padx=12, pady=4)

        style = {"bg": "#1a1a2e", "fg": "#7070ff", "font": ("Courier", 11),
                 "relief": tk.FLAT, "padx": 10, "pady": 4, "cursor": "hand2"}

        tk.Button(btn_frame, text="[ GENERER ]", command=self._generate_keys, **style).pack(side=tk.LEFT, padx=(0, 8))

        self.message_input = tk.Entry(btn_frame, bg="#1a1a2e", fg="#aaaacc",
                                      insertbackground="#7070ff", relief=tk.FLAT, font=("Courier", 11))
        self.message_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        self.message_input.insert(0, "Skriv besked her...")
        self.message_input.bind("<FocusIn>", lambda e: self.message_input.delete(0, tk.END))

        self.encrypt_btn = tk.Button(btn_frame, text="[ KRYPTER ]", command=self._encrypt_decrypt,
                                     state=tk.DISABLED, **style)
        self.encrypt_btn.pack(side=tk.LEFT)

        self.output = tk.Text(self.root, height=12, bg="#0d0d1a", fg="#7070ff", state=tk.DISABLED,
                              font=("Courier", 19), relief=tk.FLAT, insertbackground="#7070ff")
        self.output.pack(fill=tk.BOTH, expand=True, padx=12, pady=(4, 12))

    def _hsv_to_hex(self, h, s, v):
        # Konverterer HSV farve til hex string via Pythons indbyggede colorsys
        r, g, b = colorsys.hsv_to_rgb(h / 360, s, v)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    def _record_mouse(self, event):
        # Gemmer musposition og spawner 6 partikler i en cirkel ved cursoren
        self.mouse_data.append((event.x, event.y, event.time))
        self.hue = (self.hue + 2) % 360
        for i in range(6):
            angle = (i / 6) * math.pi * 2
            self.particles.append({
                "x": float(event.x), "y": float(event.y),
                "vx": math.cos(angle) * (1.5 + (i % 3) * 0.8),
                "vy": math.sin(angle) * (1.5 + (i % 3) * 0.8),
                "life": 1.0, "radius": 8 + i * 2,
                "hue": self.hue + i * 15,
            })
        self.mouse_label.config(text=f"Entropi: {len(self.mouse_data)} punkter optaget")

    def _animate(self):
        self.canvas.delete("particle")
        surviving = []
        for p in self.particles:
            p["x"] += p["vx"]; p["vx"] *= 0.96
            p["y"] += p["vy"]; p["vy"] *= 0.96
            p["life"] -= 0.018
            if p["life"] <= 0:
                continue
            surviving.append(p)
            r = p["radius"] * p["life"]
            self.canvas.create_oval(p["x"]-r, p["y"]-r, p["x"]+r, p["y"]+r,
                fill=self._hsv_to_hex(p["hue"], 0.7 + p["life"] * 0.3, p["life"] * 0.95),
                outline="", tags="particle")
        self.particles = surviving
        self.root.after(16, self._animate)

    def _log(self, label, value):
        # Midlertidigt aktiverer output så vi kan skrive, derefter låses det igen
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, f"{label}\n{value}\n\n")
        self.output.config(state=tk.DISABLED)

    def _generate_keys(self):
        # Genererer RSA nøgler fra musdata og viser seed og n i output
        if len(self.mouse_data) < 10:
            self._log("!", "Bevæg musen mere"); return
        self.output.config(state=tk.NORMAL)
        self.output.delete("1.0", tk.END)
        self.output.config(state=tk.DISABLED)
        self.rsa = RSA(512, self.mouse_data)
        self._log("SEED:", RSA._generate_seed(self.mouse_data))
        self._log("N:",    self.rsa.n)
        self._log("D:",    self.rsa.d)
        self.encrypt_btn.config(state=tk.NORMAL)

    def _encrypt_decrypt(self):
        # Krypterer beskeden fra inputfeltet og dekrypterer den igen som verificering
        besked = self.message_input.get()
        if not besked: return
        krypteret = self.rsa.encrypt(besked)
        self._log("BESKED:",      besked)
        self._log("KRYPTERET:",   krypteret)
        self._log("DEKRYPTERET:", self.rsa.decrypt(krypteret))

root = tk.Tk()
root.geometry("600x700")
root.minsize(400, 500)
App(root)
root.mainloop()