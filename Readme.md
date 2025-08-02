# 🛡️ Shell-Assist

**Shell-Assist** is a smart Linux shell assistant that translates natural language commands into secure shell commands with an added layer of risk analysis. Powered by a local LLM using Ollama, Shell-Assist helps users interact with their terminal safely and efficiently.

---

## 🚀 Features

- 🧠 **Natural Language to Shell Command Translation**
- 🔍 **Command Risk Scoring (0–10)**
- 🎨 **Color-Coded Risk Levels**
- 📘 **Command Explanation Before Execution**
- 🕓 **Command History Viewer (`history` command)**
- 📝 **Automatic Logging of Executed Commands**
- 🛑 **Execution Confirmation Prompt**
- ⚙️ **Locally Hosted & Privacy-Focused (uses Ollama + Phi model)**

---

## 🔐 Risk Levels

| Score | Level         | Description                                      |
|-------|---------------|--------------------------------------------------|
| 0–2   | ✅ Safe        | Read-only or system information commands         |
| 3–4   | ⚠️ Low Risk    | File or directory operations in user space       |
| 5–6   | 🟠 Medium Risk | System or network queries                        |
| 7–8   | 🔴 High Risk   | System modifications or package installations    |
| 9–10  | ❌ Extreme     | Data deletion or system-critical operations      |

---

## 📦 Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com) installed and running
- `phi` or `tinyllama` model pulled via Ollama
- `rich` library for CLI UI

```bash
pip install rich
ollama pull phi  # or use: ollama pull tinyllama
