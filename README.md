
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

# สรุปคำสั่งจาก ตงตง
1) S1 (switch) แก้พอร์ตที่ต่อกับ R2 ให้ถูก
ปัญหา: พอร์ตนี้ตั้งเป็น trunk (ส่ง tag VLAN) ทั้งที่ R2 อ่าน tag ไม่ได้
```shell
conf t
interface Gi0/3
 no switchport trunk allowed vlan 99,101
 switchport mode access
 switchport access vlan 101
end
wr mem
```

ผล: ping จาก ubuntuserver26x-2 ไป 10.1.2.1 ผ่านได้
2) R2 เปิดใช้งาน OSPF (ฝั่ง control-data)
ปัญหา: ไม่เคยเปิด OSPF เลย ทำให้ R1 ไม่รู้จัก route ไปเครือข่าย 10.1.2.0/24
```shell
conf t
router ospf 1 vrf control-data
 network 10.1.12.0 0.0.0.3 area 0
 network 10.1.2.0 0.0.0.255 area 0
 passive-interface GigabitEthernet0/3
end
wr mem
```

3) R1 เปิดใช้งาน OSPF (ฝั่ง control-data) เช่นกัน
```shell
conf t
router ospf 1 vrf control-data
 network 10.1.12.0 0.0.0.3 area 0
 network 10.1.1.0 0.0.0.255 area 0
end
wr mem
```

ผล: R1 ping ไป G0/3 ของ R2 (10.1.2.1) และ G0/0 ของ R0 ผ่านหมด
4) R2 ย้ายพอร์ตที่ต่อ NAT cloud เข้าไปอยู่ใน vrf control-data
ปัญหา: พอร์ตนี้เดิมอยู่ผิดโซน (global) ทำให้เครื่อง ubuntu ที่อยู่ฝั่ง control-data ไปเน็ตไม่ได้
```shell
conf t
interface Gi0/0
 no ip address
 vrf forwarding control-data
 ip address dhcp
end
```

5) R2 ประกาศเส้นทางออกเน็ตเข้า OSPF + ตั้งค่า NAT (PAT)
ให้ R1 และเครื่อง ubuntu รู้จักทางออกอินเทอร์เน็ต แล้วแปลง IP ตอนออกไป
```shell
conf t
router ospf 1 vrf control-data
 default-information originate
exit
ip access-list standard NAT_INSIDE
 permit 10.1.0.0 0.0.255.255
exit
interface Gi0/0
 ip nat outside
exit
interface Gi0/1
 ip nat inside
exit
interface Gi0/3
 ip nat inside
exit
ip nat inside source list NAT_INSIDE interface GigabitEthernet0/0 vrf control-data overload
end
wr mem
```

ผล: R2 และ R1 ping 1.1.1.1 / 8.8.8.8 ผ่าน 100%

# ไม่รู้จะให้อะไรจากซี (Maybe ใช้ได้แต่ได้ใช้)

## Authentication Network คณะ
```bash
curl -X POST "https://login.it.kmitl.ac.th/auth" -k -H "Content-Type: application/json" -d '{"username":"","password":""}'
```

## SSH Router
```bash
ssh -o KexAlgorithms=+diffie-hellman-group14-sha1 -o HostKeyAlgorithms=+ssh-rsa -o PubkeyAcceptedKeyTypes=+ssh-rsa admin@<IP Router>
```

## SSH Switch
```bash
ssh -o KexAlgorithms=+diffie-hellman-group14-sha1,diffie-hellman-group1-sha1 -o HostKeyAlgorithms=+ssh-rsa,ssh-dss -o Ciphers=+aes128-cbc,3des-cbc -o MACs=+hmac-sha1,hmac-sha1-96 admin@<IP Switch>
```
