import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os

class CompiladorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compilador - Gestión de Incidencias de Laboratorio")
        self.root.geometry("950x700")

        # Ruta de ejecutable y archivo actual
        self.exe_path = os.path.join(os.getcwd(), "compilador.exe")
        self.archivo_actual = None

        self._configurar_estilos()
        self._crear_interfaz()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))

    def _crear_interfaz(self):
        # --- BARRA SUPERIOR (HERRAMIENTAS) ---
        toolbar = ttk.Frame(self.root, padding=8)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_abrir = ttk.Button(toolbar, text="📂 Abrir Archivo (.lab)", command=self.abrir_archivo)
        btn_abrir.pack(side=tk.LEFT, padx=5)

        btn_guardar = ttk.Button(toolbar, text="💾 Guardar", command=self.guardar_archivo)
        btn_guardar.pack(side=tk.LEFT, padx=5)

        btn_compilar = ttk.Button(toolbar, text="▶ Compilar Código", command=self.compilar)
        btn_compilar.pack(side=tk.LEFT, padx=5)

        self.lbl_archivo = ttk.Label(toolbar, text="Archivo: Sin guardar", font=("Segoe UI", 9, "italic"))
        self.lbl_archivo.pack(side=tk.RIGHT, padx=10)

        # --- PANEL DIVIDIDO ---
        paned = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)

        # --- AREA 1: EDITOR DE CÓDIGO ---
        frame_editor = ttk.LabelFrame(paned, text=" Código Fuente (.lab) ", padding=5)
        paned.add(frame_editor, weight=3)

        self.editor = tk.Text(
            frame_editor, 
            font=("Consolas", 11), 
            undo=True, 
            wrap="none",
            bg="#ffffff", 
            fg="#1e1e1e"
        )
        scroll_y_ed = ttk.Scrollbar(frame_editor, orient=tk.VERTICAL, command=self.editor.yview)
        scroll_x_ed = ttk.Scrollbar(frame_editor, orient=tk.HORIZONTAL, command=self.editor.xview)
        self.editor.configure(yscrollcommand=scroll_y_ed.set, xscrollcommand=scroll_x_ed.set)

        scroll_y_ed.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x_ed.pack(side=tk.BOTTOM, fill=tk.X)
        self.editor.pack(fill=tk.BOTH, expand=True)

        # --- AREA 2: CONSOLA DE RESULTADOS Y ERRORES ---
        frame_consola = ttk.LabelFrame(paned, text=" Reporte de Compilación (Léxico / Sintáctico / Semántico) ", padding=5)
        paned.add(frame_consola, weight=2)

        self.consola = tk.Text(
            frame_consola, 
            font=("Consolas", 10), 
            bg="#1e1e1e", 
            fg="#d4d4d4", 
            wrap="word",
            insertbackground="white"
        )
        scroll_y_con = ttk.Scrollbar(frame_consola, orient=tk.VERTICAL, command=self.consola.yview)
        self.consola.configure(yscrollcommand=scroll_y_con.set)

        scroll_y_con.pack(side=tk.RIGHT, fill=tk.Y)
        self.consola.pack(fill=tk.BOTH, expand=True)

    def abrir_archivo(self):
        # Buscar directamente en carpeta de pruebas si existe
        initial_dir = os.path.join(os.getcwd(), "compilador_lab", "pruebas")
        if not os.path.exists(initial_dir):
            initial_dir = os.getcwd()

        path = filedialog.askopenfilename(
            initialdir=initial_dir,
            filetypes=[("Archivos LAB", "*.lab"), ("Todos los archivos", "*.*")]
        )
        if path:
            self.archivo_actual = path
            self.lbl_archivo.config(text=f"Archivo: {os.path.basename(path)}")
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                contenido = f.read()
                self.editor.delete("1.0", tk.END)
                self.editor.insert(tk.END, contenido)

    def guardar_archivo(self):
        if not self.archivo_actual:
            path = filedialog.asksaveasfilename(
                defaultextension=".lab",
                filetypes=[("Archivos LAB", "*.lab")]
            )
            if path:
                self.archivo_actual = path
                self.lbl_archivo.config(text=f"Archivo: {os.path.basename(path)}")
            else:
                return

        contenido = self.editor.get("1.0", tk.END)
        with open(self.archivo_actual, "w", encoding="utf-8") as f:
            f.write(contenido)

    def compilar(self):
        if not os.path.exists(self.exe_path):
            messagebox.showerror("Error", f"No se encontró 'compilador.exe' en:\n{self.exe_path}")
            return

        # Si el usuario no ha guardado archivo, se genera uno temporal
        if not self.archivo_actual:
            target_file = os.path.join(os.getcwd(), "temp_ejecucion.lab")
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(self.editor.get("1.0", tk.END))
        else:
            self.guardar_archivo()
            target_file = self.archivo_actual

        # Limpiar consola
        self.consola.delete("1.0", tk.END)
        self.consola.insert(tk.END, f"=== EJECUTANDO COMPILADOR ===\nArchivo: {target_file}\n\n")

        try:
            # Invocar al ejecutable C generado
            resultado = subprocess.run(
                [self.exe_path, target_file],
                capture_output=True,
                text=True
            )

            salida = resultado.stdout + resultado.stderr

            if not salida.strip():
                salida = "Compilación completada sin salida."

            self.consola.insert(tk.END, salida)

        except Exception as e:
            self.consola.insert(tk.END, f"Error al ejecutar compilador.exe: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompiladorGUI(root)
    root.mainloop()