#!/usr/bin/env python3
"""Generate Activity Diagrams matching sample style: B&W swimlanes."""
import os
OUT = "/Users/Study/DOAN/z pos-source-code_1/diagrams"

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

# Styles - all black & white matching sample
ACT = "rounded=1;whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor=#000000;fontSize=11;"
DEC = "rhombus;whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor=#000000;fontSize=10;"
ST = "ellipse;whiteSpace=wrap;html=0;aspect=fixed;fillColor=#000000;strokeColor=#000000;"
# End = outer ring + inner fill
EN_OUT = "ellipse;whiteSpace=wrap;html=0;aspect=fixed;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;"
EN_IN = "ellipse;whiteSpace=wrap;html=0;aspect=fixed;fillColor=#000000;strokeColor=#000000;"
LANE = "swimlane;startSize=30;html=0;fillColor=#ffffff;strokeColor=#000000;fontStyle=1;fontSize=12;"
EDGE = "endArrow=open;endSize=8;html=0;strokeColor=#000000;fontSize=9;rounded=0;curved=0;"
TITLE = "text;html=0;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontStyle=1;fontSize=14;"

def n(id,val,style,x,y,w,h,par="1"):
    return f'<mxCell id="{id}" value="{esc(val)}" style="{style}" vertex="1" parent="{par}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'

def e(id,src,tgt,lbl=""):
    v = f' value="{esc(lbl)}"' if lbl else ' value=""'
    return f'<mxCell id="{id}"{v} style="{EDGE}" edge="1" source="{src}" target="{tgt}" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>'

def start(id,x,y,par="1"):
    return n(id,"",ST,x,y,30,30,par)

def end(id,x,y,par="1"):
    o = n(id+"o","",EN_OUT,x,y,30,30,par)
    i = n(id+"i","",EN_IN,x+7,y+7,16,16,par)
    return o+"\n"+i

def act(id,val,x,y,w=200,h=40,par="1"):
    return n(id,val,ACT,x,y,w,h,par)

def dec(id,val,x,y,w=120,h=60,par="1"):
    return n(id,val,DEC,x,y,w,h,par)

def wrap(did,name,cells,pw="1000",ph="1400"):
    return f'''<mxfile>
<diagram id="{did}" name="{name}">
<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{pw}" pageHeight="{ph}" math="0" shadow="0">
<root>
<mxCell id="0"/><mxCell id="1" parent="0"/>
{chr(10).join(cells)}
</root>
</mxGraphModel>
</diagram>
</mxfile>'''

# ============================================================
# ACT01: Đăng ký tài khoản
# Lanes: Người dùng mới (300w) | Hệ thống (400w)
# ============================================================
def act01():
    c = []
    c.append(n("t","Biểu đồ hoạt động: Đăng ký tài khoản",TITLE,20,10,700,30))
    c.append(n("L0","Người dùng mới",LANE,20,50,300,1050))
    c.append(n("L1","Hệ thống",LANE,320,50,400,1050))
    # Start
    c.append(start("s",135,50,"L0"))
    # Actions in Lane 0 (Người dùng) - coords relative to lane
    c.append(act("a1","Chọn Đăng ký",50,110,200,40,"L0"))
    c.append(act("a2","Nhập thông tin:\nfullName, email, password, phone",30,180,240,50,"L0"))
    # Actions in Lane 1 (Hệ thống)
    c.append(act("a3","Gửi POST /auth/signup\nđến AuthController",100,110,220,50,"L1"))
    c.append(act("a4","Kiểm tra email\ntrong Database",100,200,220,40,"L1"))
    c.append(dec("d1","Email đã\ntồn tại?",110,270,120,70,"L1"))
    c.append(act("a5","Trả lỗi:\nEmail already exists",100,400,220,40,"L1"))
    c.append(dec("d2","Role =\nROLE_ADMIN?",110,480,120,70,"L1"))
    c.append(act("a6","Trả lỗi:\nKhông thể đăng ký Admin",100,610,220,40,"L1"))
    c.append(act("a7","Mã hóa password\nbằng BCryptPasswordEncoder",100,700,220,50,"L1"))
    c.append(act("a8","Tạo User mới\nvà lưu vào Database",100,780,220,40,"L1"))
    c.append(act("a9","Tạo JWT Token\n(JwtProvider.generateToken)",100,850,220,50,"L1"))
    c.append(act("a10","Trả về { jwt, user }",100,930,220,40,"L1"))
    # Back to Lane 0
    c.append(act("a11","Lưu JWT vào localStorage\nĐiều hướng vào hệ thống",30,930,240,50,"L0"))
    c.append(end("end",135,1010,"L0"))
    # Edges
    c.append(e("e1","s","a1"))
    c.append(e("e2","a1","a2"))
    c.append(e("e3","a2","a3"))
    c.append(e("e4","a3","a4"))
    c.append(e("e5","a4","d1"))
    c.append(e("e6","d1","a5","Có"))
    c.append(e("e7","d1","d2","Không"))
    c.append(e("e8","d2","a6","Có"))
    c.append(e("e9","d2","a7","Không"))
    c.append(e("e10","a7","a8"))
    c.append(e("e11","a8","a9"))
    c.append(e("e12","a9","a10"))
    c.append(e("e13","a10","a11"))
    c.append(e("e14","a11","endo"))
    c.append(e("e15","a5","endo"))
    c.append(e("e16","a6","endo"))
    return wrap("act01","Đăng ký tài khoản",c,"800","1200")

# ============================================================
# ACT02: Đăng nhập
# Lanes: Người dùng (300w) | Hệ thống (400w)
# ============================================================
def act02():
    c = []
    c.append(n("t","Biểu đồ hoạt động: Đăng nhập",TITLE,20,10,700,30))
    c.append(n("L0","Người dùng",LANE,20,50,300,1150))
    c.append(n("L1","Hệ thống",LANE,320,50,400,1150))
    c.append(start("s",135,50,"L0"))
    # Lane 0
    c.append(act("a1","Chọn Đăng nhập",50,110,200,40,"L0"))
    c.append(act("a2","Nhập email và password",50,180,200,40,"L0"))
    # Lane 1
    c.append(act("a3","Gửi POST /auth/login\nđến AuthController",100,180,220,50,"L1"))
    c.append(act("a4","loadUserByUsername(email)\nTìm User trong Database",100,270,220,50,"L1"))
    c.append(dec("d1","User\ntồn tại?",110,350,120,70,"L1"))
    c.append(act("a5","Trả lỗi:\nUser not found",100,470,220,40,"L1"))
    c.append(act("a6","passwordEncoder.matches()\nSo sánh password",100,550,220,50,"L1"))
    c.append(dec("d2","Password\nđúng?",110,630,120,70,"L1"))
    c.append(act("a7","Trả lỗi:\nInvalid password",100,750,220,40,"L1"))
    c.append(act("a8","Tạo JWT Token",100,830,220,40,"L1"))
    c.append(act("a9","Cập nhật lastLogin\nTrả về { jwt, user }",100,900,220,50,"L1"))
    # Lane 0 - routing
    c.append(dec("d3","Xác định\nRole?",90,960,120,70,"L0"))
    c.append(act("a10","Điều hướng theo role:\nAdmin / Store / Branch / Cashier",30,1060,240,50,"L0"))
    c.append(end("end",135,1140,"L0"))
    # Edges
    c.append(e("e1","s","a1"))
    c.append(e("e2","a1","a2"))
    c.append(e("e3","a2","a3"))
    c.append(e("e4","a3","a4"))
    c.append(e("e5","a4","d1"))
    c.append(e("e6","d1","a5","Không"))
    c.append(e("e7","d1","a6","Có"))
    c.append(e("e8","a6","d2"))
    c.append(e("e9","d2","a7","Sai"))
    c.append(e("e10","d2","a8","Đúng"))
    c.append(e("e11","a8","a9"))
    c.append(e("e12","a9","d3"))
    c.append(e("e13","d3","a10"))
    c.append(e("e14","a10","endo"))
    c.append(e("e15","a5","endo"))
    c.append(e("e16","a7","endo"))
    return wrap("act02","Đăng nhập",c,"800","1300")

# ============================================================
# ACT03: Quên/Đặt lại mật khẩu
# Lanes: Người dùng | Hệ thống | Email Server
# ============================================================
def act03():
    c = []
    c.append(n("t","Biểu đồ hoạt động: Quên / Đặt lại mật khẩu",TITLE,20,10,900,30))
    c.append(n("L0","Người dùng",LANE,20,50,280,1200))
    c.append(n("L1","Hệ thống",LANE,300,50,350,1200))
    c.append(n("L2","Email Server",LANE,650,50,250,1200))
    c.append(start("s",125,50,"L0"))
    c.append(act("a1","Chọn Quên mật khẩu",40,110,200,40,"L0"))
    c.append(act("a2","Nhập email",40,180,200,40,"L0"))
    c.append(act("a3","POST /auth/forgot-password",70,180,220,40,"L1"))
    c.append(act("a4","Tìm User theo email\ntrong Database",70,260,220,40,"L1"))
    c.append(dec("d1","Email\ntồn tại?",100,330,120,70,"L1"))
    c.append(act("a5","Trả lỗi:\nUser not found",70,450,220,40,"L1"))
    c.append(act("a6","Tạo UUID token\n(hết hạn 5 phút)",70,540,220,50,"L1"))
    c.append(act("a7","Lưu token vào bảng\npassword_reset_tokens",70,620,220,50,"L1"))
    c.append(act("a8","Gọi Gmail SMTP\ngửi email chứa link reset",70,700,220,50,"L1"))
    c.append(act("a9","Gửi email\nđến người dùng",30,700,200,50,"L2"))
    c.append(act("a10","Nhận email\nClick link reset password",40,790,200,50,"L0"))
    c.append(act("a11","Nhập password mới",40,870,200,40,"L0"))
    c.append(act("a12","POST /auth/reset-password\n{token, newPassword}",70,870,220,50,"L1"))
    c.append(dec("d2","Token còn\nhiệu lực?",100,950,120,70,"L1"))
    c.append(act("a13","Trả lỗi: Token expired\nXóa token",70,1060,220,50,"L1"))
    c.append(act("a14","BCrypt encode password mới\nCập nhật user, xóa token",70,1140,220,50,"L1"))
    c.append(act("a15","Thông báo\nđổi mật khẩu thành công",40,1140,200,50,"L0"))
    c.append(end("end",125,1220,"L0"))
    c.append(e("e1","s","a1"))
    c.append(e("e2","a1","a2"))
    c.append(e("e3","a2","a3"))
    c.append(e("e4","a3","a4"))
    c.append(e("e5","a4","d1"))
    c.append(e("e6","d1","a5","Không"))
    c.append(e("e7","d1","a6","Có"))
    c.append(e("e8","a6","a7"))
    c.append(e("e9","a7","a8"))
    c.append(e("e10","a8","a9"))
    c.append(e("e11","a9","a10"))
    c.append(e("e12","a10","a11"))
    c.append(e("e13","a11","a12"))
    c.append(e("e14","a12","d2"))
    c.append(e("e15","d2","a13","Hết hạn"))
    c.append(e("e16","d2","a14","Còn"))
    c.append(e("e17","a14","a15"))
    c.append(e("e18","a15","endo"))
    c.append(e("e19","a5","endo"))
    c.append(e("e20","a13","endo"))
    return wrap("act03","Quên mật khẩu",c,"950","1350")

# ============================================================
# ACT04: Tạo cửa hàng & Duyệt
# Lanes: Store Admin | Hệ thống | Super Admin
# ============================================================
def act04():
    c = []
    c.append(n("t","Biểu đồ hoạt động: Tạo cửa hàng và Duyệt",TITLE,20,10,900,30))
    c.append(n("L0","Store Admin",LANE,20,50,280,1100))
    c.append(n("L1","Hệ thống",LANE,300,50,350,1100))
    c.append(n("L2","Super Admin",LANE,650,50,250,1100))
    c.append(start("s",125,50,"L0"))
    c.append(act("a1","Đăng nhập hệ thống",40,110,200,40,"L0"))
    c.append(act("a2","Nhập thông tin cửa hàng:\nbrand, description,\nstoreType, contact",30,180,230,60,"L0"))
    c.append(act("a3","POST /api/stores\nGửi dữ liệu tạo Store",70,180,220,50,"L1"))
    c.append(act("a4","Lấy currentUser từ JWT\nTạo Store(storeAdmin=user)",70,270,220,50,"L1"))
    c.append(act("a5","Set status = PENDING\nLưu vào Database",70,350,220,50,"L1"))
    c.append(act("a6","Trả về Store (PENDING)\nChờ Super Admin duyệt",70,430,220,50,"L1"))
    c.append(act("a7","Hiển thị thông báo:\nCửa hàng đang chờ duyệt",40,500,200,50,"L0"))
    c.append(act("a8","Đăng nhập hệ thống\nXem DS Store PENDING",30,580,200,50,"L2"))
    c.append(act("a9","Chọn Store cần duyệt",30,660,200,40,"L2"))
    c.append(dec("d1","Quyết định\nduyệt?",60,730,120,70,"L2"))
    c.append(act("a10","PUT /stores/{id}/moderate\naction=APPROVE\nstatus → ACTIVE",70,830,220,60,"L1"))
    c.append(act("a11","PUT /stores/{id}/moderate\naction=BLOCK\nstatus → BLOCKED",70,920,220,60,"L1"))
    c.append(act("a12","Store hoạt động\nCó thể tạo Branch, Product",40,920,200,50,"L0"))
    c.append(end("end",125,1010,"L0"))
    c.append(e("e1","s","a1"))
    c.append(e("e2","a1","a2"))
    c.append(e("e3","a2","a3"))
    c.append(e("e4","a3","a4"))
    c.append(e("e5","a4","a5"))
    c.append(e("e6","a5","a6"))
    c.append(e("e7","a6","a7"))
    c.append(e("e8","a7","a8"))
    c.append(e("e9","a8","a9"))
    c.append(e("e10","a9","d1"))
    c.append(e("e11","d1","a10","Duyệt"))
    c.append(e("e12","d1","a11","Từ chối"))
    c.append(e("e13","a10","a12"))
    c.append(e("e14","a12","endo"))
    c.append(e("e15","a11","endo"))
    return wrap("act04","Tạo cửa hàng",c,"950","1250")

for fname, content in [
    ("ACT01_DangKy.drawio", act01()),
    ("ACT02_DangNhap.drawio", act02()),
    ("ACT03_QuenMatKhau.drawio", act03()),
    ("ACT04_TaoCuaHang_Duyet.drawio", act04()),
]:
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(content)
    print(f"✓ {fname}")
print("Done! 4 diagrams generated.")
