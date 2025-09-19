import tkinter as tk
from tkinter import ttk, messagebox


class PokedexApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokédex - Prototipo")
        self.geometry("800x600")
        self.resizable(False, False)

        self._show_login()

    # ---------------- Pantalla Login ----------------
    def _show_login(self):
        self._clear_frame()

        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Pokédex - Login", font=("Arial", 18)).pack(pady=10)

        ttk.Label(frame, text="Usuario:").pack(anchor="w")
        username = ttk.Entry(frame)
        username.pack(fill="x", pady=5)

        ttk.Label(frame, text="Contraseña:").pack(anchor="w")
        password = ttk.Entry(frame, show="*")
        password.pack(fill="x", pady=5)

        ttk.Button(frame, text="Iniciar sesión", command=self._show_main).pack(pady=10)
        ttk.Button(frame, text="Registrarse", command=lambda: messagebox.showinfo("Registro", "Función aún no implementada")).pack()

    # ---------------- Pantalla Principal ----------------
    def _show_main(self):
        self._clear_frame()

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        # Tabs
        tab_pokemon = ttk.Frame(notebook)
        tab_teams = ttk.Frame(notebook)
        tab_changelog = ttk.Frame(notebook)
        tab_chatbot = ttk.Frame(notebook)

        notebook.add(tab_pokemon, text="Lista Pokémon")
        notebook.add(tab_teams, text="Equipos")
        notebook.add(tab_changelog, text="Changelog")
        notebook.add(tab_chatbot, text="ChatBot")

        # ----- Lista Pokémon -----
        ttk.Label(tab_pokemon, text="Buscar Pokémon:", font=("Arial", 12)).pack(pady=5)
        search_entry = ttk.Entry(tab_pokemon)
        search_entry.pack(pady=5)

        listbox = tk.Listbox(tab_pokemon)
        listbox.pack(expand=True, fill="both", padx=10, pady=10)
        for p in ["Pikachu", "Charmander", "Squirtle", "Bulbasaur"]:
            listbox.insert(tk.END, p)

        ttk.Button(tab_pokemon, text="Ver Detalles", command=lambda: self._show_pokemon_details(listbox)).pack(pady=5)

        # ----- Equipos -----
        ttk.Label(tab_teams, text="Tus Equipos Pokémon", font=("Arial", 12)).pack(pady=5)
        ttk.Button(tab_teams, text="Crear Equipo").pack(pady=10)
        ttk.Button(tab_teams, text="Editar Equipo").pack(pady=5)

        # ----- Changelog -----
        ttk.Label(tab_changelog, text="Últimos eventos de tus amigos:", font=("Arial", 12)).pack(pady=5)
        changelog_list = tk.Listbox(tab_changelog)
        changelog_list.pack(expand=True, fill="both", padx=10, pady=10)
        changelog_list.insert(tk.END, "Ash capturó un Pikachu")
        changelog_list.insert(tk.END, "Misty editó su equipo")

        # ----- ChatBot -----
        ttk.Label(tab_chatbot, text="ChatBot Pokédex", font=("Arial", 12)).pack(pady=5)
        chat_display = tk.Text(tab_chatbot, height=15, state="disabled")
        chat_display.pack(expand=True, fill="both", padx=10, pady=10)

        chat_entry = ttk.Entry(tab_chatbot)
        chat_entry.pack(fill="x", padx=10, pady=5)

        ttk.Button(tab_chatbot, text="Enviar", command=lambda: self._send_chat(chat_display, chat_entry)).pack(pady=5)

    # ---------------- Detalle Pokémon ----------------
    def _show_pokemon_details(self, listbox):
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Atención", "Selecciona un Pokémon primero")
            return

        name = listbox.get(selection[0])
        messagebox.showinfo("Pokémon", f"Detalles de {name} (prototipo)")

    # ---------------- ChatBot ----------------
    def _send_chat(self, display, entry):
        msg = entry.get()
        if not msg.strip():
            return
        entry.delete(0, tk.END)

        display.config(state="normal")
        display.insert(tk.END, f"Tú: {msg}\n")
        display.insert(tk.END, f"Bot: (respuesta simulada a '{msg}')\n\n")
        display.config(state="disabled")
        display.see(tk.END)

    # ---------------- Utils ----------------
    def _clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = PokedexApp()
    app.mainloop()
