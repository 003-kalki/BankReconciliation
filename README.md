# 💰 Bank Reconciliation Automation Tool

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Docker](https://img.shields.io/badge/Dockerized-Yes-2496ED)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Status-Active-brightgreen)

A powerful automation tool built with Python to perform high-speed, reliable **bank transaction reconciliation**.  
Perfect for accountants, businesses, and devs who are tired of doing it manually.

---

## 🚀 Features

- 🔍 **Automatic Reconciliation** of bank transactions
- 📊 Supports **Excel (.xlsx)** and **CSV** formats
- ✅ Detects and highlights **mismatches**
- 📁 Outputs easy-to-read reports
- 🐳 **Dockerized** for smooth deployment anywhere
- 🧪 Test coverage via `pytest`
- ⚙️ Modular design, easy to extend

---

## 📦 Tech Stack

- Python 3.12
- `pandas`, `numpy`, `openpyxl`, `selenium`
- Docker 🐳
- Pytest for testing

---


## ⚙️ Installation & Usage

### 🔧 Local Setup

```bash
git clone https://github.com/yourusername/bankAutomation.git
cd bankAutomation
pip install -r requirements.txt
python app/reconciler.py

🐳 Docker Setup
# Build the Docker image
docker build -t bank-reconciliation-tool .

# Run the container (mounting local data folder)
docker run -v $(pwd)/data:/app/data bank-reconciliation-tool
