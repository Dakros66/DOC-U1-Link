import os
import sys

# --- SOLUCIÓN PARA ERROR DE CUSTOMTKINTER AL USAR --windowed EN WINDOWS ---
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")
    
import io
import threading
import urllib.request
from tkinter.colorchooser import askcolor
import customtkinter as ctk
from tkinter import filedialog
import zipfile
import json
import platform
import locale
import webbrowser
import re
import xml.etree.ElementTree as ET
import posixpath
import subprocess

# --- GESTIÓN DE RUTAS PARA PYINSTALLER ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CONFIGURACIÓN LOCAL (Persistencia) ---
CONFIG_FILE = os.path.expanduser("~/.doc_u1_config.json")

# --- SOPORTE MULTIMEDIA Y DND ---
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
APP_VERSION = "v1.1.0"
GITHUB_URL = "https://github.com/Dakros66/DOC-U1-Link"
GITHUB_API_URL = "https://api.github.com/repos/Dakros66/DOC-U1-Link/releases/latest"

# --- CONSTANTES DEL MOTOR ---
TARGET_FILAMENTS = 4
DEFAULT_FILAMENT_PROFILE = 'Snapmaker PLA SnapSpeed @U1'
FILAMENT_PROFILES_FILE = 'filament_types.3mf'

# --- TRADUCCIÓN DE VARIABLES (Bambu -> Orca) ---
KEY_TRANSLATIONS = {
    "skirt_loops": "skirts"
}

# --- PERFILES DINÁMICOS POR BOQUILLA ---
NOZZLE_PROFILES = {
    "0.2": {"machine": "Snapmaker U1 (0.2 nozzle)", "profile": "0.10 Standard @Snapmaker U1 (0.2 nozzle)"},
    "0.4": {"machine": "Snapmaker U1 (0.4 nozzle)", "profile": "0.20 Standard @Snapmaker U1 (0.4 nozzle)"},
    "0.6": {"machine": "Snapmaker U1 (0.6 nozzle)", "profile": "0.30 Standard @Snapmaker U1 (0.6 nozzle)"},
    "0.8": {"machine": "Snapmaker U1 (0.8 nozzle)", "profile": "0.40 Standard @Snapmaker U1 (0.8 nozzle)"}
}

# --- PALETA DE COLORES PREMIUM ---
ctk.set_appearance_mode("Dark")
BG_ROOT = "#0A0A0C"
BG_SURFACE = "#141417"
BG_CARD_HOVER = "#1E1E22"
BORDER_COLOR = "#2A2A30"
ACCENT_TEAL = "#00D1C1"
ACCENT_ORANGE = "#FACC15"
TEXT_MAIN = "#FFFFFF"
TEXT_DIM = "#8B8B9E"
COLOR_ERROR = "#EF4444"
COLOR_SUCCESS = "#10B981"
BAMBU_GREEN = "#00EA85"

# --- DICCIONARIO DE IDIOMAS ---
TRANSLATIONS = {
    "en": {
        "title": "DOC U1 LINK",
        "settings_title": "Injection Settings",
        "whitelist_title": "Export Parameters",
        "cat_quality": "✨ Quality",
        "cat_strength": "💪 Strength",
        "cat_support": "🚧 Supports",
        "cat_adhesion": "🧲 Adhesion",
        "cat_temperature": "🔥 Temps",
        "cat_speed": "⚡ Speeds",
        "drop_idle": "📥\n\nDrag & Drop .3MF here\nOr click to browse",
        "drop_hover": "✨ Drop file(s) here!",
        "drop_loaded": "🔁 Change File(s)",
        "btn_save_as": "Save As...",
        "btn_save_open": "🚀 Save & Open Orca",
        "btn_save_batch": "🚀 Auto-Convert Batch",
        "batch_params_title": "Detected Parameters Comparator",
        "col_bambu": ".3mf Parameter (Source)",
        "col_snorca": "Snorca U1 Template (Base)",
        "color_picker_title": "Filament Color",
        "info_time": "⏱️ {}",
        "info_weight": "⚖️ {}",
        "info_nozzle": "📏 {}mm",
        "multi_plate": "📑 Contains {} plates",
        "batch_mode": "📦 Batch Mode: {} files selected",
        "filaments_title": "Detected Filaments (Click color to edit):",
        "no_filaments": "No filaments detected. Defaulting to PLA.",
        "msg_success": "✅ Saved successfully!",
        "msg_processing": "⏳ Processing file(s)...",
        "msg_error": "❌ Error: {}",
        "update_avail": "GitHub (Update: {}) ↗",
        "update_latest": "GitHub ({}) ↗",
        "tt_none": "ℹ️ No mapped parameters detected in source.",
        "tt_no_diff": "ℹ️ No differences. (Matches Snorca exactly)",
        "tt_more": "... and {} more variable(s)"
    },
    "es": {
        "title": "DOC U1 LINK",
        "settings_title": "Ajustes de Inyección",
        "whitelist_title": "Parámetros a Exportar",
        "cat_quality": "✨ Calidad",
        "cat_strength": "💪 Resistencia",
        "cat_support": "🚧 Soportes",
        "cat_adhesion": "🧲 Adherencia",
        "cat_temperature": "🔥 Temps",
        "cat_speed": "⚡ Velocidades",
        "drop_idle": "📥\n\nArrastra .3MF aquí\nO haz clic para buscar",
        "drop_hover": "✨ ¡Suelta los archivos aquí!",
        "drop_loaded": "🔁 Cambiar Archivo(s)",
        "btn_save_as": "Guardar como...",
        "btn_save_open": "🚀 Guardar y Abrir Orca",
        "btn_save_batch": "🚀 Autoconvertir Lote",
        "batch_params_title": "Comparador de Diferencias (Modo Delta)",
        "col_bambu": "Parámetro .3mf (Origen)",
        "col_snorca": "Plantilla Snorca U1 (Base)",
        "color_picker_title": "Color del Filamento",
        "info_time": "⏱️ {}",
        "info_weight": "⚖️ {}",
        "info_nozzle": "📏 {}mm",
        "multi_plate": "📑 Contiene {} placas",
        "batch_mode": "📦 Modo Lote: {} archivos",
        "filaments_title": "Filamentos Mapeados (Clic color para editar):",
        "no_filaments": "Sin filamentos. Usando PLA base.",
        "msg_success": "✅ ¡Guardado con éxito!",
        "msg_processing": "⏳ Procesando archivo(s)...",
        "msg_error": "❌ Error: {}",
        "update_avail": "GitHub (Actualizar a {}) ↗",
        "update_latest": "GitHub ({}) ↗",
        "tt_none": "ℹ️ Ningún parámetro listado detectado en el origen.",
        "tt_no_diff": "ℹ️ Sin diferencias. (Coincide con Snorca)",
        "tt_more": "... y {} variable(s) más"
    }
}

LANG_MAP = {"English": "en", "Español": "es"}
INV_LANG_MAP = {v: k for k, v in LANG_MAP.items()}

CONVERTER_PARAMS = {
    "quality": ["layer_height", "initial_layer_height", "seam_position", "ironing_type", "ironing_flow", "ironing_speed", "wall_generator", "elefant_foot_compensation", "precision", "top_surface_pattern", "bottom_surface_pattern", "line_width", "initial_layer_line_width", "outer_wall_line_width", "inner_wall_line_width", "top_surface_line_width", "fuzzy_skin", "fuzzy_skin_mode", "fuzzy_skin_thickness", "fuzzy_skin_point_distance", "seam_slope_type", "seam_gap", "role_base_wipe_speed"],
    "strength": ["wall_loops", "top_shell_layers", "bottom_shell_layers", "sparse_infill_density", "sparse_infill_pattern", "infill_combination", "infill_wall_overlap", "wall_sequence", "bottom_shell_thickness", "top_shell_thickness", "infill_direction", "internal_solid_infill_pattern", "minimum_sparse_infill_area", "top_surface_density", "bottom_surface_density"],
    "support": ["enable_support", "support_type", "support_style", "support_top_z_distance", "support_bottom_z_distance", "support_interface_layers", "support_interface_spacing", "support_expansion", "support_angle", "support_threshold_angle", "tree_support_branch_angle", "tree_support_branch_diameter", "tree_support_branch_distance", "support_base_pattern", "support_interface_pattern", "support_on_build_plate_only", "support_object_xy_distance"],
    "adhesion": ["brim_type", "brim_width", "draft_shield", "brim_object_gap", "skirt_loops", "skirt_distance", "skirt_height", "raft_layers", "raft_contact_distance", "raft_expansion", "raft_first_layer_density"],
    "temperature": ["nozzle_temperature", "nozzle_temperature_initial_layer", "hot_plate_temp", "hot_plate_temp_initial_layer", "temperature_vitrification", "chamber_temperature"],
    "speed": ["outer_wall_speed", "inner_wall_speed", "sparse_infill_speed", "top_surface_speed", "support_speed", "bridge_speed", "initial_layer_speed"]
}

if DND_SUPPORT:
    class BaseWindow(ctk.CTk, TkinterDnD.DnDWrapper):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            try:
                self.TkdndVersion = TkinterDnD._require(self)
                self._dnd_active = True
            except RuntimeError:
                self._dnd_active = False
else:
    class BaseWindow(ctk.CTk):
        _dnd_active = False

class U1SlicerApp(BaseWindow):
    def __init__(self):
        super().__init__()

        self.rutas_3mf_actuales = []
        self.batch_data = [] 
        self.available_filaments = self.load_filament_profiles()
        self.tipos_disponibles = ["PLA", "PETG", "ABS", "TPU"]
        
        self.template_defaults = {}
        self.load_template_defaults()
        
        self.states = {
            "quality": True, "strength": True, "support": True,
            "adhesion": True, "temperature": False, "speed": False
        }
        self.current_lang = "en"
        self.cargar_configuracion()
        
        self.title(f"{APP_NAME} {APP_VERSION}")
        self.geometry("1050x780")
        self.configure(fg_color=BG_ROOT)
        self.minsize(950, 750)
        
        self.tile_buttons = {}
        self._tooltip_timer = None
        self._active_tooltip_key = None 

        self.setup_layout()
        self.chequear_actualizaciones()

        if getattr(self, '_dnd_active', False):
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self.al_soltar_archivo)
            self.dnd_bind('<<DropEnter>>', self.al_entrar_drag)
            self.dnd_bind('<<DropLeave>>', self.al_salir_drag)

    # --- MOTOR DE SCROLL RECURSIVO ---
    def _aplicar_scroll_seguro(self, widget, ctk_scrollable_frame):
        def _on_mousewheel(event):
            canvas = ctk_scrollable_frame._parent_canvas
            if canvas.yview() == (0.0, 1.0): return
            if platform.system() == 'Windows':
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif platform.system() == 'Darwin':
                canvas.yview_scroll(int(-1*event.delta), "units")
                
        def _on_linux_scroll_up(event):
            canvas = ctk_scrollable_frame._parent_canvas
            if canvas.yview() != (0.0, 1.0): canvas.yview_scroll(-1, "units")
            
        def _on_linux_scroll_down(event):
            canvas = ctk_scrollable_frame._parent_canvas
            if canvas.yview() != (0.0, 1.0): canvas.yview_scroll(1, "units")

        try:
            widget.bind("<MouseWheel>", _on_mousewheel, add="+")
            widget.bind("<Button-4>", _on_linux_scroll_up, add="+")
            widget.bind("<Button-5>", _on_linux_scroll_down, add="+")
        except: pass

        for child in widget.winfo_children():
            self._aplicar_scroll_seguro(child, ctk_scrollable_frame)

    def T(self, key): return TRANSLATIONS.get(self.current_lang, TRANSLATIONS["en"]).get(key, key)

    def guardar_configuracion(self):
        try:
            config = {"lang": self.current_lang, "states": self.states}
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f)
        except: pass

    def cargar_configuracion(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    self.current_lang = config.get("lang", "en")
                    if "states" in config:
                        self.states.update(config["states"])
            else:
                self.current_lang = self.detect_system_language()
        except:
            self.current_lang = self.detect_system_language()

    def detect_system_language(self):
        try:
            loc = locale.getlocale()[0]
            if not loc: loc = os.environ.get('LANG', 'en')
            if loc and loc[:2].lower() in TRANSLATIONS: return loc[:2].lower()
        except: pass
        return 'en'

    def chequear_actualizaciones(self):
        def fetch():
            try:
                req = urllib.request.Request(GITHUB_API_URL, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=3) as response:
                    data = json.loads(response.read().decode())
                    latest = data.get('tag_name', '')
                    if latest:
                        self.after(0, self.mostrar_version_github, latest)
            except: pass
        threading.Thread(target=fetch, daemon=True).start()

    def mostrar_version_github(self, latest_version):
        if latest_version != APP_VERSION:
            self.btn_git.configure(text=self.T("update_avail").format(latest_version), text_color=ACCENT_ORANGE)
        else:
            self.btn_git.configure(text=self.T("update_latest").format(latest_version), text_color=TEXT_DIM)

    def load_filament_profiles(self):
        path = resource_path(FILAMENT_PROFILES_FILE)
        try:
            if os.path.exists(path):
                with zipfile.ZipFile(path, 'r') as z:
                    cfg = json.loads(z.read('Metadata/project_settings.config').decode('utf-8'))
                    return [{'type': t, 'settings_id': sid} for t, sid in zip(cfg.get('filament_type', []), cfg.get('filament_settings_id', []))]
        except: pass
        return [{'type': 'PLA', 'settings_id': DEFAULT_FILAMENT_PROFILE}]

    def load_template_defaults(self):
        path = resource_path('u1_template.3mf')
        if os.path.exists(path):
            try:
                with zipfile.ZipFile(path, 'r') as z:
                    if 'Metadata/project_settings.config' in z.namelist():
                        cfg = json.loads(z.read('Metadata/project_settings.config').decode('utf-8', 'ignore'))
                        self.template_defaults = cfg
            except: pass

    def format_val(self, val):
        if isinstance(val, list):
            if len(val) > 0 and all(x == val[0] for x in val):
                return str(val[0])
            return f"[{', '.join(str(x) for x in val)}]"
        return str(val)

    def normalize_color(self, color):
        if not color: return '#000000'
        c = color.lstrip('#')[:6]
        return f'#{c.upper()}' if len(c)==6 else '#000000'

    def abrir_github(self, event=None): webbrowser.open(GITHUB_URL)

    def mostrar_whitelist(self):
        modal = ctk.CTkToplevel(self)
        modal.title(self.T("whitelist_title"))
        modal.geometry("450x600")
        modal.configure(fg_color=BG_ROOT)
        modal.attributes('-topmost', True)
        
        lbl_title = ctk.CTkLabel(modal, text=self.T("whitelist_title"), font=ctk.CTkFont(size=18, weight="bold"), text_color=ACCENT_TEAL)
        lbl_title.pack(pady=(20, 10))

        scroll = ctk.CTkScrollableFrame(modal, fg_color=BG_SURFACE, corner_radius=15, border_width=1, border_color=BORDER_COLOR)
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        for cat, params in CONVERTER_PARAMS.items():
            cat_label = ctk.CTkLabel(scroll, text=self.T(f"cat_{cat}").upper(), font=ctk.CTkFont(weight="bold", size=14), text_color=ACCENT_ORANGE)
            cat_label.pack(anchor="w", pady=(15, 5), padx=10)
            for p in sorted(params):
                ctk.CTkLabel(scroll, text=f"• {p}", font=ctk.CTkFont(size=12), text_color=TEXT_MAIN).pack(anchor="w", padx=20)
                
        self._aplicar_scroll_seguro(scroll, scroll)

    def cambiar_color_filamento(self, fil_dict, btn_widget):
        nuevo_color = askcolor(color=fil_dict['color'], title=self.T("color_picker_title"))[1]
        if nuevo_color:
            fil_dict['color'] = nuevo_color.upper()
            btn_widget.configure(fg_color=nuevo_color, hover_color=nuevo_color)

    # --- LÓGICA DEL TOOLTIP MATEMÁTICO ANTI-CORTES ---
    def schedule_tooltip(self, btn, key):
        self.cancel_hide_tooltip()
        if self._active_tooltip_key == key: return
        self._tooltip_timer = self.after(200, lambda: self.show_tooltip(btn, key))

    def show_tooltip(self, btn, key):
        if not self.batch_data or len(self.batch_data) > 1: return

        self._active_tooltip_key = key
        self.tooltip_frame.place_forget() 
        
        for w in self.tooltip_content.winfo_children(): w.destroy()

        cat_title = self.T(f"cat_{key}").upper()
        ctk.CTkLabel(self.tooltip_content, text=cat_title, font=ctk.CTkFont(size=14, weight="bold"), text_color=ACCENT_TEAL).pack(anchor="w", pady=(5, 10), padx=5)

        params = self.batch_data[0].get('detected_params', {}).get(key, {})
        diff_params = []
        
        for p_k, p_v in params.items():
            target_k = KEY_TRANSLATIONS.get(p_k, p_k)
            orca_val_raw = self.template_defaults.get(target_k, None)
            orca_val = self.format_val(orca_val_raw) if orca_val_raw is not None else "--"
            if str(p_v) != str(orca_val):
                diff_params.append((p_k, p_v, target_k, orca_val))
        
        max_items = 6 
        
        if not params:
            ctk.CTkLabel(self.tooltip_content, text=self.T("tt_none"), font=ctk.CTkFont(size=11, slant="italic"), text_color=TEXT_DIM).pack(anchor="w", padx=15)
        elif not diff_params:
            ctk.CTkLabel(self.tooltip_content, text=self.T("tt_no_diff"), font=ctk.CTkFont(size=11, slant="italic"), text_color=TEXT_DIM).pack(anchor="w", padx=15)
        else:
            header_f = ctk.CTkFrame(self.tooltip_content, fg_color="transparent")
            header_f.pack(fill="x", padx=5, pady=(0, 5))
            header_f.grid_columnconfigure((0, 1), weight=1)
            ctk.CTkLabel(header_f, text=self.T("col_bambu"), text_color=BAMBU_GREEN, font=ctk.CTkFont(weight="bold", size=12)).grid(row=0, column=0, sticky="w")
            ctk.CTkLabel(header_f, text=self.T("col_snorca"), text_color=TEXT_MAIN, font=ctk.CTkFont(weight="bold", size=12)).grid(row=0, column=1, sticky="w")

            for p_k, p_v, target_k, orca_val in diff_params[:max_items]:
                row_f = ctk.CTkFrame(self.tooltip_content, fg_color="transparent")
                row_f.pack(fill="x", padx=5, pady=2)
                row_f.grid_columnconfigure((0, 1), weight=1)
                
                ctk.CTkLabel(row_f, text=f"{p_k} = {p_v}", text_color=BAMBU_GREEN, font=ctk.CTkFont(size=11)).grid(row=0, column=0, sticky="w", padx=(0, 10))
                ctk.CTkLabel(row_f, text=f"{target_k} = {orca_val}", text_color=TEXT_MAIN, font=ctk.CTkFont(size=11)).grid(row=0, column=1, sticky="w")
            
            if len(diff_params) > max_items:
                ctk.CTkLabel(self.tooltip_content, text=self.T("tt_more").format(len(diff_params) - max_items), font=ctk.CTkFont(size=10, slant="italic"), text_color=TEXT_DIM).pack(anchor="w", padx=10, pady=(5, 0))

        # Pedirle a tkinter que renderice la caja en background para saber qué tamaño ha ocupado TODO el texto
        self.tooltip_frame.update_idletasks()

        # Medidas Reales Renderizadas Orgánicamente
        tw = self.tooltip_frame.winfo_reqwidth()
        th = self.tooltip_frame.winfo_reqheight()

        app_w = self.winfo_width()
        app_h = self.winfo_height()

        # Coordenadas Absolutas del Botón
        b_x = btn.winfo_rootx() - self.winfo_rootx()
        b_y = btn.winfo_rooty() - self.winfo_rooty()
        b_w = btn.winfo_width()
        b_h = btn.winfo_height()

        # Intento Normal: Centrado Arriba
        x = b_x + (b_w // 2) - (tw // 2)
        y = b_y - th - 10

        # Anti-Colisión Horizontal
        if x < 10: 
            x = 10
        elif x + tw > app_w - 10: 
            x = app_w - tw - 10

        # Anti-Colisión Vertical
        if y < 10: 
            y = b_y + b_h + 10 # Se saldría por arriba, lo empujamos abajo
            if y + th > app_h - 10: 
                y = app_h - th - 10 # Es enorme y se sale por abajo también, lo anclamos al fondo
                
        self.tooltip_frame.place(x=x, y=y)
        self.tooltip_frame.lift()

    def cancel_hide_tooltip(self, event=None):
        if self._tooltip_timer:
            self.after_cancel(self._tooltip_timer)
            self._tooltip_timer = None

    def hide_tooltip(self, event=None):
        self.cancel_hide_tooltip()
        self._tooltip_timer = self.after(100, self._do_hide_tooltip)

    def _do_hide_tooltip(self):
        self._active_tooltip_key = None
        self.tooltip_frame.place_forget()

    # --- INSPECTOR DE PARÁMETROS EN LOTE/SINGLE ---
    def abrir_modal_params_lote(self):
        if not self.batch_data: return
        
        modal = ctk.CTkToplevel(self)
        modal.title(self.T("batch_params_title"))
        modal.geometry("900x650")
        modal.configure(fg_color=BG_ROOT)
        modal.focus()

        lbl_title = ctk.CTkLabel(modal, text=self.T("batch_params_title"), font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_MAIN)
        lbl_title.pack(pady=(20, 10))

        scroll = ctk.CTkScrollableFrame(modal, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        for f_data in self.batch_data:
            card = ctk.CTkFrame(scroll, fg_color=BG_SURFACE, corner_radius=10, border_color=BORDER_COLOR, border_width=1)
            card.pack(fill="x", pady=10)
            
            ctk.CTkLabel(card, text=f"📄 {f_data['filename']}", font=ctk.CTkFont(size=14, weight="bold"), text_color=ACCENT_TEAL).pack(anchor="w", padx=15, pady=(10, 5))
            
            has_any_param = False
            has_differences = False
            
            for cat, keys_list in CONVERTER_PARAMS.items():
                params = f_data.get('detected_params', {}).get(cat, {})
                diff_params = []
                
                if params:
                    has_any_param = True
                    for p_k, p_v in params.items():
                        target_k = KEY_TRANSLATIONS.get(p_k, p_k)
                        orca_val_raw = self.template_defaults.get(target_k, None)
                        orca_val = self.format_val(orca_val_raw) if orca_val_raw is not None else "--"
                        if str(p_v) != str(orca_val):
                            diff_params.append((p_k, p_v, target_k, orca_val))

                if diff_params:
                    has_differences = True
                    cat_label = ctk.CTkLabel(card, text=self.T(f"cat_{cat}").upper(), font=ctk.CTkFont(size=12, weight="bold"), text_color=ACCENT_ORANGE)
                    cat_label.pack(anchor="w", padx=25, pady=(10, 0))
                    
                    table_f = ctk.CTkFrame(card, fg_color="transparent")
                    table_f.pack(fill="x", padx=35, pady=5)
                    table_f.grid_columnconfigure((0, 1), weight=1)
                    
                    ctk.CTkLabel(table_f, text=self.T("col_bambu"), text_color=BAMBU_GREEN, font=ctk.CTkFont(weight="bold", size=11)).grid(row=0, column=0, sticky="w")
                    ctk.CTkLabel(table_f, text=self.T("col_snorca"), text_color=TEXT_MAIN, font=ctk.CTkFont(weight="bold", size=11)).grid(row=0, column=1, sticky="w")
                    
                    row_idx = 1
                    for p_k, p_v, target_k, orca_val in diff_params:
                        ctk.CTkLabel(table_f, text=f"{p_k} = {p_v}", text_color=BAMBU_GREEN, font=ctk.CTkFont(size=11)).grid(row=row_idx, column=0, sticky="w", pady=1)
                        ctk.CTkLabel(table_f, text=f"{target_k} = {orca_val}", text_color=TEXT_MAIN, font=ctk.CTkFont(size=11)).grid(row=row_idx, column=1, sticky="w", pady=1)
                        row_idx += 1
                        
            if not has_any_param:
                ctk.CTkLabel(card, text=self.T("tt_none"), font=ctk.CTkFont(size=11, slant="italic"), text_color=TEXT_DIM).pack(anchor="w", padx=25, pady=(5, 15))
            elif not has_differences:
                ctk.CTkLabel(card, text=self.T("tt_no_diff"), font=ctk.CTkFont(size=11, slant="italic"), text_color=TEXT_DIM).pack(anchor="w", padx=25, pady=(5, 15))

        self._aplicar_scroll_seguro(scroll, scroll)

    def setup_layout(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=45, uniform="cols")
        self.grid_columnconfigure(1, weight=55, uniform="cols")

        # --- FRAME DEL TOOLTIP DINÁMICO (Sin tamaños fijos) ---
        self.tooltip_frame = ctk.CTkFrame(self, fg_color=BG_SURFACE, border_width=2, border_color=ACCENT_TEAL, corner_radius=15)
        self.tooltip_content = ctk.CTkFrame(self.tooltip_frame, fg_color="transparent")
        self.tooltip_content.pack(fill="both", expand=True, padx=10, pady=10)

        self.tooltip_frame.bind("<Enter>", self.cancel_hide_tooltip)
        self.tooltip_frame.bind("<Leave>", self.hide_tooltip)
        self.tooltip_content.bind("<Enter>", self.cancel_hide_tooltip)
        self.tooltip_content.bind("<Leave>", self.hide_tooltip)

        # --- COLUMNA IZQUIERDA ---
        self.left_p = ctk.CTkFrame(self, fg_color="transparent")
        self.left_p.grid(row=1, column=0, sticky="nsew", padx=(30, 15), pady=(20, 10))
        
        header_izq = ctk.CTkFrame(self.left_p, fg_color="transparent")
        header_izq.pack(side="top", fill="x", pady=(0, 20))
        ctk.CTkLabel(header_izq, text="DOC U1 LINK", font=ctk.CTkFont(family="Arial Black", size=24, slant="italic"), text_color=ACCENT_TEAL).pack(side="left")
        ctk.CTkLabel(header_izq, text=APP_VERSION, font=ctk.CTkFont(size=10, weight="bold"), text_color=BG_ROOT, fg_color=ACCENT_TEAL, corner_radius=8, padx=6).pack(side="left", padx=10)

        self.left_act_f = ctk.CTkFrame(self.left_p, fg_color="transparent")
        self.left_act_f.pack(side="bottom", fill="x")
        
        self.btn_change = ctk.CTkButton(self.left_act_f, text=self.T("drop_loaded"), height=60, corner_radius=15,
                                        fg_color=BG_SURFACE, hover_color=BG_CARD_HOVER, border_width=2, border_color=BORDER_COLOR,
                                        font=ctk.CTkFont(size=15, weight="bold"), text_color=TEXT_DIM,
                                        command=self.cargar_3mf_manual)

        self.dropzone = ctk.CTkButton(self.left_p, text=self.T("drop_idle"), 
                                      corner_radius=20, fg_color=BG_SURFACE, hover_color=BG_CARD_HOVER, 
                                      border_width=2, border_color=BORDER_COLOR, font=ctk.CTkFont(size=14, weight="bold"), 
                                      text_color=TEXT_DIM, command=self.cargar_3mf_manual)
        self.dropzone.pack(side="top", fill="both", expand=True)

        self.info_card = ctk.CTkFrame(self.left_p, fg_color=BG_SURFACE, corner_radius=20, border_width=1, border_color=BORDER_COLOR)
        self.lbl_file = ctk.CTkLabel(self.info_card, text="", font=ctk.CTkFont(size=15, weight="bold"), text_color=ACCENT_TEAL, wraplength=300)
        
        # Color sólido para habilitar Scroll
        self.batch_scroll = ctk.CTkScrollableFrame(self.info_card, fg_color=BG_SURFACE, scrollbar_button_color=BORDER_COLOR, scrollbar_button_hover_color=TEXT_DIM)

        # --- COLUMNA DERECHA ---
        self.right_p = ctk.CTkFrame(self, fg_color="transparent")
        self.right_p.grid(row=1, column=1, sticky="nsew", padx=(15, 30), pady=(20, 10))

        top_bar = ctk.CTkFrame(self.right_p, fg_color="transparent")
        top_bar.pack(side="top", fill="x", pady=(0, 20))
        
        self.lbl_settings = ctk.CTkLabel(top_bar, text=self.T("settings_title"), font=ctk.CTkFont(size=18, weight="bold"), text_color=TEXT_MAIN)
        self.lbl_settings.pack(side="left")
        
        self.btn_info = ctk.CTkButton(top_bar, text="ℹ️", width=30, height=30, fg_color="transparent", hover_color=BG_CARD_HOVER, font=ctk.CTkFont(size=16), command=self.mostrar_whitelist)
        self.btn_info.pack(side="left", padx=(10, 0))
        
        self.btn_inspector = ctk.CTkButton(top_bar, text="🔍", width=30, height=30, fg_color="transparent", hover_color=BG_CARD_HOVER, font=ctk.CTkFont(size=16), command=self.abrir_modal_params_lote, state="disabled")
        self.btn_inspector.pack(side="left", padx=(5, 0))

        self.lang_menu = ctk.CTkOptionMenu(top_bar, values=list(LANG_MAP.keys()), command=self.change_language, 
                                           width=100, fg_color=BG_SURFACE, button_color=BG_SURFACE, button_hover_color=BG_CARD_HOVER, font=ctk.CTkFont(weight="bold"))
        self.lang_menu.set(INV_LANG_MAP[self.current_lang])
        self.lang_menu.pack(side="right")

        self.right_act_f = ctk.CTkFrame(self.right_p, fg_color="transparent")
        self.right_act_f.pack(side="bottom", fill="x")
        
        self.btn_save = ctk.CTkButton(self.right_act_f, text=self.T("btn_save_as"), height=60, corner_radius=15,
                                      fg_color="transparent", border_width=2, border_color=ACCENT_TEAL,
                                      text_color=TEXT_MAIN, font=ctk.CTkFont(size=15, weight="bold"),
                                      state="disabled", command=self.accion_guardar_como)
        self.btn_save.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_open = ctk.CTkButton(self.right_act_f, text=self.T("btn_save_open"), height=60, corner_radius=15,
                                      fg_color=ACCENT_ORANGE, hover_color="#E09900", text_color=BG_ROOT, 
                                      font=ctk.CTkFont(size=16, weight="bold"),
                                      state="disabled", command=self.accion_guardar_y_abrir)
        self.btn_open.pack(side="right", fill="x", expand=True)

        self.progressbar = ctk.CTkProgressBar(self.right_p, mode="indeterminate", fg_color=BG_SURFACE, progress_color=ACCENT_TEAL, height=4)
        
        self.grid_f = ctk.CTkFrame(self.right_p, fg_color="transparent")
        self.grid_f.pack(side="top", fill="both", expand=True, pady=(0, 20))
        self.grid_f.grid_columnconfigure((0, 1), weight=1, uniform="tiles")
        self.grid_f.grid_rowconfigure((0, 1, 2), weight=1, uniform="tiles")

        self.tiles_keys = ["quality", "strength", "support", "adhesion", "temperature", "speed"]

        for i, key in enumerate(self.tiles_keys):
            btn = ctk.CTkButton(self.grid_f, text=self.T(f"cat_{key}"), corner_radius=15, 
                                font=ctk.CTkFont(size=15, weight="bold"),
                                command=lambda k=key: self.toggle_tile(k))
            btn.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="nsew")
            
            btn.bind("<Enter>", lambda e, b=btn, k=key: self.schedule_tooltip(b, k))
            btn.bind("<Leave>", self.hide_tooltip)
            
            self.tile_buttons[key] = btn
            self.update_tile_appearance(key)

        # --- FOOTER ---
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, columnspan=2, sticky="ew", padx=30, pady=(0, 15))
        
        self.btn_git = ctk.CTkButton(footer, text="GitHub ↗", height=20, width=60, font=ctk.CTkFont(size=12, weight="bold", underline=True),
                                     fg_color="transparent", text_color=TEXT_DIM, hover_color=BG_ROOT, command=self.abrir_github)
        self.btn_git.pack(side="right")

    def set_ui_loading(self, is_loading):
        estado = "disabled" if is_loading else "normal"
        self.btn_save.configure(state=estado)
        self.btn_open.configure(state=estado)
        self.btn_change.configure(state=estado)
        self.btn_info.configure(state=estado)
        self.btn_inspector.configure(state=estado)
        
        for btn in self.tile_buttons.values():
            btn.configure(state=estado)
            
        for f_data in self.batch_data:
            for combo in f_data.get('combos_ui', []):
                combo.configure(state=estado)
            for c_btn in f_data.get('color_btns_ui', []):
                c_btn.configure(state=estado)
            
        if is_loading:
            self.batch_scroll.pack_forget()
            self.info_card.pack_forget()
            self.dropzone.configure(text=self.T("msg_processing"), text_color=ACCENT_ORANGE)
            self.dropzone.pack(side="top", fill="both", expand=True)
            self.progressbar.pack(side="bottom", fill="x", pady=(0, 15))
            self.progressbar.start()
        else:
            self.progressbar.stop()
            self.progressbar.pack_forget()
            self.dropzone.pack_forget()
            self.info_card.pack(side="top", fill="both", expand=True, pady=(0, 20))
            self.batch_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def change_language(self, selected_language_name):
        self.current_lang = LANG_MAP[selected_language_name]
        self.guardar_configuracion()
        self.lbl_settings.configure(text=self.T("settings_title"))
        self.btn_save.configure(text=self.T("btn_save_as"))
        self.btn_open.configure(text=self.T("btn_save_open"))
        
        if self.rutas_3mf_actuales:
            self.btn_change.configure(text=self.T("drop_loaded"))
            if len(self.rutas_3mf_actuales) > 1:
                self.btn_save.configure(text=self.T("btn_save_batch"))
                self.lbl_file.configure(text=self.T("batch_mode").format(len(self.rutas_3mf_actuales)))
        else:
            self.dropzone.configure(text=self.T("drop_idle"))
            
        for key in self.tiles_keys:
            self.tile_buttons[key].configure(text=self.T(f"cat_{key}"))

    def toggle_tile(self, key):
        self.states[key] = not self.states[key]
        self.update_tile_appearance(key)
        self.guardar_configuracion()

    def update_tile_appearance(self, key):
        active = self.states[key]
        btn = self.tile_buttons[key]
        if active:
            btn.configure(fg_color=ACCENT_TEAL, hover_color=ACCENT_TEAL, text_color=BG_ROOT, border_width=0)
        else:
            btn.configure(fg_color=BG_SURFACE, hover_color=BG_CARD_HOVER, text_color=TEXT_DIM, border_width=2, border_color=BORDER_COLOR)

    def _parse_dnd_files(self, event_data):
        files = re.findall(r'\{[^\}]+\}|[^\s]+', event_data)
        return [f.strip('{}') for f in files if f.lower().endswith('.3mf')]

    def al_entrar_drag(self, event):
        self.dropzone.configure(text=self.T("drop_hover"), border_color=ACCENT_TEAL, text_color=ACCENT_TEAL)
        
    def al_salir_drag(self, event):
        self.dropzone.configure(text=self.T("drop_idle"), border_color=BORDER_COLOR, text_color=TEXT_DIM)

    def al_soltar_archivo(self, event):
        self.al_salir_drag(event)
        files = self._parse_dnd_files(event.data)
        if files: self._procesar_y_extraer_datos(files)

    def cargar_3mf_manual(self):
        r = filedialog.askopenfilenames(filetypes=[("3MF", "*.3mf")])
        if r: self._procesar_y_extraer_datos(r)

    def extraer_miniatura(self, z, size=260):
        if not PIL_SUPPORT: return None
        for name in z.namelist():
            if name.lower().endswith('.png') and ('thumbnail' in name.lower() or 'plate' in name.lower() or 'top' in name.lower()):
                try:
                    img_data = z.read(name)
                    img = Image.open(io.BytesIO(img_data))
                    img.thumbnail((size, size), Image.Resampling.LANCZOS)
                    return ctk.CTkImage(light_image=img, dark_image=img, size=(img.width, img.height))
                except: pass
        return None

    def _procesar_y_extraer_datos(self, files):
        try:
            self.rutas_3mf_actuales = files
            self.batch_data = []
            
            tipos_disp = list(set([f['type'] for f in self.available_filaments]))
            self.tipos_disponibles = tipos_disp if tipos_disp else ["PLA", "PETG", "ABS", "TPU"]

            for idx_f, path in enumerate(files):
                t_s, w_g, fils, plates_count = 0, 0, [], 1
                img_small = None
                det_nozzle = "0.4"
                f_data_detected = {k: {} for k in CONVERTER_PARAMS.keys()}
                
                with zipfile.ZipFile(path, 'r') as z:
                    img_small = self.extraer_miniatura(z, size=150 if len(files)==1 else 90)

                    if "Metadata/slice_info.config" in z.namelist():
                        c = z.read("Metadata/slice_info.config").decode('utf-8', 'ignore')
                        m_t = re.search(r'key="(?:prediction|estimated_time)" value="([^"]+)"', c)
                        m_w = re.search(r'key="weight" value="([^"]+)"', c)
                        t_s, w_g = float(m_t.group(1)) if m_t else 0, float(m_w.group(1)) if m_w else 0
                        try:
                            root = ET.fromstring(c)
                            plates_count = len(root.findall('.//plate'))
                            if plates_count == 0: plates_count = 1
                            for f in root.findall('.//filament'): 
                                fils.append({'id':f.get('id'), 'color':self.normalize_color(f.get('color')), 'type':f.get('type','PLA')})
                        except: pass
                    
                    if 'Metadata/project_settings.config' in z.namelist():
                        cfg = json.loads(z.read('Metadata/project_settings.config').decode('utf-8', 'ignore'))
                        nozzle_list = cfg.get("nozzle_diameter", ["0.4"])
                        det_nozzle = nozzle_list[0] if nozzle_list else "0.4"
                        
                        if not fils:
                            for i, (col, typ) in enumerate(zip(cfg.get('filament_colour',[]), cfg.get('filament_type',[]))):
                                fils.append({'id':str(i+1), 'color':self.normalize_color(col), 'type':typ})
                                
                        for cat, keys_list in CONVERTER_PARAMS.items():
                            for k in keys_list:
                                if k in cfg:
                                    val = cfg[k]
                                    if isinstance(val, list):
                                        if len(val) > 0 and all(x == val[0] for x in val): val = self.format_val(val[0])
                                        else: val = f"[{', '.join(str(x) for x in val)}]"
                                    else:
                                        val = self.format_val(val)
                                    f_data_detected[cat][k] = val
                                
                for f in fils:
                    if f['type'] not in self.tipos_disponibles:
                        self.tipos_disponibles.append(f['type'])
                
                self.batch_data.append({
                    "path": path,
                    "filename": os.path.basename(path),
                    "time": t_s,
                    "weight": w_g,
                    "nozzle": det_nozzle,
                    "filaments": fils,
                    "plates": plates_count,
                    "thumb_small": img_small,
                    "combos_ui": [],
                    "color_btns_ui": [],
                    "detected_params": f_data_detected
                })

            is_batch = len(files) > 1
            self.dropzone.pack_forget()
            self.info_card.pack(side="top", fill="both", expand=True, pady=(0, 20))
            self.btn_change.pack(fill="x")
            
            self.btn_save.configure(state="normal", text=self.T("btn_save_batch") if is_batch else self.T("btn_save_as"))
            self.btn_open.configure(state="normal")
            self.btn_inspector.configure(state="normal")
            
            if is_batch:
                self.lbl_file.configure(text=self.T("batch_mode").format(len(files)), text_color=ACCENT_ORANGE)
            else:
                self.lbl_file.configure(text=f"📁 {self.batch_data[0]['filename']}", text_color=ACCENT_TEAL)
            self.lbl_file.pack(pady=(20, 5), padx=25, anchor="w")

            for widget in self.batch_scroll.winfo_children(): widget.destroy()
            self.batch_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            for f_data in self.batch_data:
                card = ctk.CTkFrame(self.batch_scroll, fg_color=BG_ROOT, corner_radius=12)
                card.pack(fill="x", pady=6, padx=5, ipadx=10, ipady=10)
                
                top_f = ctk.CTkFrame(card, fg_color="transparent")
                top_f.pack(fill="x", padx=5)
                
                if f_data['thumb_small']:
                    ctk.CTkLabel(top_f, image=f_data['thumb_small'], text="").pack(side="left", padx=(0, 15))
                else:
                    ctk.CTkLabel(top_f, text="[IMG]", font=ctk.CTkFont(size=10), text_color=TEXT_DIM, width=70).pack(side="left", padx=(0, 15))
                
                info_right = ctk.CTkFrame(top_f, fg_color="transparent")
                info_right.pack(side="left", fill="both", expand=True)
                
                if is_batch:
                    fname = f_data['filename'] if len(f_data['filename']) < 30 else f_data['filename'][:27] + "..."
                    ctk.CTkLabel(info_right, text=fname, font=ctk.CTkFont(size=13, weight="bold"), text_color=ACCENT_TEAL).pack(anchor="w", pady=(2, 2))
                
                s_f = ctk.CTkFrame(info_right, fg_color="transparent")
                s_f.pack(anchor="w")
                time_str = f"{int(f_data['time']//3600)}h {int((f_data['time']%3600)//60)}m" if f_data['time']>0 else "--"
                weight_str = f"{f_data['weight']:.1f}g" if f_data['weight']>0 else "--"
                ctk.CTkLabel(s_f, text=f"⏱️ {time_str}   ⚖️ {weight_str}   📏 {f_data['nozzle']}mm", font=ctk.CTkFont(size=11), text_color=TEXT_DIM).pack(side="left")

                if f_data['plates'] > 1:
                    ctk.CTkLabel(info_right, text=self.T("multi_plate").format(f_data['plates']), font=ctk.CTkFont(size=10, weight="bold"), text_color=ACCENT_ORANGE).pack(anchor="w", pady=(2,0))

                if f_data['filaments']:
                    fil_grid = ctk.CTkFrame(card, fg_color="transparent")
                    fil_grid.pack(fill="x", padx=5, pady=(10, 0))
                    fil_grid.grid_columnconfigure((0, 1), weight=1)
                    
                    f_data['combos_ui'] = []
                    
                    for idx, fil in enumerate(f_data['filaments'][:TARGET_FILAMENTS]):
                        fila = ctk.CTkFrame(fil_grid, fg_color="transparent")
                        fila.grid(row=idx//2, column=idx%2, sticky="w", pady=2)
                        
                        c_btn = ctk.CTkButton(fila, text="", width=14, height=14, corner_radius=7, 
                                              fg_color=fil['color'], hover_color=fil['color'], border_width=1, border_color=TEXT_DIM)
                        c_btn.configure(command=lambda f_ref=fil, b_ref=c_btn: self.cambiar_color_filamento(f_ref, b_ref))
                        c_btn.pack(side="left", padx=(0, 5))

                        ctk.CTkLabel(fila, text=f"E{idx+1}:", font=ctk.CTkFont(size=11, weight="bold"), text_color=TEXT_DIM).pack(side="left", padx=(0, 5))
                        
                        combo = ctk.CTkOptionMenu(fila, values=self.tipos_disponibles, width=80, height=22,
                                                  fg_color=BG_SURFACE, button_color=BG_SURFACE, 
                                                  button_hover_color=BG_CARD_HOVER, font=ctk.CTkFont(size=11, weight="bold"))
                        combo.set(fil['type'])
                        combo.pack(side="left")
                        f_data['combos_ui'].append(combo)

            self._aplicar_scroll_seguro(self.batch_scroll, self.batch_scroll)

        except Exception as e:
            print(f"Error cargando archivo: {e}")

    def preparar_datos_motor(self):
        for f_data in self.batch_data:
            if 'combos_ui' in f_data and f_data['combos_ui']:
                for i, cb in enumerate(f_data['combos_ui']):
                    if i < len(f_data['filaments']):
                        f_data['filaments'][i]['type'] = cb.get()

    def accion_guardar_como(self):
        self.preparar_datos_motor()
        if len(self.batch_data) > 1:
            self.set_ui_loading(True)
            threading.Thread(target=self._hilo_procesar_lote, args=(False,)).start()
        else:
            f = filedialog.asksaveasfilename(defaultextension=".3mf", filetypes=[("3MF", "*.3mf")])
            if f:
                self.set_ui_loading(True)
                threading.Thread(target=self._hilo_procesar, args=(self.batch_data[0], f, False)).start()

    def accion_guardar_y_abrir(self):
        self.preparar_datos_motor()
        self.set_ui_loading(True)
        if len(self.batch_data) > 1:
            threading.Thread(target=self._hilo_procesar_lote, args=(True,)).start()
        else:
            f_data = self.batch_data[0]
            p = os.path.join(os.path.dirname(f_data['path']), f"{os.path.splitext(f_data['filename'])[0]}_U1.3mf")
            threading.Thread(target=self._hilo_procesar, args=(f_data, p, True)).start()

    def _hilo_procesar_lote(self, abrir_despues):
        success = True
        msg = ""
        archivos_procesados = []
        for f_data in self.batch_data:
            p = os.path.join(os.path.dirname(f_data['path']), f"{os.path.splitext(f_data['filename'])[0]}_U1.3mf")
            s, m = self._ejecutar_motor(f_data, p)
            if not s: 
                success = False
                msg = m
                break
            archivos_procesados.append(p)
        
        self.after(0, self._finalizar_procesamiento_lote, success, msg, archivos_procesados, abrir_despues)

    def _finalizar_procesamiento_lote(self, success, msg, archivos_procesados, abrir_despues):
        self.set_ui_loading(False)
        if success:
            for widget in self.batch_scroll.winfo_children(): widget.destroy()
            ctk.CTkLabel(self.batch_scroll, text=self.T("msg_success"), font=ctk.CTkFont(size=18, weight="bold"), text_color=COLOR_SUCCESS).pack(pady=40)
            if abrir_despues:
                for i, p in enumerate(archivos_procesados):
                    self.after(i * 1000, lambda file_path=p: self.abrir_en_slicer(file_path))
        else:
            for widget in self.batch_scroll.winfo_children(): widget.destroy()
            ctk.CTkLabel(self.batch_scroll, text=self.T("msg_error").format(msg), font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_ERROR).pack(pady=40)

    def _hilo_procesar(self, f_data, r_out, abrir_despues):
        success, msg = self._ejecutar_motor(f_data, r_out)
        self.after(0, self._finalizar_procesamiento, success, msg, r_out, abrir_despues)

    def _finalizar_procesamiento(self, success, msg, p, abrir_despues):
        self.set_ui_loading(False)
        if success:
            for widget in self.batch_scroll.winfo_children(): widget.destroy()
            ctk.CTkLabel(self.batch_scroll, text=self.T("msg_success"), font=ctk.CTkFont(size=18, weight="bold"), text_color=COLOR_SUCCESS).pack(pady=40)
            if abrir_despues and p:
                self.abrir_en_slicer(p)
        else:
            for widget in self.batch_scroll.winfo_children(): widget.destroy()
            ctk.CTkLabel(self.batch_scroll, text=self.T("msg_error").format(msg), font=ctk.CTkFont(size=14, weight="bold"), text_color=COLOR_ERROR).pack(pady=40)

    def abrir_en_slicer(self, p):
        sys_os = platform.system()
        try:
            if sys_os == "Darwin": subprocess.Popen(["open", "-n", "-a", "Snapmaker Orca", p])
            elif sys_os == "Windows": os.startfile(p)
            else: subprocess.Popen(["xdg-open", p])
        except: pass

    def _ejecutar_motor(self, f_data, r_out):
        keys = set()
        r_in = f_data['path']
        for k, v in self.states.items():
            if v: keys.update(CONVERTER_PARAMS[k])
        
        try:
            with zipfile.ZipFile(r_in, 'r') as zin, zipfile.ZipFile(r_out, 'w', zipfile.ZIP_DEFLATED) as zout:
                orig = {}
                for n in zin.namelist():
                    if n.startswith("Config/") or n == 'Metadata/project_settings.config':
                        try: orig.update(json.loads(zin.read(n).decode('utf-8')))
                        except: pass
                
                temp_name = 'u1_template_supports.3mf' if any('enable_support' in str(s) for s in orig.get('different_settings_to_system',[])) else 'u1_template.3mf'
                path_template = resource_path(temp_name)
                
                with zipfile.ZipFile(path_template, 'r') as zt: 
                    comb = json.loads(zt.read('Metadata/project_settings.config').decode('utf-8'))
                
                nozzle_key = str(f_data['nozzle'])
                perfil_data = NOZZLE_PROFILES.get(nozzle_key, NOZZLE_PROFILES["0.4"])
                comb['printer_model'] = perfil_data['machine']
                comb['default_print_profile'] = perfil_data['profile']
                
                cols = [f['color'] for f in f_data['filaments']]
                typs = [f['type'] for f in f_data['filaments']]

                new_c = [(c+'FF' if len(c)==7 else c).upper() for c in (cols + ['#FFFFFFFF']*4)[:4]]
                new_t = (typs + ['PLA']*4)[:4]
                comb.update({'filament_colour':new_c, 'filament_type':new_t})
                
                p_map = {f['type']: f['settings_id'] for f in self.available_filaments}
                comb['filament_settings_id'] = [p_map.get(t, DEFAULT_FILAMENT_PROFILE) for t in new_t]
                
                inj = []
                for k in keys:
                    if k in orig:
                        target_key = KEY_TRANSLATIONS.get(k, k)
                        comb[target_key] = orig[k]
                        inj.append(target_key)
                
                if inj:
                    diff = comb.get("different_settings_to_system", [""]*5)
                    exist = [x for x in diff[0].split(";") if x]
                    diff[0] = ";".join(sorted(list(set(exist + inj))))
                    comb["different_settings_to_system"] = diff

                bambu_ns = 'http://schemas.bambulab.com/package/2021'
                slic3r_ns = 'http://schemas.slic3r.org/3mf/2017'
                core_ns = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
                
                ET.register_namespace('', core_ns)
                ET.register_namespace('slic3r', slic3r_ns)
                ET.register_namespace('p', 'http://schemas.microsoft.com/3dmanufacturing/production/2015/06')

                for item in zin.infolist():
                    name = posixpath.normpath(item.filename).lstrip('/')
                    if name == 'Metadata/project_settings.config':
                        zout.writestr(item, json.dumps(comb, indent=4))
                    elif name == 'Metadata/slice_info.config':
                        xml = zin.read(item.filename).decode('utf-8','ignore')
                        xml = re.sub(r'key="printer_model_id" value="[^"]*"', f'key="printer_model_id" value="{perfil_data["machine"]}"', xml)
                        zout.writestr(item, xml.encode('utf-8'))
                    elif name.startswith('3D/') and name.endswith('.model'):
                        xml_raw = zin.read(item.filename)
                        try:
                            root = ET.fromstring(xml_raw)
                            for meta in root.findall(f'.//{{{core_ns}}}metadata'):
                                name_attr = meta.get('name')
                                if name_attr and name_attr.startswith('BambuStudio:'):
                                    meta.set('name', name_attr.replace('BambuStudio:', 'slic3r:'))
                            for elem in root.iter():
                                if elem.tag.startswith(f'{{{bambu_ns}}}'):
                                    elem.tag = elem.tag.replace(f'{{{bambu_ns}}}', f'{{{slic3r_ns}}}')
                                for attr_name in list(elem.attrib.keys()):
                                    if attr_name.startswith(f'{{{bambu_ns}}}'):
                                        new_attr = attr_name.replace(f'{{{bambu_ns}}}', f'{{{slic3r_ns}}}')
                                        elem.set(new_attr, elem.attrib.pop(attr_name))
                            xml_out = ET.tostring(root, encoding='utf-8', xml_declaration=True)
                            zout.writestr(item, xml_out)
                        except Exception as parse_e:
                            print(f"ET Fallback en {name}: {parse_e}")
                            xml_str = xml_raw.decode('utf-8', 'ignore')
                            xml_str = xml_str.replace('xmlns:BambuStudio=', 'xmlns:slic3r=').replace('name="BambuStudio:', 'name="slic3r:').replace('<BambuStudio:', '<slic3r:').replace('</BambuStudio:', '</slic3r:').replace(' BambuStudio:', ' slic3r:')
                            zout.writestr(item, xml_str.encode('utf-8'))
                    else:
                        zout.writestr(item, zin.read(item.filename))
            return True, ""
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    app = U1SlicerApp()
    app.mainloop()
