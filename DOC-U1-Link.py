import os
# Solución para el error de CustomTkinter al usar --windowed
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")
import customtkinter as ctk
from tkinter import filedialog
import zipfile
import json
import os
import sys
import platform
import locale
import webbrowser
import re
import xml.etree.ElementTree as ET
import posixpath
import subprocess
import sys

# --- GESTIÓN DE RUTAS PARA PYINSTALLER ---
def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, compatible con el ejecutable compilado """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- SOPORTE DRAG & DROP Y GIF ---
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_SUPPORT = True
except ImportError:
    DND_SUPPORT = False

try:
    from PIL import Image, ImageTk
    PIL_SUPPORT = True
except ImportError:
    PIL_SUPPORT = False

# --- CONFIGURACIÓN DE VERSIÓN Y APP ---
APP_NAME = "DOC U1 Link"
APP_VERSION = "v1.0.0"
GITHUB_URL = "https://github.com/Dakros66/DOC-U1-Link"

# --- CONSTANTES DEL MOTOR ---
TARGET_FILAMENTS = 4
DEFAULT_FILAMENT_PROFILE = 'Snapmaker PLA SnapSpeed @U1'
FILAMENT_PROFILES_FILE = 'filament_types.3mf'
GIF_FILENAME = 'esperando.gif'

# --- CONFIGURACIÓN DE ESTILO ---
ctk.set_appearance_mode("Dark")

SNAPMAKER_TEAL = "#00A396"
SNAPMAKER_TEAL_HOVER = "#00857A"
BG_MAIN = "#18181B"      
BG_CARD = "#27272A"      
TEXT_MUTED = "#A1A1AA"   
TEXT_MAIN = "#FAFAFA"    
ACCENT_ORANGE = "#FACC15" 
COLOR_SUCCESS = "#10B981"
COLOR_ERROR = "#EF4444"

# --- DICCIONARIO DE IDIOMAS ---
TRANSLATIONS = {
    "en": {
        "title": "DOC U1 LINK",
        "keep_params": "Parameters to be Exported:",
        "cat_quality": "✨ Quality",
        "cat_strength": "💪 Strength",
        "cat_support": "🚧 Supports",
        "cat_adhesion": "🧲 Adhesion",
        "cat_material": "🔥 Temps",
        "cat_speed": "⚡ Speeds",
        "btn_load": "📂 Drag & Drop or Select .3MF",
        "btn_save_as": "Save As...",
        "btn_save_open": "Auto-Save & Open Orca",
        "status_wait": "Waiting for file...",
        "file_loaded": "📁 {}",
        "info_print": "⏱️ {}  |  ⚖️ {}",
        "filaments_detected": "🎨 AMS Filaments (Ex 1-4):",
        "no_filaments": "No filaments detected. Defaulting to PLA.",
        "msg_success_save": "✅ Saved successfully!",
        "msg_success_open": "✅ Saved! Opening Orca Slicer...",
        "error_template": "❌ Missing base templates in app folder.",
        "not_sliced": "Not Sliced",
        "whitelist_title": "Parameters to be Exported"
    },
    "es": {
        "title": "DOC U1 LINK",
        "keep_params": "Parámetros a Exportar:",
        "cat_quality": "✨ Calidad",
        "cat_strength": "💪 Resistencia",
        "cat_support": "🚧 Soportes",
        "cat_adhesion": "🧲 Adherencia",
        "cat_material": "🔥 Temperaturas",
        "cat_speed": "⚡ Velocidades",
        "btn_load": "📂 Arrastre o Seleccione .3MF",
        "btn_save_as": "Guardar como...",
        "btn_save_open": "Guardar y Abrir Orca",
        "status_wait": "Esperando archivo...",
        "file_loaded": "📁 {}",
        "info_print": "⏱️ {}  |  ⚖️ {}",
        "filaments_detected": "🎨 Filamentos AMS (Ex 1-4):",
        "no_filaments": "Sin filamentos. Usando PLA base.",
        "msg_success_save": "✅ ¡Archivo guardado con éxito!",
        "msg_success_open": "✅ ¡Guardado! Abriendo Orca Slicer...",
        "error_template": "❌ Faltan las plantillas base en la carpeta.",
        "not_sliced": "Sin Laminar",
        "whitelist_title": "Parámetros a Exportar"
    }
}

# --- WHITELIST ---
CONVERTER_PARAMS = {
    "quality": ["layer_height", "initial_layer_height", "seam_position", "ironing_type", "ironing_flow", "ironing_speed", "wall_generator", "elefant_foot_compensation", "precision", "top_surface_pattern", "bottom_surface_pattern", "line_width", "initial_layer_line_width", "outer_wall_line_width", "inner_wall_line_width", "top_surface_line_width", "fuzzy_skin", "fuzzy_skin_mode", "fuzzy_skin_thickness", "fuzzy_skin_point_distance", "seam_slope_type", "seam_gap", "role_base_wipe_speed"],
    "strength": ["wall_loops", "top_shell_layers", "bottom_shell_layers", "sparse_infill_density", "sparse_infill_pattern", "infill_combination", "infill_wall_overlap", "wall_sequence", "bottom_shell_thickness", "top_shell_thickness", "infill_direction", "internal_solid_infill_pattern", "minimum_sparse_infill_area", "top_surface_density", "bottom_surface_density"],
    "support": ["enable_support", "support_type", "support_style", "support_top_z_distance", "support_bottom_z_distance", "support_interface_layers", "support_interface_spacing", "support_expansion", "support_angle", "support_threshold_angle", "tree_support_branch_angle", "tree_support_branch_diameter", "tree_support_branch_distance", "support_base_pattern", "support_interface_pattern", "support_on_build_plate_only", "support_object_xy_distance"],
    "adhesion": ["brim_type", "brim_width", "draft_shield", "brim_object_gap", "skirt_loops", "skirt_distance", "skirt_height", "raft_layers", "raft_contact_distance", "raft_expansion", "raft_first_layer_density"],
    "temperature": ["nozzle_temperature", "nozzle_temperature_initial_layer", "hot_plate_temp", "hot_plate_temp_initial_layer", "temperature_vitrification", "chamber_temperature"],
    "speed": ["outer_wall_speed", "inner_wall_speed", "sparse_infill_speed", "top_surface_speed", "support_speed", "bridge_speed", "initial_layer_speed"]
}

LANG_MAP = {"English": "en", "Español": "es"}
INV_LANG_MAP = {v: k for k, v in LANG_MAP.items()}

if DND_SUPPORT:
    class BaseWindow(ctk.CTk, TkinterDnD.DnDWrapper):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.TkdndVersion = TkinterDnD._require(self)
else:
    class BaseWindow(ctk.CTk):
        pass

class U1SlicerApp(BaseWindow):
    def __init__(self):
        super().__init__()

        self.current_lang = self.detect_system_language()
        self.title(f"{APP_NAME}")
        self.geometry("650x740") 
        self.configure(fg_color=BG_MAIN)
        self.minsize(650, 740)
        self.resizable(False, False)

        self.ruta_3mf_actual = None
        self.detected_filaments = []
        self.available_filaments = self.load_filament_profiles()
        self.timer_mensaje = None
        self.gif_frames = []
        self.gif_index = 0

        self.crear_interfaz()
        
        if PIL_SUPPORT and os.path.exists(resource_path(GIF_FILENAME)):
            self.cargar_gif()

        if DND_SUPPORT:
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self.al_soltar_archivo)

    def T(self, key): return TRANSLATIONS[self.current_lang].get(key, key)

    def detect_system_language(self):
        try:
            loc = locale.getlocale()[0]
            if not loc: loc = os.environ.get('LANG', 'en')
            if loc and loc[:2].lower() in TRANSLATIONS: return loc[:2].lower()
        except: pass
        return 'en' 

    def change_language(self, selected_language_name):
        self.current_lang = LANG_MAP[selected_language_name]
        self.retranslate_ui()

    def retranslate_ui(self):
        self.logo_label.configure(text=self.T("title"))
        self.lbl_keep.configure(text=self.T("keep_params"))
        self.chk_quality.configure(text=self.T("cat_quality"))
        self.chk_strength.configure(text=self.T("cat_strength"))
        self.chk_support.configure(text=self.T("cat_support"))
        self.chk_adhesion.configure(text=self.T("cat_adhesion"))
        self.chk_temp.configure(text=self.T("cat_material"))
        self.chk_speed.configure(text=self.T("cat_speed"))
        self.btn_load_3mf.configure(text=self.T("btn_load"))
        self.btn_save_as.configure(text=self.T("btn_save_as"))
        self.btn_save_open.configure(text=self.T("btn_save_open"))
        
        if not self.ruta_3mf_actual:
            if not self.gif_frames: self.lbl_file_name.configure(text=self.T("status_wait"))
            self.lbl_info.configure(text="")
            self.lbl_filaments_title.configure(text="")

    def abrir_github(self): webbrowser.open(GITHUB_URL)

    def mostrar_whitelist(self):
        modal = ctk.CTkToplevel(self)
        modal.title(self.T("whitelist_title"))
        modal.geometry("400x500")
        modal.configure(fg_color=BG_MAIN)
        modal.attributes('-topmost', True)
        modal.resizable(False, False)

        lbl_title = ctk.CTkLabel(modal, text=self.T("whitelist_title"), font=ctk.CTkFont(size=16, weight="bold"), text_color=SNAPMAKER_TEAL)
        lbl_title.pack(pady=(20, 10))

        scroll = ctk.CTkScrollableFrame(modal, fg_color=BG_CARD)
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        for cat, params in CONVERTER_PARAMS.items():
            cat_label = ctk.CTkLabel(scroll, text=self.T(f"cat_{cat}").upper(), font=ctk.CTkFont(weight="bold", size=13), text_color=SNAPMAKER_TEAL)
            cat_label.pack(anchor="w", pady=(15, 5), padx=10)
            for p in sorted(params):
                ctk.CTkLabel(scroll, text=f"• {p}", font=ctk.CTkFont(size=12), text_color=TEXT_MAIN).pack(anchor="w", padx=20)

    def cargar_gif(self):
        try:
            from PIL import Image
            gif = Image.open(resource_path(GIF_FILENAME))
            w, h = gif.size
            new_h = 120
            new_w = int(new_h * (w/h))
            for i in range(gif.n_frames):
                gif.seek(i)
                f_img = gif.copy().resize((new_w, new_h), Image.Resampling.LANCZOS)
                self.gif_frames.append(ctk.CTkImage(light_image=f_img, dark_image=f_img, size=(new_w, new_h)))
            self.lbl_file_name.configure(text="")
            self.animar_gif()
        except: pass

    def animar_gif(self):
        if not self.ruta_3mf_actual and self.gif_frames:
            self.lbl_file_name.configure(image=self.gif_frames[self.gif_index])
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
            self.after(50, self.animar_gif)

    def al_soltar_archivo(self, event):
        path = event.data
        if path.startswith('{'): path = path[1:-1]
        if path.lower().endswith('.3mf'): self._procesar_y_mostrar_info(path)
        else: self.mostrar_mensaje("❌ Solo archivos .3mf", COLOR_ERROR)

    def load_filament_profiles(self):
        fils = []
        path_profiles = resource_path(FILAMENT_PROFILES_FILE)
        try:
            if os.path.exists(path_profiles):
                with zipfile.ZipFile(path_profiles, 'r') as z:
                    cfg = json.loads(z.read('Metadata/project_settings.config').decode('utf-8'))
                    for t, sid in zip(cfg.get('filament_type', []), cfg.get('filament_settings_id', [])):
                        fils.append({'type': t, 'settings_id': sid})
        except: pass
        return fils if fils else [{'type': 'PLA', 'settings_id': DEFAULT_FILAMENT_PROFILE}]

    def normalize_color(self, color):
        if not color: return '#000000'
        c = color.lstrip('#')[:6]
        return f'#{c.upper()}' if len(c)==6 else '#000000'

    def mostrar_mensaje(self, texto, color):
        self.lbl_inline_status.configure(text=texto, text_color=color)
        if self.timer_mensaje: self.after_cancel(self.timer_mensaje)
        self.timer_mensaje = self.after(5000, lambda: self.lbl_inline_status.configure(text=""))

    def crear_interfaz(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=35, pady=25)

        head = ctk.CTkFrame(main, fg_color="transparent")
        head.pack(fill="x", pady=(0, 20))
        
        self.logo_label = ctk.CTkLabel(head, text=self.T("title"), font=ctk.CTkFont(family="Arial Black", size=28, slant="italic"), text_color=SNAPMAKER_TEAL)
        self.logo_label.pack(side="left")
        
        self.lang_menu = ctk.CTkOptionMenu(head, values=list(LANG_MAP.keys()), command=self.change_language, width=95, fg_color=BG_CARD, button_color=BG_CARD, button_hover_color=SNAPMAKER_TEAL)
        self.lang_menu.set(INV_LANG_MAP[self.current_lang])
        self.lang_menu.pack(side="right")

        self.btn_load_3mf = ctk.CTkButton(main, text=self.T("btn_load"), command=self.cargar_3mf_manual, fg_color="transparent", border_width=2, border_color=SNAPMAKER_TEAL, text_color=TEXT_MAIN, hover_color=BG_CARD, height=80, corner_radius=12, font=ctk.CTkFont(size=18, weight="bold"))
        self.btn_load_3mf.pack(fill="x", pady=(0, 20))

        self.info_panel = ctk.CTkFrame(main, fg_color=BG_CARD, corner_radius=12, height=180)
        self.info_panel.pack(fill="x", pady=0)
        self.info_panel.pack_propagate(False)
        self.lbl_file_name = ctk.CTkLabel(self.info_panel, text=self.T("status_wait"), font=ctk.CTkFont(size=15, weight="bold"), text_color=SNAPMAKER_TEAL, wraplength=500)
        self.lbl_file_name.pack(pady=(15, 5))
        self.lbl_info = ctk.CTkLabel(self.info_panel, text="", font=ctk.CTkFont(size=13))
        self.lbl_info.pack(pady=0)
        self.lbl_filaments_title = ctk.CTkLabel(self.info_panel, text="", font=ctk.CTkFont(size=12), text_color=TEXT_MUTED)
        self.lbl_filaments_title.pack(pady=(10, 5))
        self.filaments_list_frame = ctk.CTkFrame(self.info_panel, fg_color="transparent")
        self.filaments_list_frame.pack(pady=(0, 15))

        opts = ctk.CTkFrame(main, fg_color="transparent")
        opts.pack(fill="x", pady=20)
        title_f = ctk.CTkFrame(opts, fg_color="transparent")
        title_f.pack(fill="x", pady=(0, 10))
        self.lbl_keep = ctk.CTkLabel(title_f, text=self.T("keep_params"), font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT_MUTED)
        self.lbl_keep.pack(side="left")
        self.btn_info = ctk.CTkButton(title_f, text="ℹ️", width=25, height=25, fg_color="transparent", text_color=SNAPMAKER_TEAL, hover_color=BG_CARD, font=ctk.CTkFont(size=16), command=self.mostrar_whitelist)
        self.btn_info.pack(side="right")

        grid = ctk.CTkFrame(opts, fg_color=BG_CARD, corner_radius=10)
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.chk_quality = ctk.CTkCheckBox(grid, text=self.T("cat_quality"), font=ctk.CTkFont(size=13), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER)
        self.chk_quality.grid(row=0, column=0, pady=12, padx=10, sticky="w"); self.chk_quality.select()
        self.chk_strength = ctk.CTkCheckBox(grid, text=self.T("cat_strength"), font=ctk.CTkFont(size=13), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER)
        self.chk_strength.grid(row=0, column=1, pady=12, padx=10, sticky="w"); self.chk_strength.select()
        self.chk_support = ctk.CTkCheckBox(grid, text=self.T("cat_support"), font=ctk.CTkFont(size=13), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER) 
        self.chk_support.grid(row=0, column=2, pady=12, padx=10, sticky="w"); self.chk_support.select()
        self.chk_adhesion = ctk.CTkCheckBox(grid, text=self.T("cat_adhesion"), font=ctk.CTkFont(size=13), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER)
        self.chk_adhesion.grid(row=1, column=0, pady=12, padx=10, sticky="w"); self.chk_adhesion.select()
        self.chk_temp = ctk.CTkCheckBox(grid, text=self.T("cat_material"), font=ctk.CTkFont(size=13), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER)
        self.chk_temp.grid(row=1, column=1, pady=12, padx=10, sticky="w")
        self.chk_speed = ctk.CTkCheckBox(grid, text=self.T("cat_speed"), font=ctk.CTkFont(size=13), fg_color=SNAPMAKER_TEAL, hover_color=SNAPMAKER_TEAL_HOVER)
        self.chk_speed.grid(row=1, column=2, pady=12, padx=10, sticky="w")

        self.lbl_inline_status = ctk.CTkLabel(main, text="", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_inline_status.pack(fill="x", side="bottom", pady=(0, 5))
        acts = ctk.CTkFrame(main, fg_color="transparent")
        acts.pack(fill="x", side="bottom", pady=(0, 15))
        acts.grid_columnconfigure((0, 1), weight=1)
        self.btn_save_as = ctk.CTkButton(acts, text=self.T("btn_save_as"), command=self.accion_guardar_como, fg_color="transparent", border_width=2, border_color=SNAPMAKER_TEAL, text_color=TEXT_MAIN, hover_color=BG_CARD, height=55, font=ctk.CTkFont(size=15, weight="bold"), state="disabled")
        self.btn_save_as.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.btn_save_open = ctk.CTkButton(acts, text=self.T("btn_save_open"), command=self.accion_guardar_y_abrir, fg_color=ACCENT_ORANGE, text_color=BG_MAIN, hover_color="#EAB308", height=55, font=ctk.CTkFont(size=16, weight="bold"), state="disabled")
        self.btn_save_open.grid(row=0, column=1, padx=(8, 0), sticky="ew")

        foot = ctk.CTkFrame(main, fg_color="transparent")
        foot.pack(fill="x", side="bottom", pady=(0, 15))
        ctk.CTkLabel(foot, text=APP_VERSION, font=ctk.CTkFont(size=11), text_color=TEXT_MUTED).pack(side="left")
        ctk.CTkButton(foot, text="GitHub ↗", width=60, height=24, fg_color="transparent", hover_color=BG_CARD, font=ctk.CTkFont(size=11, weight="bold", underline=True), text_color=TEXT_MUTED, command=self.abrir_github).pack(side="right")

    def cargar_3mf_manual(self):
        r = filedialog.askopenfilename(filetypes=[("3MF", "*.3mf")])
        if r: self._procesar_y_mostrar_info(r)

    def _procesar_y_mostrar_info(self, r):
        try:
            self.ruta_3mf_actual = r
            self.lbl_file_name.configure(image="", text=self.T("file_loaded").format(os.path.basename(r)[:45]))
            t_s, w_g, fils = 0, 0, []
            with zipfile.ZipFile(r, 'r') as z:
                if "Metadata/slice_info.config" in z.namelist():
                    c = z.read("Metadata/slice_info.config").decode('utf-8', 'ignore')
                    m_t = re.search(r'key="(?:prediction|estimated_time)" value="([^"]+)"', c)
                    m_w = re.search(r'key="weight" value="([^"]+)"', c)
                    t_s, w_g = float(m_t.group(1)) if m_t else 0, float(m_w.group(1)) if m_w else 0
                    try:
                        root = ET.fromstring(c)
                        for f in root.findall('.//filament'): fils.append({'id':f.get('id'), 'color':self.normalize_color(f.get('color')), 'type':f.get('type','PLA')})
                    except: pass
                if not fils and 'Metadata/project_settings.config' in z.namelist():
                    cfg = json.loads(z.read('Metadata/project_settings.config').decode('utf-8', 'ignore'))
                    for i, (col, typ) in enumerate(zip(cfg.get('filament_colour',[]), cfg.get('filament_type',[]))):
                        fils.append({'id':str(i+1), 'color':self.normalize_color(col), 'type':typ})
            self.lbl_info.configure(text=self.T("info_print").format(f"{int(t_s//3600)}h {int((t_s%3600)//60)}m" if t_s>0 else "--", f"{w_g:.1f}g" if w_g>0 else "--"))
            self.detected_filaments = fils
            for w in self.filaments_list_frame.winfo_children(): w.destroy()
            if fils:
                self.lbl_filaments_title.configure(text=self.T("filaments_detected"))
                for i, f in enumerate(fils[:4]):
                    fr = ctk.CTkFrame(self.filaments_list_frame, fg_color="transparent"); fr.pack(side="left", padx=8)
                    ctk.CTkFrame(fr, fg_color=f['color'], width=18, height=18, corner_radius=9).pack(side="left", padx=(0,5))
                    ctk.CTkLabel(fr, text=f"E{i+1}:{f['type']}", font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
            else: self.lbl_filaments_title.configure(text=self.T("no_filaments"))
            self.btn_save_as.configure(state="normal"); self.btn_save_open.configure(state="normal")
        except Exception as e: self.mostrar_mensaje(f"❌ Error: {e}", COLOR_ERROR)

    def accion_guardar_como(self):
        f = filedialog.asksaveasfilename(defaultextension=".3mf", filetypes=[("3MF", "*.3mf")])
        if f and self._procesar_archivo(self.ruta_3mf_actual, f): self.mostrar_mensaje(self.T("msg_success_save"), COLOR_SUCCESS)

    def accion_guardar_y_abrir(self):
        p = os.path.join(os.path.dirname(self.ruta_3mf_actual), f"{os.path.splitext(os.path.basename(self.ruta_3mf_actual))[0]}_U1.3mf")
        if self._procesar_archivo(self.ruta_3mf_actual, p):
            self.mostrar_mensaje(self.T("msg_success_open"), COLOR_SUCCESS)
            self.after(500, lambda: self.abrir_en_slicer(p))

    def abrir_en_slicer(self, p):
        sys = platform.system()
        try:
            if sys == "Darwin": subprocess.call(["open", "-a", "Snapmaker Orca", p])
            elif sys == "Windows": os.startfile(p)
            else: subprocess.call(["xdg-open", p])
        except: pass

    def _procesar_archivo(self, r_in, r_out):
        keys = set()
        if self.chk_quality.get(): keys.update(CONVERTER_PARAMS["quality"])
        if self.chk_strength.get(): keys.update(CONVERTER_PARAMS["strength"])
        if self.chk_support.get(): keys.update(CONVERTER_PARAMS["support"])
        if self.chk_adhesion.get(): keys.update(CONVERTER_PARAMS["adhesion"])
        if self.chk_temp.get(): keys.update(CONVERTER_PARAMS["temperature"])
        if self.chk_speed.get(): keys.update(CONVERTER_PARAMS["speed"])
        try:
            with zipfile.ZipFile(r_in, 'r') as zin, zipfile.ZipFile(r_out, 'w', zipfile.ZIP_DEFLATED) as zout:
                orig = {}
                for n in zin.namelist():
                    if n.startswith("Config/") or n == 'Metadata/project_settings.config':
                        try: orig.update(json.loads(zin.read(n).decode('utf-8')))
                        except: pass
                
                temp_name = 'u1_template_supports.3mf' if any('enable_support' in str(s) for s in orig.get('different_settings_to_system',[])) else 'u1_template.3mf'
                path_template = resource_path(temp_name)
                
                with zipfile.ZipFile(path_template, 'r') as zt: comb = json.loads(zt.read('Metadata/project_settings.config').decode('utf-8'))
                
                cols, typs = orig.get('filament_colour',[]), orig.get('filament_type',[])
                new_c = [(c+'FF' if len(c)==7 else c).upper() for c in (cols + ['#FFFFFFFF']*4)[:4]]
                new_t = (typs + ['PLA']*4)[:4]
                comb.update({'filament_colour':new_c, 'filament_type':new_t, 'printer_model':'Snapmaker U1'})
                
                p_map = {f['type']: f['settings_id'] for f in self.available_filaments}
                comb['filament_settings_id'] = [p_map.get(t, DEFAULT_FILAMENT_PROFILE) for t in new_t]
                
                inj = []
                for k in keys:
                    if k in orig: comb[k] = orig[k]; inj.append(k)
                
                if inj:
                    diff = comb.get("different_settings_to_system", [""]*5)
                    exist = [x for x in diff[0].split(";") if x]
                    diff[0] = ";".join(sorted(list(set(exist + inj))))
                    comb["different_settings_to_system"] = diff

                for item in zin.infolist():
                    name = posixpath.normpath(item.filename).lstrip('/')
                    if name == 'Metadata/project_settings.config': zout.writestr(item, json.dumps(comb, indent=4))
                    elif name == 'Metadata/slice_info.config':
                        xml = zin.read(item.filename).decode('utf-8','ignore')
                        zout.writestr(item, re.sub(r'key="printer_model_id" value="[^"]*"', 'key="printer_model_id" value="Snapmaker U1"', xml).encode('utf-8'))
                    else: zout.writestr(item, zin.read(item.filename))
            return True
        except Exception as e: self.mostrar_mensaje(f"❌ Error: {e}", COLOR_ERROR); return False

if __name__ == "__main__":
    app = U1SlicerApp()
    app.mainloop()
