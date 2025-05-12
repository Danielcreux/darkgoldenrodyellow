import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import pyperclip
import os

class UltimateProjectAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate AI Project Analyzer")
        self.root.geometry("1400x850")
        self.selected_folder = ""
        self.file_contents = {}
        self.checked_files = {}
        self.current_file_item = ""
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.colors = {
            "primary": "#007BFF",
            "secondary": "#6C757D",
            "success": "#28A745",
            "danger": "#DC3545",
            "light": "#F8F9FA",
            "dark": "#343A40",
            "background": "#E9ECEF"
        }
        
        self.style.configure(".", background=self.colors["background"], foreground=self.colors["dark"])
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TLabel", background=self.colors["background"], foreground=self.colors["dark"], font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        self.style.map("TButton",
                      background=[("active", self.colors["primary"]), ("!active", self.colors["primary"])],
                      foreground=[("active", "white"), ("!active", "white")])
        self.style.configure("Primary.TButton", background=self.colors["primary"])
        self.style.configure("Success.TButton", background=self.colors["success"])
        self.style.configure("Danger.TButton", background=self.colors["danger"])
        self.style.configure("Treeview", background="white", fieldbackground="white")
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Panel izquierdo (Controles)
        left_panel = ttk.Frame(main_frame, width=350)
        left_panel.pack(side="left", fill="y", padx=10, pady=10)
        
        # Sección de objetivo
        goal_frame = ttk.LabelFrame(left_panel, text="🎯 Objetivo del Análisis", padding=15)
        goal_frame.pack(fill="x", pady=5)
        
        self.goal_input = scrolledtext.ScrolledText(
            goal_frame,
            wrap=tk.WORD,
            height=10,
            bg="white",
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        self.goal_input.pack(fill="x")
        
        # Botón para cargar proyecto
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill="x", pady=10)
        ttk.Button(btn_frame, text="Abrir Proyecto", 
                  command=self.load_project, style="Primary.TButton").pack(fill="x")
        
        # Treeview con checkboxes
        tree_frame = ttk.LabelFrame(left_panel, text="📁 Estructura del Proyecto", padding=15)
        tree_frame.pack(fill="both", expand=True, pady=5)
        
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Button-1>", self.toggle_checkbox)
        self.tree.bind("<<TreeviewSelect>>", self.show_content)
        
        # Panel derecho (Contenido y reporte)
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Sección de contenido de archivo
        file_frame = ttk.LabelFrame(right_panel, text="📄 Vista Previa del Contenido", padding=15)
        file_frame.pack(fill="both", expand=True)
        
        # Marco para botones de la vista previa
        file_btn_frame = ttk.Frame(file_frame)
        file_btn_frame.pack(fill='x', pady=5)

        # Botón para seleccionar todos los archivos en la carpeta actual
        ttk.Button(file_btn_frame, text="Seleccionar Archivo", 
         command=self.toggle_current_file_selection, style="Success.TButton").pack(side='left', padx=2)

        self.file_content = scrolledtext.ScrolledText(
            file_frame,
            wrap=tk.WORD,
            bg="white",
            font=("Consolas", 10),
            padx=10,
            pady=10
        )
        self.file_content.pack(fill="both", expand=True)
        
        # Sección de reporte AI
        report_frame = ttk.LabelFrame(right_panel, text="📊 Reporte Generado", padding=15)
        report_frame.pack(fill="both", expand=True, pady=10)
        
        self.report_output = scrolledtext.ScrolledText(
            report_frame,
            wrap=tk.WORD,
            bg="white",
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        self.report_output.pack(fill="both", expand=True)
        
        # Botones de acción
        ttk.Button(btn_frame, text="Generar Reporte", 
          command=self.generate_report, style="Primary.TButton").pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Copiar Reporte", 
                command=self.copy_report, style="Success.TButton").pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Borrar Reporte", 
                command=self.clear_report, style="Danger.TButton").pack(side="left", padx=2)
        
    def load_project(self):
        self.selected_folder = filedialog.askdirectory()
        if self.selected_folder:
            self.populate_tree()
            self.analyze_project()
            messagebox.showinfo("Proyecto Cargado", f"Proyecto: {os.path.basename(self.selected_folder)}")
        
    def populate_tree(self): 
        self.tree.delete(*self.tree.get_children())
        
        def insert_node(parent, path):  # Quitar el parámetro self
            for entry in sorted(os.listdir(path)):
                entry_path = os.path.join(path, entry)
                is_dir = os.path.isdir(entry_path)
                prefix = "☐ " if not is_dir else "📁 "
                node = self.tree.insert(parent, "end", text=f"{prefix}{entry}", open=False)
                if is_dir:
                    insert_node(node, entry_path)  # Llamada recursiva sin self
        
        insert_node("", self.selected_folder)
        
    def analyze_project(self):
        self.file_contents.clear()
        self.checked_files.clear()
        for root, _, files in os.walk(self.selected_folder):
            for file in files:
                file_path = os.path.join(root, file)
                self.checked_files[file_path] = False
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        self.file_contents[file_path] = f.read()
                except Exception as e:
                    self.file_contents[file_path] = f"[Error: {str(e)}]"
        
    def toggle_checkbox(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            item = self.tree.identify_row(event.y)
            current_text = self.tree.item(item, "text")
            file_path = self.get_full_path(item)  # Obtener la ruta completa
            
            # Verificar si es archivo y no directorio
            if os.path.isfile(file_path):
                if current_text.startswith("☐ "):
                    new_text = current_text.replace("☐ ", "☑ ", 1)
                    self.checked_files[file_path] = True
                elif current_text.startswith("☑ "):
                    new_text = current_text.replace("☑ ", "☐ ", 1)
                    self.checked_files[file_path] = False
                else:
                    return  # Solo para manejar casos inesperados
                self.tree.item(item, text=new_text)
                
    def toggle_current_file_selection(self):
        """Alterna la selección del archivo actualmente visible en la vista previa"""
        if hasattr(self, 'current_file_item'):
            item = self.current_file_item
            current_text = self.tree.item(item, "text")
            file_path = self.get_full_path(item)
            
            if os.path.isfile(file_path):
                # Cambiar estado del checkbox
                if current_text.startswith("☐ "):
                    new_text = current_text.replace("☐ ", "☑ ", 1)
                    self.checked_files[file_path] = True
                else:
                    new_text = current_text.replace("☑ ", "☐ ", 1)
                    self.checked_files[file_path] = False
                
                self.tree.item(item, text=new_text)
        else:
            messagebox.showwarning("Advertencia", "Selecciona un archivo primero")
                
    def get_full_path(self, item):
        path = []
        while item:
            path.append(self.tree.item(item, "text").split(" ", 1)[-1])
            item = self.tree.parent(item)
        return os.path.join(self.selected_folder, *reversed(path))
    
    def show_content(self, event):
        selected_item = self.tree.selection()  # ¡Indentación correcta!
        if selected_item:
            item = selected_item[0]
            item_path = self.get_full_path(item)
            self.current_file_item = item  # Guardar la referencia del ítem
            
            content = ""
            if os.path.isdir(item_path):
                try:
                    dir_content = os.listdir(item_path)
                    content = "Contenido del directorio:\n\n" + "\n".join(dir_content)
                except Exception as e:
                    content = f"Error al leer directorio: {str(e)}"
            elif os.path.isfile(item_path):
                content = self.file_contents.get(item_path, "")
            
            self.file_content.delete("1.0", tk.END)
            self.file_content.insert(tk.END, content)


    def update_tree_checkboxes(self):
        """Actualiza visualmente los checkboxes en el Treeview"""
        def check_children(parent):
            for item in self.tree.get_children(parent):
                item_path = self.get_full_path(item)
                if os.path.isfile(item_path):
                    is_checked = self.checked_files.get(item_path, False)
                    prefix = "☑ " if is_checked else "☐ "
                    current_text = self.tree.item(item, "text")
                    new_text = prefix + current_text.split(" ", 1)[-1]
                    self.tree.item(item, text=new_text)
                # Verificar recursivamente subdirectorios
                check_children(item)
        
        check_children("")
        
    def generate_report(self):
        if not self.selected_folder:
            messagebox.showerror("Error", "Primero selecciona un proyecto")
            return
            
        report = "=== REPORTE COMPLETO ===\n\n"
        report += f"Objetivo del análisis:\n{self.goal_input.get('1.0', tk.END)}\n\n"
        report += "Archivos seleccionados:\n"
        
        selected_files = [fp for fp, checked in self.checked_files.items() if checked]
        if not selected_files:
            report += "Ningún archivo seleccionado\n"
        else:
            for file_path in selected_files:
                report += f"\n● {os.path.relpath(file_path, self.selected_folder)}\n"
                report += f"Contenido:\n{self.file_contents.get(file_path, '')}\n"
                report += "-"*100 + "\n"
        
        self.report_output.delete("1.0", tk.END)
        self.report_output.insert(tk.END, report)
        messagebox.showinfo("Reporte Generado", "Reporte creado con éxito")
        
    def copy_report(self):
        report = self.report_output.get("1.0", tk.END)
        pyperclip.copy(report)
        messagebox.showinfo("Copiado", "Reporte copiado al portapapeles")
        
    def clear_report(self):
        self.report_output.delete("1.0", tk.END)
        messagebox.showinfo("Reporte Borrado", "El reporte ha sido eliminado")

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateProjectAnalyzer(root)
    root.mainloop()
