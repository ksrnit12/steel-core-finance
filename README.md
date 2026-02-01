# 🛡️ Steel Core Finance Engine

**Neuro-Symbolic AI That Eliminates Hallucinations in Financial Analysis**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 The Problem

Traditional AI systems **hallucinate** when processing financial data.

* **User:** "What is our Q4 profit?"
* **LLM:** "Your Q4 profit is approximately $4.2M"
* **Reality:** Actually $2.1M
* **Consequence:** Audit failure → Lawsuit

---

## ✅ The Solution: The Steel Core Pattern

A **three-layer architecture** that guarantees zero hallucinations:

1. **ROUTER** → Classifies intent, blocks LLM from guessing
2. **STEEL CORE (Python Logic)** → Deterministic calculations only
3. **VOICE LAYER (Optional LLM)** → Natural language formatting only

**Key Principle:**  
The LLM **never** sees raw data or performs calculations.  
Python does the math. The LLM just makes it readable.

---

## 🔥 Key Features

### 1. Zero Hallucinations
- All financial calculations use deterministic Python/Pandas
- Every result is mathematically verifiable

### 2. Cryptographic Audit Trail
Every calculation gets a unique, verifiable Audit ID:  
`Total Profit: $4,876,543.21 (Audit ID: a3f5e9d2c1b8f4a7)`

### 3. Enterprise-Ready
- SOX / GAAP compliant immutable audit logs (append-only, SHA256)
- Full traceability: drill down to transaction

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/ksrnit12/steel-core-finance.git
cd steel-core-finance
pip install pandas
```

### Basic Usage

```bash
python3 steel_core.py
```

---

## 📄 License

This project is licensed under the MIT License.  
**Copyright (c) 2026**
