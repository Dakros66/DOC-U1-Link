# DOC U1 Link 🔗

**DOC U1 Link** is a professional workflow utility designed exclusively for **Snapmaker U1** users.

It acts as an intelligent bridge that transforms **Bambu Studio `.3mf`** projects (commonly downloaded from MakerWorld) into files that are fully compatible and optimized for **Snapmaker Orca**.

![License](https://img.shields.io/badge/license-GPLv3-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-orange.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows-lightgrey.svg)

---

# 🌟 Key Features

## 🧠 Smart Data Surgery

Automatically removes unsafe or incompatible Bambu Lab hardware parameters, including:

- Kinematic limits
- Start G-code
- Bed dimensions
- Machine-specific settings

This helps prevent slicing conflicts and unsafe printer behavior.

---

## 🖨️ U1 Profile Injection

Automatically injects optimized **Snapmaker U1** printer and process profiles using high-quality base templates.

---

## 🎛️ Selective Preservation (Whitelist System)

Choose exactly which settings should be preserved from the original `.3mf` project.

### ✨ Quality Settings
- Layer heights
- Surface patterns
- Seam settings
- Fuzzy Skin

### 💪 Strength Settings
- Infill density
- Wall loops
- Structural patterns

### 🚧 Support Settings
- Tree supports
- Standard supports
- Support interface options

### ⚡ Speed Settings
Choose between:
- Original creator speeds
- Your local safe U1 profile speeds

---

## 🚀 One-Click Workflow

- ✅ Drag & Drop support
- ✅ Automatic AMS color mapping (up to 4 extruders)
- ✅ Auto-save converted projects
- ✅ Automatically launches Snapmaker Orca

---

# 🚀 Installation

## Requirements

- Python **3.9+**
- Windows or macOS

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Dakros66/DOC-U1-Link.git
cd DOC-U1-Link
```

---

## 2️⃣ Install Dependencies

```bash
pip install customtkinter tkinterdnd2 Pillow
```

---

## 3️⃣ Run the Application

```bash
python DOC-U1-Link.py
```

---

# 📂 Required Files

For proper conversion, make sure the following files are located in the same folder as the script:

| File | Description |
|------|-------------|
| `u1_template.3mf` | Base template for prints without supports |
| `u1_template_supports.3mf` | Base template for prints with supports |
| `filament_types.3mf` | Filament mapping dictionary |
| `esperando.gif` *(optional)* | Loading animation (~450x120 recommended) |

---

# 🛠️ How to Use

## 1️⃣ Load a File

Drag & drop a **Bambu Studio `.3mf`** file into the application window  
or load it manually.

---

## 2️⃣ Configure Settings

Enable or disable the parameters you want to preserve from the original project.

---

## 3️⃣ Convert the Project

Click:

```text
Auto-Save & Open Orca
```

---

## 4️⃣ Print

Snapmaker Orca will open automatically with your converted project ready to slice and print on your **Snapmaker U1**.

---

# ℹ️ Authorized Parameters

The application uses a strict **Whitelist System** to ensure machine safety and compatibility.

You can inspect the full list of exported parameters by clicking the **ℹ️ icon** inside the application.

---

# 🤝 Contributions

Contributions are welcome!

If you discover:
- Missing whitelist parameters
- Compatibility issues
- Workflow improvements

feel free to:
- Open an **Issue**
- Submit a **Pull Request**

---

# ⚖️ License

This project is licensed under the **GNU GPLv3**.

See the `LICENSE` file for more information.

---

# 👨‍💻 Author

Developed by **Dakros66**
