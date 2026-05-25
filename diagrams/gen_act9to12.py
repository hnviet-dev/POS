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

def act09():
    c=[]
    c+=[nd("t","Biểu đồ hoạt động: Hoàn trả đơn hàng",TT,20,10,700,30)]
    c+=[nd("L0","Cashier",LN,20,50,300,1100)]
    c+=[nd("L1","Hệ thống",LN,320,50,380,1100)]
    c+=[nd("s","",ST,135,50,30,30,"L0")]
    c+=[nd("a1","Chọn Hoàn trả đơn hàng",A,50,110,200,40,"L0")]
    c+=[nd("a2","Tải DS đơn hàng\ncủa chi nhánh",A,90,110,220,50,"L1")]
    c+=[nd("a3","Hiển thị đơn hàng\ncó status = COMPLETED",A,90,190,220,50,"L1")]
    c+=[nd("a4","Chọn đơn hàng\ncần hoàn trả",A,50,280,200,50,"L0")]
    c+=[nd("a5","Nhập lý do hoàn trả",A,50,360,200,40,"L0")]
    c+=[nd("a6","POST /api/refunds\nGửi yêu cầu hoàn trả",A,90,370,220,50,"L1")]
    c+=[nd("d1","Order hợp\nlệ?",DC,120,450,120,70,"L1")]
    c+=[nd("a7","Trả lỗi:\nĐơn không tồn tại\nhoặc đã hoàn trả",A,90,560,220,60,"L1")]
    c+=[nd("a8","Tạo Refund mới\n(order, reason, amount,\npaymentType, cashier, branch)",A,90,660,220,70,"L1")]
    c+=[nd("a9","Cập nhật Order\nstatus = REFUNDED",A,90,760,220,50,"L1")]
    c+=[nd("a10","Lưu Refund + cập nhật\nOrder vào Database",A,90,840,220,50,"L1")]
    c+=[nd("a11","Thông báo\nhoàn trả thành công",A,50,930,200,50,"L0")]
    c+=[nd("eo","",EO,135,1010,30,30,"L0")]
    c+=[nd("ei","",EI,142,1017,16,16,"L0")]
    for s,t,lb in [("s","a1",""),("a1","a2",""),("a2","a3",""),("a3","a4",""),("a4","a5",""),("a5","a6",""),("a6","d1",""),("d1","a7","Không"),("d1","a8","Có"),("a8","a9",""),("a9","a10",""),("a10","a11",""),("a11","eo",""),("a7","eo","")]:
        c+=[ed(f"e_{s}_{t}",s,t,lb)]
    return wr("act09","Hoàn trả",c,"750","1200")

def act10():
    c=[]
    c+=[nd("t","Biểu đồ hoạt động: Kết thúc ca làm việc",TT,20,10,700,30)]
    c+=[nd("L0","Cashier",LN,20,50,300,1100)]
    c+=[nd("L1","Hệ thống",LN,320,50,380,1100)]
    c+=[nd("s","",ST,135,50,30,30,"L0")]
    c+=[nd("a1","Nhấn Kết thúc ca",A,50,110,200,40,"L0")]
    c+=[nd("a2","PUT /api/shifts/{id}/close\nSet shiftEnd = now()",A,90,110,220,50,"L1")]
    c+=[nd("a3","Query tất cả Orders\ntrong khoảng shiftStart-shiftEnd",A,90,190,220,50,"L1")]
    c+=[nd("a4","Query tất cả Refunds\ntrong khoảng shiftStart-shiftEnd",A,90,270,220,50,"L1")]
    c+=[nd("a5","Tính toán:\ntotalSales = SUM(orders)\ntotalRefunds = SUM(refunds)\nnetSales = totalSales - totalRefunds\ntotalOrders = COUNT(orders)",A,80,350,240,90,"L1")]
    c+=[nd("a6","Tính PaymentSummary:\nNhóm theo CASH/CARD/UPI\nTính % từng loại",A,90,470,220,60,"L1")]
    c+=[nd("a7","Tính Top 5 sản phẩm\nbán chạy nhất trong ca",A,90,560,220,50,"L1")]
    c+=[nd("a8","Lưu ShiftReport\nvào Database",A,90,640,220,50,"L1")]
    c+=[nd("a9","Trả về báo cáo ca",A,90,720,220,40,"L1")]
    c+=[nd("a10","Hiển thị tổng kết ca:\n- Tổng doanh thu\n- Tổng hoàn trả\n- Doanh thu thuần\n- Top 5 SP bán chạy",A,40,810,230,80,"L0")]
    c+=[nd("eo","",EO,135,920,30,30,"L0")]
    c+=[nd("ei","",EI,142,927,16,16,"L0")]
    for s,t,lb in [("s","a1",""),("a1","a2",""),("a2","a3",""),("a3","a4",""),("a4","a5",""),("a5","a6",""),("a6","a7",""),("a7","a8",""),("a8","a9",""),("a9","a10",""),("a10","eo","")]:
        c+=[ed(f"e_{s}_{t}",s,t,lb)]
    return wr("act10","Kết thúc ca",c,"750","1100")

def act11():
    c=[]
    c+=[nd("t","Biểu đồ hoạt động: Đăng ký Subscription",TT,20,10,900,30)]
    c+=[nd("L0","Store Admin",LN,20,50,280,1250)]
    c+=[nd("L1","Hệ thống",LN,300,50,350,1250)]
    c+=[nd("L2","Razorpay",LN,650,50,250,1250)]
    c+=[nd("s","",ST,125,50,30,30,"L0")]
    c+=[nd("a1","Chọn Nâng cấp gói",40,110,200,40,"L0")]
    c+=[nd("a2","Tải DS SubscriptionPlan",A,70,110,220,40,"L1")]
    c+=[nd("a3","Hiển thị các gói:\nBASIC, PRO, ENTERPRISE",A,70,180,220,50,"L1")]
    c+=[nd("a4","Chọn gói\nvà nhấn Đăng ký",A,40,270,200,50,"L0")]
    c+=[nd("a5","POST /api/subscriptions\nTạo Subscription(PENDING)",A,70,270,220,50,"L1")]
    c+=[nd("a6","Tạo PaymentLink\nqua Razorpay API",A,70,350,220,50,"L1")]
    c+=[nd("a7","Trả về paymentLinkUrl",A,70,430,220,40,"L1")]
    c+=[nd("a8","Redirect đến trang\nthanh toán Razorpay",A,40,510,200,50,"L0")]
    c+=[nd("a9","Hiển thị form\nthanh toán",A,30,510,200,50,"L2")]
    c+=[nd("a10","Nhập thông tin\nthanh toán",A,40,600,200,50,"L0")]
    c+=[nd("a11","Xử lý giao dịch",A,30,600,200,40,"L2")]
    c+=[nd("a12","Callback về hệ thống",A,30,680,200,40,"L2")]
    c+=[nd("a13","Verify payment",A,70,680,220,40,"L1")]
    c+=[nd("d1","Thanh toán\nthành công?",DC,100,760,120,70,"L1")]
    c+=[nd("a14","Cập nhật Subscription:\nstatus = ACTIVE\nstartDate, endDate",A,70,870,220,60,"L1")]
    c+=[nd("a15","Lưu Payment record",A,70,960,220,40,"L1")]
    c+=[nd("a16","Cập nhật Subscription:\nstatus = CANCELLED",A,70,1040,220,50,"L1")]
    c+=[nd("a17","Thông báo\nđăng ký thành công",A,40,1060,200,50,"L0")]
    c+=[nd("eo","",EO,125,1150,30,30,"L0")]
    c+=[nd("ei","",EI,132,1157,16,16,"L0")]
    # Fix: a1 missing style
    c[4] = nd("a1","Chọn Nâng cấp gói",A,40,110,200,40,"L0")
    for s,t,lb in [("s","a1",""),("a1","a2",""),("a2","a3",""),("a3","a4",""),("a4","a5",""),("a5","a6",""),("a6","a7",""),("a7","a8",""),("a8","a9",""),("a9","a10",""),("a10","a11",""),("a11","a12",""),("a12","a13",""),("a13","d1",""),("d1","a14","Có"),("d1","a16","Không"),("a14","a15",""),("a15","a17",""),("a17","eo",""),("a16","eo","")]:
        c+=[ed(f"e_{s}_{t}",s,t,lb)]
    return wr("act11","Subscription",c,"950","1350")

def act12():
    c=[]
    c+=[nd("t","Biểu đồ hoạt động: Xem báo cáo Analytics",TT,20,10,700,30)]
    c+=[nd("L0","Store Admin /\nBranch Manager",LN,20,50,300,950)]
    c+=[nd("L1","Hệ thống",LN,320,50,380,950)]
    c+=[nd("s","",ST,135,50,30,30,"L0")]
    c+=[nd("a1","Chọn Báo cáo",A,50,110,200,40,"L0")]
    c+=[nd("a2","Hiển thị trang báo cáo",A,90,110,220,40,"L1")]
    c+=[nd("a3","Chọn loại báo cáo:\nDoanh thu / SP / Thanh toán",A,50,190,200,50,"L0")]
    c+=[nd("a4","Chọn khoảng thời gian:\nHôm nay / Tuần / Tháng / Năm",A,50,270,200,50,"L0")]
    c+=[nd("a5","GET /api/analytics/...\nGửi request với params",A,90,280,220,50,"L1")]
    c+=[nd("a6","Query Orders + Refunds\ntrong khoảng thời gian",A,90,360,220,50,"L1")]
    c+=[nd("a7","Tính toán aggregate:\n- Tổng doanh thu\n- Nhóm theo ngày/tuần/tháng\n- Top SP bán chạy\n- Phân bổ thanh toán",A,80,440,240,90,"L1")]
    c+=[nd("a8","Trả về dữ liệu\nbáo cáo (JSON)",A,90,560,220,50,"L1")]
    c+=[nd("a9","Vẽ biểu đồ Recharts:\nBarChart, LineChart, PieChart",A,90,640,220,50,"L1")]
    c+=[nd("a10","Xem báo cáo trực quan",A,50,740,200,40,"L0")]
    c+=[nd("eo","",EO,135,810,30,30,"L0")]
    c+=[nd("ei","",EI,142,817,16,16,"L0")]
    for s,t,lb in [("s","a1",""),("a1","a2",""),("a2","a3",""),("a3","a4",""),("a4","a5",""),("a5","a6",""),("a6","a7",""),("a7","a8",""),("a8","a9",""),("a9","a10",""),("a10","eo","")]:
        c+=[ed(f"e_{s}_{t}",s,t,lb)]
    return wr("act12","Báo cáo",c,"750","1050")

for f,content in [("ACT09_HoanTra.drawio",act09()),("ACT10_KetThucCa.drawio",act10()),("ACT11_Subscription.drawio",act11()),("ACT12_BaoCao.drawio",act12())]:
    open(os.path.join(OUT,f),"w").write(content)
    print(f"✓ {f}")
print("Batch 2 done! All 12 complete.")
