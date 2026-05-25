#!/usr/bin/env python3
"""ClassDiagram.drawio - straight lines, no routing, spread layout."""

# Layout: 5 columns, classes spread so lines don't cross boxes
# Col1=30, Col2=380, Col3=760, Col4=1140, Col5=1500
classes = [
    # ROW 1 - Core entities
    ("c1","User",30,30,230,310,
     "- id: Long\n- fullName: String\n- email: String\n- password: String\n- phone: String\n- role: UserRole\n- store: Store\n- branch: Branch\n- verified: Boolean\n- lastLogin: LocalDateTime\n- createdAt: LocalDateTime\n- updatedAt: LocalDateTime",
     "+ login()\n+ register()\n+ resetPassword()\n+ getProfile()"),
    ("c2","Store",380,30,230,280,
     "- id: Long\n- brand: String\n- description: String\n- storeType: String\n- status: StoreStatus\n- contact: StoreContact\n- storeAdmin: User\n- createdAt: LocalDateTime\n- updatedAt: LocalDateTime",
     "+ createStore()\n+ updateStore()\n+ getStoreByUser()\n+ moderateStore()"),
    ("c3","Branch",760,30,240,310,
     "- id: Long\n- name: String\n- address: String\n- phone: String\n- email: String\n- openTime: LocalTime\n- closeTime: LocalTime\n- workingDays: List<String>\n- store: Store\n- manager: User\n- createdAt: LocalDateTime\n- updatedAt: LocalDateTime",
     "+ createBranch()\n+ updateBranch()\n+ deleteBranch()\n+ getBranchesByStore()"),
    ("c4","Product",1140,30,230,310,
     "- id: Long\n- name: String\n- sku: String\n- description: String\n- mrp: Double\n- sellingPrice: Double\n- brand: String\n- image: String\n- category: Category\n- store: Store\n- createdAt: LocalDateTime\n- updatedAt: LocalDateTime",
     "+ createProduct()\n+ updateProduct()\n+ deleteProduct()\n+ getProductsByStore()"),
    ("c5","Category",1500,30,210,180,
     "- id: Long\n- name: String\n- store: Store",
     "+ createCategory()\n+ updateCategory()\n+ deleteCategory()\n+ getCategoriesByStore()"),
    # ROW 1.5 - Small connected to Row 1
    ("c6","StoreContact",380,380,210,100,
     "- address: String\n- phone: String\n- email: String",""),
    # ROW 2 - Operations
    ("c7","Order",30,450,230,280,
     "- id: Long\n- totalAmount: Double\n- paymentType: PaymentType\n- status: OrderStatus\n- branch: Branch\n- cashier: User\n- customer: Customer\n- items: List<OrderItem>\n- createdAt: LocalDateTime",
     "+ createOrder()\n+ getOrders()\n+ getOrdersByBranch()\n+ getOrdersByCashier()"),
    ("c8","OrderItem",380,530,210,170,
     "- id: Long\n- quantity: Integer\n- price: Double\n- product: Product\n- order: Order",
     "+ addOrderItem()\n+ calculateSubtotal()"),
    ("c10","ShiftReport",760,450,250,330,
     "- id: Long\n- shiftStart: LocalDateTime\n- shiftEnd: LocalDateTime\n- totalSales: Double\n- totalRefunds: Double\n- netSales: Double\n- totalOrders: int\n- cashier: User\n- branch: Branch\n- paymentSummaries: List\n- topSellingProducts: List<Product>\n- recentOrders: List<Order>\n- refunds: List<Refund>",
     "+ startShift()\n+ endShift()\n+ getShiftReports()\n+ getShiftReportsByBranch()"),
    ("c12","Inventory",1140,430,230,190,
     "- id: Long\n- branch: Branch\n- product: Product\n- quantity: Integer\n- lastUpdated: LocalDateTime",
     "+ updateInventory()\n+ getInventoryByBranch()\n+ getInventoryByProduct()"),
    # ROW 3 - Secondary
    ("c9","Customer",30,830,220,200,
     "- id: Long\n- fullName: String\n- email: String\n- phone: String\n- createdAt: LocalDateTime\n- updatedAt: LocalDateTime",
     "+ createCustomer()\n+ updateCustomer()\n+ getCustomers()"),
    ("c18","PaymentSummary",380,780,210,130,
     "- type: PaymentType\n- totalAmount: Double\n- transactionCount: int\n- percentage: double",""),
    ("c11","Refund",760,860,240,250,
     "- id: Long\n- order: Order\n- reason: String\n- amount: Double\n- shiftReport: ShiftReport\n- cashier: User\n- branch: Branch\n- paymentType: PaymentType\n- createdAt: LocalDateTime",
     "+ createRefund()\n+ getRefundsByShift()\n+ getRefundsByBranch()"),
    ("c13","Subscription",1140,700,250,270,
     "- id: Long\n- store: Store\n- plan: SubscriptionPlan\n- startDate: LocalDate\n- endDate: LocalDate\n- status: SubscriptionStatus\n- paymentGateway: PaymentGateway\n- transactionId: String\n- paymentStatus: PaymentStatus\n- createdAt: LocalDateTime\n- updatedAt: LocalDateTime",
     "+ subscribe()\n+ upgradeSubscription()\n+ getSubscriptionByStore()"),
    ("c14","SubscriptionPlan",1500,280,260,420,
     "- id: Long\n- name: String\n- description: String\n- price: Double\n- billingCycle: BillingCycle\n- maxBranches: Integer\n- maxUsers: Integer\n- maxProducts: Integer\n- enableAdvancedReports: Boolean\n- enableInventory: Boolean\n- enableIntegrations: Boolean\n- enableEcommerce: Boolean\n- enableInvoiceBranding: Boolean\n- prioritySupport: Boolean\n- enableMultiLocation: Boolean\n- extraFeatures: List<String>\n- createdAt: LocalDateTime\n- updatedAt: LocalDateTime",
     "+ createPlan()\n+ updatePlan()\n+ deletePlan()\n+ getAllPlans()"),
    # ROW 4 - Bottom
    ("c17","PasswordResetToken",30,1110,230,160,
     "- id: Long\n- token: String\n- user: User\n- expiryDate: LocalDateTime",
     "+ createToken()\n+ validateToken()"),
    ("c15","Payment",1140,1040,250,300,
     "- id: Long\n- store: Store\n- subscription: Subscription\n- amount: Double\n- provider: PaymentGateway\n- providerPaymentId: String\n- transactionId: String\n- method: String\n- status: PaymentStatus\n- failureReason: String\n- paidAt: LocalDateTime\n- refundId: String\n- createdAt: Instant\n- updatedAt: Instant",
     "+ processPayment()"),
    ("c16","PaymentOrder",1500,780,240,200,
     "- id: Long\n- amount: Double\n- status: PaymentOrderStatus\n- paymentLinkId: String\n- user: User\n- planId: Long",
     "+ createPaymentLink()\n+ processPaymentOrder()"),
]

enums = [
    ("e1","UserRole",30,1350,190,170,"ROLE_ADMIN\nROLE_STORE_ADMIN\nROLE_STORE_MANAGER\nROLE_BRANCH_MANAGER\nROLE_BRANCH_ADMIN\nROLE_BRANCH_CASHIER\nROLE_CUSTOMER"),
    ("e2","StoreStatus",250,1350,140,100,"PENDING\nACTIVE\nBLOCKED"),
    ("e3","OrderStatus",420,1350,150,100,"COMPLETED\nREFUNDED\nCANCELLED"),
    ("e4","PaymentType",600,1350,140,100,"CASH\nCARD\nUPI"),
    ("e5","SubscriptionStatus",770,1350,170,110,"TRIAL\nACTIVE\nEXPIRED\nCANCELLED"),
    ("e6","BillingCycle",970,1350,140,90,"MONTHLY\nYEARLY"),
    ("e7","PaymentGateway",1140,1350,160,90,"RAZORPAY\nSTRIPE"),
    ("e8","PaymentStatus",1330,1350,150,100,"PENDING\nCOMPLETED\nFAILED"),
    ("e9","PaymentOrderStatus",1510,1350,170,100,"PENDING\nSUCCESS\nFAILED"),
]

# Simple straight lines - NO edgeStyle, NO routing
rels = [
    ("r1","c1","c2","1","1"),       # User-Store
    ("r2","c2","c3","1","N"),       # Store-Branch
    ("r3","c2","c4","1","N"),       # Store-Product
    ("r4","c4","c5","N","1"),       # Product-Category
    ("r5","c2","c6","1","1"),       # Store-StoreContact
    ("r6","c7","c8","1","N"),       # Order-OrderItem
    ("r7","c8","c4","N","1"),       # OrderItem-Product
    ("r8","c3","c7","1","N"),       # Branch-Order
    ("r9","c1","c7","1","N"),       # User(cashier)-Order
    ("r10","c7","c9","N","0..1"),   # Order-Customer
    ("r11","c1","c10","1","N"),     # User-ShiftReport
    ("r12","c3","c10","1","N"),     # Branch-ShiftReport
    ("r13","c10","c11","1","N"),    # ShiftReport-Refund
    ("r14","c7","c11","1","N"),     # Order-Refund
    ("r15","c3","c12","1","N"),     # Branch-Inventory
    ("r16","c4","c12","1","N"),     # Product-Inventory
    ("r17","c2","c13","1","N"),     # Store-Subscription
    ("r18","c14","c13","1","N"),    # SubscriptionPlan-Subscription
    ("r19","c13","c15","1","1"),    # Subscription-Payment
    ("r20","c2","c15","1","N"),     # Store-Payment
    ("r21","c1","c16","1","N"),     # User-PaymentOrder
    ("r22","c1","c17","1","N"),     # User-PasswordResetToken
    ("r23","c10","c18","1","N"),    # ShiftReport-PaymentSummary
    ("r24","c2","c5","1","N"),      # Store-Category
]

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("\n","&#xa;")

o = []
a = o.append
a('<mxfile>')
a('<diagram id="cd" name="Class Diagram">')
a('<mxGraphModel dx="2400" dy="1800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1900" pageHeight="1600" math="0" shadow="0">')
a('<root>')
a('<mxCell id="0"/><mxCell id="1" parent="0"/>')

for cid,name,x,y,w,h,attrs,methods in classes:
    al = attrs.count("\n")+1 if attrs else 0
    ml = methods.count("\n")+1 if methods else 0
    ah = al*16; sy = 26+ah; mh = ml*16 if methods else 0
    h = max(h, sy+8+mh+4 if methods else sy+4)
    a(f'<mxCell id="{cid}" value="{esc(name)}" style="swimlane;fontStyle=1;align=center;startSize=26;html=0;fillColor=#ffffff;strokeColor=#000000;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    a(f'<mxCell id="{cid}a" value="{esc(attrs)}" style="text;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;html=0;fontSize=10;" vertex="1" parent="{cid}"><mxGeometry y="26" width="{w}" height="{ah}" as="geometry"/></mxCell>')
    if methods:
        a(f'<mxCell id="{cid}b" value="" style="line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;spacingLeft=3;spacingRight=10;rotatable=0;labelPosition=left;points=[];portConstraint=eastwest;" vertex="1" parent="{cid}"><mxGeometry y="{sy}" width="{w}" height="8" as="geometry"/></mxCell>')
        a(f'<mxCell id="{cid}c" value="{esc(methods)}" style="text;align=left;verticalAlign=top;spacingLeft=4;spacingRight=4;overflow=hidden;rotatable=0;html=0;fontSize=10;" vertex="1" parent="{cid}"><mxGeometry y="{sy+8}" width="{w}" height="{mh}" as="geometry"/></mxCell>')

for eid,name,x,y,w,h,vals in enums:
    a(f'<mxCell id="{eid}" value="&lt;&lt;enum&gt;&gt;&#xa;{esc(name)}" style="swimlane;fontStyle=1;align=center;startSize=40;html=0;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    vl = vals.count("\n")+1
    a(f'<mxCell id="{eid}a" value="{esc(vals)}" style="text;align=left;verticalAlign=top;spacingLeft=4;html=0;fontSize=9;" vertex="1" parent="{eid}"><mxGeometry y="40" width="{w}" height="{vl*14}" as="geometry"/></mxCell>')

# STRAIGHT LINES ONLY - no edgeStyle, no routing
ST = "endArrow=none;strokeColor=#000000;fontSize=10;"
for rid,src,tgt,sl,tl in rels:
    a(f'<mxCell id="{rid}" value="" style="{ST}" edge="1" source="{src}" target="{tgt}" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>')
    a(f'<mxCell id="{rid}s" value="{sl}" style="edgeLabel;html=0;align=left;verticalAlign=bottom;fontSize=9;" vertex="1" connectable="0" parent="{rid}"><mxGeometry x="-0.8" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry></mxCell>')
    a(f'<mxCell id="{rid}e" value="{tl}" style="edgeLabel;html=0;align=right;verticalAlign=bottom;fontSize=9;" vertex="1" connectable="0" parent="{rid}"><mxGeometry x="0.8" relative="1" as="geometry"><mxPoint as="offset"/></mxGeometry></mxCell>')

a('</root></mxGraphModel></diagram></mxfile>')

with open("/Users/Study/DOAN/z pos-source-code_1/diagrams/ClassDiagram.drawio","w") as f:
    f.write("\n".join(o))
print("Done! Straight lines only, no routing/curves.")
