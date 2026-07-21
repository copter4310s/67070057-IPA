
# 67070057-IPA

นายทีปดา ชื่นเปรมปรีดิ์ 67070057

# UV (Python Package Manager) แบบง่าย ๆ จากพีพีนะอิอิ
## 1. ติดตั้ง uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
### หรือผ่าน pip
```bash
pip install uv
```
# สร้าง Virtual Environment
```bash
uv venv
```

### Activate (Linux/macOS)
```bash
source .venv/bin/activate
```
### Activate (Windows)

```powershell
.venv\Scripts\activate
```
> **หมายเหตุ:** สามารถใช้ `uv run` ได้โดยไม่ต้อง Activate Virtual Environment

# 3. ติดตั้ง Package
ติดตั้ง Package เดียว
```bash
uv add numpy
```
ติดตั้งหลาย Package
```bash
uv add numpy pandas matplotlib
```

# รัน script
```bash
uv run main.py
```

```bash
uv run python main.py
```

# ลบ Package
```bash
uv remove numpy
```

# ติดตั้ง Dependency จากโปรเจกต์
```bash
uv sync
```
เหมาะสำหรับหลังจาก Clone โปรเจกต์จาก Git แล้วก็ uv sync ได้เลยแบบง่ายๆๆ

สร้าง Virtual Environment ด้วย Python 3.12
```bash
uv venv --python 3.12
```

# ใช้งานกับ requirements.txt
ติดตั้ง
```bash
uv pip install -r requirements.txt
```

สร้างไฟล์ requirements.txt
```bash
uv pip freeze > requirements.txt
```

# คำสั่งที่ใช้บ่อย

| คำสั่ง | ความหมาย |
|---------|-----------|
| `uv init` | สร้างโปรเจกต์ใหม่ |
| `uv venv` | สร้าง Virtual Environment |
| `uv add <package>` | ติดตั้ง Package |
| `uv remove <package>` | ลบ Package |
| `uv sync` | ติดตั้ง Dependency ทั้งหมด |
| `uv run <file>` | รันโปรแกรม |
| `uv python install <version>` | ติดตั้ง Python |
| `uv lock` | อัปเดตไฟล์ Lock |
| `uv tree` | แสดง Dependency Tree |
