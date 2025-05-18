# 🌞 Solar Challenge – Week 0

Welcome to the **Solar Challenge Week 0** project!  
This repository documents the initial setup and exploration work for the challenge, including:

- ✅ Git & environment setup
- ✅ Package installation
- ✅ EDA notebook and initial insights
- ✅ GitHub Actions workflow

---

## 📁 Project Structure

```
solar-challenge-week-0/
├── .github/workflows/ci.yml     # GitHub Actions CI setup
├── .vscode/settings.json        # VSCode settings
├── notebooks/                   # Jupyter notebooks (EDA work)
├── scripts/                     # Python utility scripts
├── tests/                       # Test modules
├── requirements.txt             # Project dependencies
├── interim_report.md            # Week 0 report
├── README.md                    # This file
```

---

## 🛠 Environment Setup

To reproduce the development environment:

### 1. Clone the Repository

```bash
git clone https://github.com/5237-mests/solar-challenge-week-0.git
cd solar-challenge-week-0
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

- On Linux/macOS:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

### 3. Install Required Packages

```bash
pip install -r requirements.txt
```

---

## ⚙️ GitHub Actions

This repo includes a CI workflow that installs dependencies on each push to `main`.

Workflow file: `.github/workflows/ci.yml`

It uses:

```yaml
- uses: actions/setup-python@v4
- run: pip install -r requirements.txt
```

This ensures your project is installable and the environment is reproducible.

---

## 🧾 Interim Report

The [interim_report.md](interim_report.md) includes:

- ✅ Task 1: Git & Environment setup summary
- ✅ Task 2: Profiling, cleaning, and EDA plan

---

## 📬 Contact

- 👤 Mesfin Mulugeta
- 🌐 [LinkedIn](https://www.linkedin.com/in/mesfin-mulgeta)
- 📧 msfnmulgeta@gmail.com

---
