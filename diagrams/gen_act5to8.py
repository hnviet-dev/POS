#!/usr/bin/env python3
import os
OUT="/Users/Study/DOAN/z pos-source-code_1/diagrams"
def esc(s):return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
A="rounded=1;whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor=#000000;fontSize=11;"
DC="rhombus;whiteSpace=wrap;html=0;fillColor=#ffffff;strokeColor=#000000;fontSize=10;"
ST="ellipse;whiteSpace=wrap;html=0;aspect=fixed;fillColor=#000000;strokeColor=#000000;"
EO="ellipse;whiteSpace=wrap;html=0;aspect=fixed;fillColor=#ffffff;strokeColor=#000000;strokeWidth=2;"
EI="ellipse;whiteSpace=wrap;html=0;aspect=fixed;fillColor=#000000;strokeColor=#000000;"
LN="swimlane;startSize=30;html=0;fillColor=#ffffff;strokeColor=#000000;fontStyle=1;fontSize=12;"
ED="endArrow=open;endSize=8;html=0;strokeColor=#000000;fontSize=9;rounded=0;curved=0;"
TT="text;html=0;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;fontStyle=1;fontSize=14;"
def nd(i,v,s,x,y,w,h,p="1"):return f'<mxCell id="{i}" value="{esc(v)}" style="{s}" vertex="1" parent="{p}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
def ed(i,s,t,lb=""):
    v=f' value="{esc(lb)}"' if lb else ' value=""'
    return f'<mxCell id="{i}"{v} style="{ED}" edge="1" source="{s}" target="{t}" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>'
def wr(did,nm,cells,pw="900",ph="1300"):return f'<mxfile>\n<diagram id="{did}" name="{nm}">\n<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{pw}" pageHeight="{ph}" math="0" shadow="0">\n<root>\n<mxCell id="0"/><mxCell id="1" parent="0"/>\n'+'\n'.join(cells)+'\n</root>\n</mxGraphModel>\n</diagram>\n</mxfile>'

def act05():
    c=[]
    c+=[nd("t","Biểu đồ hoạt động: Quản lý sản phẩm",TT,20,10,700,30)]
    c+=[nd("L0","Store Admin",LN,20,50,300,1100)]
    c+=[nd("L1","Hệ thống",LN,320,50,380,1100)]
    c+=[nd("s","",ST,135,50,30,30,"L0")]
    c+=[nd("a1","Chọn Quản lý sản phẩm",A,50,110,200,40,"L0")]
    c+=[nd("a2","Hiển thị danh sách\nsản phẩm của Store",A,90,110,220,50,"L1")]
    c+=[nd("a3","Chọn Tạo sản phẩm mới",A,50,200,200,40,"L0")]
    c+=[nd("a4","Hiển thị form\ntạo sản phẩm",A,90,200,220,40,"L1")]
    c+=[nd("a5","Nhập thông tin sản phẩm:\nname, sku, mrp, sellingPrice,\nbrand, image, categoryId",A,30,280,240,70,"L0")]
    c+=[nd("a6","POST /api/products",A,90,380,220,40,"L1")]
    c+=[nd("a7","checkAuthority()\nKiểm tra quyền Store Admin",A,90,450,220,50,"L1")]
    c+=[nd("d1","Có quyền?",DC,120,530,120,70,"L1")]
    c+=[nd("a8","Trả lỗi: Unauthorized",A,90,640,220,40,"L1")]
    c+=[nd("a9","Kiểm tra Category\ntồn tại trong Store",A,90,720,220,50,"L1")]
    c+=[nd("d2","Category\nhợp lệ?",DC,120,800,120,70,"L1")]
    c+=[nd("a10","Trả lỗi:\nCategory not found",A,90,910,220,40,"L1")]
    c+=[nd("a11","Tạo Product mới\nLưu vào Database",A,90,980,220,50,"L1")]
    c+=[nd("a12","Thông báo\ntạo SP thành công",A,50,980,200,50,"L0")]
    c+=[nd("eo","",EO,135,1060,30,30,"L0")]
    c+=[nd("ei","",EI,142,1067,16,16,"L0")]
    for s,t,lb in [("s","a1",""),("a1","a2",""),("a2","a3",""),("a3","a4",""),("a4","a5",""),("a5","a6",""),("a6","a7",""),("a7","d1",""),("d1","a8","Không"),("d1","a9","Có"),("a9","d2",""),("d2","a10","Không"),("d2","a11","Có"),("a11","a12",""),("a12","eo",""),("a8","eo",""),("a10","eo","")]:
        c+=[ed(f"e_{s}_{t}",s,t,lb)]
    return wr("act05","Quản lý sản phẩm",c,"750","1200")

def act06():
    c=[]
    c+=[nd("t","Biểu đồ hoạt động: Thêm nhân viên",TT,20,10,700,30)]
    c+=[nd("L0","Store Admin",LN,20,50,300,1000)]
    c+=[nd("L1","Hệ thống",LN,320,50,380,1000)]
    c+=[nd("s","",ST,135,50,30,30,"L0")]
    c+=[nd("a1","Chọn Thêm nhân viên",A,50,110,200,40,"L0")]
    c+=[nd("a2","Hiển thị form\nthêm nhân viên",A,90,110,220,50,"L1")]
    c+=[nd("a3","Nhập thông tin:\nfullName, email, password,\nphone, role, branchId",A,30,200,240,70,"L0")]
    c+=[nd("a4","POST /api/users/add-employee",A,90,300,220,40,"L1")]
    c+=[nd("a5","Kiểm tra email\ntrùng trong Database",A,90,370,220,50,"L1")]
    c+=[nd("d1","Email\ntồn tại?",DC,120,450,120,70,"L1")]
    c+=[nd("a6","Trả lỗi:\nEmail already exists",A,90,560,220,40,"L1")]
    c+=[nd("a7","BCrypt encode password",A,90,640,220,40,"L1")]
    c+=[nd("a8","Tạo User(role, store, branch)\nLưu vào Database",A,90,710,220,50,"L1")]
    c+=[nd("a9","Thông báo thêm\nnhân viên thành công",A,50,800,200,50,"L0")]
    c+=[nd("eo","",EO,135,880,30,30,"L0")]
    c+=[nd("ei","",EI,142,887,16,16,"L0")]
    for s,t,lb in [("s","a1",""),("a1","a2",""),("a2","a3",""),("a3","a4",""),("a4","a5",""),("a5","d1",""),("d1","a6","Có"),("d1","a7","Không"),("a7","a8",""),("a8","a9",""),("a9","eo",""),("a6","eo","")]:
        c+=[ed(f"e_{s}_{t}",s,t,lb)]
    return wr("act06","Thêm nhân viên",c,"750","1100")

def act07():
    c=[]
    c+=[nd("t","Biểu đồ hoạt động: Luồng bán hàng POS",TT,20,10,700,30)]
    c+=[nd("L0","Cashier",LN,20,50,300,1350)]
    c+=[nd("L1","Hệ thống",LN,320,50,380,1350)]
    c+=[nd("s","",ST,135,50,30,30,"L0")]
    c+=[nd("a1","Mở màn hình POS",A,50,110,200,40,"L0")]
    c+=[nd("a2","Tải danh sách sản phẩm\nGET /api/products",A,90,110,220,50,"L1")]
    c+=[nd("a3","Hiển thị danh sách\nSP theo chi nhánh",A,90,190,220,50,"L1")]
    c+=[nd("a4","Tìm kiếm sản phẩm\n(theo tên hoặc mã)",A,50,280,200,50,"L0")]
    c+=[nd("a5","Chọn sản phẩm\nNhập số lượng",A,50,360,200,50,"L0")]
    c+=[nd("a6","Redux: cartSlice.addItem()\nTính subtotal, tax, total",A,90,360,220,50,"L1")]
    c+=[nd("d1","Thêm SP\ntiếp?",DC,90,450,120,70,"L0")]
    c+=[nd("a7","Chọn khách hàng\n(tùy chọn)",A,50,560,200,50,"L0")]
    c+=[nd("a8","Chọn phương thức\nthanh toán: CASH/CARD/UPI",A,50,640,200,50,"L0")]
    c+=[nd("a9","Nhấn Thanh toán",A,50,720,200,40,"L0")]
    c+=[nd("a10","POST /api/orders\nTạo Order + OrderItems",A,90,720,220,50,"L1")]
    c+=[nd("a11","Lấy cashier, branch từ JWT\nSet status = COMPLETED",A,90,800,220,50,"L1")]
    c+=[nd("a12","Lưu Order + OrderItems\nvào Database",A,90,880,220,50,"L1")]
    c+=[nd("a13","Redux: clearCart()\nXóa giỏ hàng",A,90,960,220,40,"L1")]
    c+=[nd("a14","Hiển thị hóa đơn\nthành công",A,50,1040,200,50,"L0")]
    c+=[nd("d2","In hóa đơn?",DC,90,1120,120,70,"L0")]
    c+=[nd("a15","In hóa đơn",A,50,1220,200,40,"L0")]
    c+=[nd("eo","",EO,135,1290,30,30,"L0")]
    c+=[nd("ei","",EI,142,1297,16,16,"L0")]
    for s,t,lb in [("s","a1",""),("a1","a2",""),("a2","a3",""),("a3","a4",""),("a4","a5",""),("a5","a6",""),("a6","d1",""),("d1","a4","Có"),("d1","a7","Không"),("a7","a8",""),("a8","a9",""),("a9","a10",""),("a10","a11",""),("a11","a12",""),("a12","a13",""),("a13","a14",""),("a14","d2",""),("d2","a15","Có"),("d2","eo","Không"),("a15","eo","")]:
        c+=[ed(f"e_{s}_{t}",s,t,lb)]
    return wr("act07","Bán hàng POS",c,"750","1450")

def act08():
    c=[]
    c+=[nd("t","Biểu đồ hoạt động: Tạm giữ và Khôi phục đơn",TT,20,10,700,30)]
    c+=[nd("L0","Cashier",LN,20,50,300,1000)]
    c+=[nd("L1","Hệ thống (Redux)",LN,320,50,380,1000)]
    c+=[nd("s","",ST,135,50,30,30,"L0")]
    c+=[nd("a1","Thêm SP vào giỏ hàng\n(đang phục vụ khách A)",A,50,110,200,50,"L0")]
    c+=[nd("a2","Nhấn nút Tạm giữ\n(Hold Order)",A,50,200,200,50,"L0")]
    c+=[nd("a3","holdCurrentCart():\nLưu giỏ vào holdOrders[]\nTạo giỏ hàng mới (rỗng)",A,80,200,230,60,"L1")]
    c+=[nd("a4","Hiển thị badge\nsố đơn tạm giữ",A,90,300,220,40,"L1")]
    c+=[nd("a5","Phục vụ khách B\n(thêm SP, thanh toán)",A,50,380,200,50,"L0")]
    c+=[nd("a6","Nhấn Đơn tạm giữ\n(Held Orders)",A,50,470,200,50,"L0")]
    c+=[nd("a7","getHoldOrders():\nHiển thị DS đơn tạm giữ",A,90,470,220,50,"L1")]
    c+=[nd("a8","Chọn đơn cần khôi phục",A,50,560,200,40,"L0")]
    c+=[nd("a9","resumeHoldOrder(index):\nLấy đơn từ holdOrders[]\nSet làm giỏ hiện tại",A,80,560,230,60,"L1")]
    c+=[nd("a10","Giỏ hàng khách A\nđược khôi phục",A,50,660,200,50,"L0")]
    c+=[nd("a11","Tiếp tục thanh toán\ncho khách A",A,50,740,200,50,"L0")]
    c+=[nd("eo","",EO,135,830,30,30,"L0")]
    c+=[nd("ei","",EI,142,837,16,16,"L0")]
    for s,t,lb in [("s","a1",""),("a1","a2",""),("a2","a3",""),("a3","a4",""),("a4","a5",""),("a5","a6",""),("a6","a7",""),("a7","a8",""),("a8","a9",""),("a9","a10",""),("a10","a11",""),("a11","eo","")]:
        c+=[ed(f"e_{s}_{t}",s,t,lb)]
    return wr("act08","Tạm giữ đơn",c,"750","1100")

for f,content in [("ACT05_QuanLySanPham.drawio",act05()),("ACT06_ThemNhanVien.drawio",act06()),("ACT07_BanHangPOS.drawio",act07()),("ACT08_TamGiu_KhoiPhuc.drawio",act08())]:
    open(os.path.join(OUT,f),"w").write(content)
    print(f"✓ {f}")
print("Batch 1 done!")
