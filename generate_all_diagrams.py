import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    try:
        font_name = 'arialbd.ttf' if bold else 'arial.ttf'
        return ImageFont.truetype(font_name, size)
    except:
        return ImageFont.load_default()

def draw_arrow(draw, p1, p2, label='', color='#334155'):
    draw.line([p1, p2], fill=color, width=2)
    x1, y1 = p1
    x2, y2 = p2
    if x2 > x1:
        draw.polygon([(x2, y2), (x2-8, y2-5), (x2-8, y2+5)], fill=color)
    elif x2 < x1:
        draw.polygon([(x2, y2), (x2+8, y2-5), (x2+8, y2+5)], fill=color)
    elif y2 > y1:
        draw.polygon([(x2, y2), (x2-5, y2-8), (x2+5, y2-8)], fill=color)
    elif y2 < y1:
        draw.polygon([(x2, y2), (x2-5, y2+8), (x2+5, y2+8)], fill=color)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - 14
        draw.text((mx - 25, my), label, fill='#0369A1', font=get_font(10))

# 1. DFD Diagram
def render_dfd():
    img = Image.new('RGB', (1000, 520), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font = get_font(18, True)
    header_font = get_font(13, True)
    text_font = get_font(11)
    
    draw.text((25, 15), 'Figure B.1: Data Flow Diagram (DFD) - Level 1 Redistribution Lifecycle', fill='#0F172A', font=title_font)
    draw.line([(25, 45), (975, 45)], fill='#CBD5E1', width=2)
    
    entities = [
        ('Donor Entity', (40, 90), '#16A34A'),
        ('NGO Entity', (40, 230), '#2563EB'),
        ('Volunteer Entity', (40, 370), '#D97706'),
        ('Admin Entity', (800, 230), '#7C3AED')
    ]
    for name, (x, y), color in entities:
        draw.rectangle([x, y, x + 140, y + 60], fill=color, outline='#0F172A', width=2)
        draw.text((x + 18, y + 22), name, fill='#FFFFFF', font=header_font)
        
    processes = [
        ('1.0 Auth & Session', (250, 90)),
        ('2.0 Post Food Surplus', (250, 230)),
        ('3.0 Claim & Allocation', (520, 230)),
        ('4.0 Transit & Delivery', (520, 370)),
        ('5.0 System Governance', (780, 90))
    ]
    for text, (x, y) in processes:
        draw.rounded_rectangle([x, y, x + 170, y + 60], radius=12, fill='#F8FAFC', outline='#2563EB', width=2)
        draw.text((x + 14, y + 22), text, fill='#1E293B', font=header_font)
        
    draw.line([(480, 100), (660, 100)], fill='#0F172A', width=2)
    draw.line([(480, 140), (660, 140)], fill='#0F172A', width=2)
    draw.text((500, 114), 'D1: Relational Store (MySQL)', fill='#0F172A', font=text_font)
    
    draw_arrow(draw, (180, 120), (250, 120), 'Credentials')
    draw_arrow(draw, (180, 260), (250, 260), 'Meal Batch')
    draw_arrow(draw, (420, 260), (520, 260), 'Available List')
    draw_arrow(draw, (180, 400), (520, 400), 'Pickup Claim')
    draw_arrow(draw, (605, 370), (605, 290), 'Delivered')
    draw_arrow(draw, (690, 260), (800, 260), 'Audit Trail')
    draw_arrow(draw, (865, 150), (865, 230), 'Realtime Stats')
    
    img.save('design/diagram_renders/dfd_diagram.png')

# 2. ER Diagram
def render_erd():
    img = Image.new('RGB', (1000, 560), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font = get_font(18, True)
    header_font = get_font(13, True)
    text_font = get_font(11)
    
    draw.text((25, 15), 'Figure C.1: Entity-Relationship Diagram (ERD) - Relational Model', fill='#0F172A', font=title_font)
    draw.line([(25, 45), (975, 45)], fill='#CBD5E1', width=2)
    
    # Table USERS
    draw.rectangle([80, 90, 420, 420], fill='#F8FAFC', outline='#0284C7', width=2)
    draw.rectangle([80, 90, 420, 130], fill='#0284C7')
    draw.text((100, 102), 'TABLE: USERS (Sequelize Model)', fill='#FFFFFF', font=header_font)
    
    user_fields = [
        ('PK  id', 'INTEGER (AUTO_INCREMENT)'),
        ('    name', 'VARCHAR(255) NOT NULL'),
        ('    email', 'VARCHAR(255) UNIQUE'),
        ('    password', 'VARCHAR(255) (Bcrypt 10 rounds)'),
        ('    role', 'ENUM(donor, ngo, volunteer, admin)'),
        ('    createdAt', 'DATETIME'),
        ('    updatedAt', 'DATETIME')
    ]
    for i, (col, typ) in enumerate(user_fields):
        y = 150 + i * 36
        draw.text((95, y), col, fill='#0F172A', font=get_font(11, True if 'PK' in col else False))
        draw.text((230, y), typ, fill='#64748B', font=text_font)
        draw.line([(80, y + 25), (420, y + 25)], fill='#E2E8F0', width=1)
        
    # Table DONATIONS
    draw.rectangle([580, 90, 940, 500], fill='#F8FAFC', outline='#16A34A', width=2)
    draw.rectangle([580, 90, 940, 130], fill='#16A34A')
    draw.text((600, 102), 'TABLE: DONATIONS (Sequelize Model)', fill='#FFFFFF', font=header_font)
    
    donation_fields = [
        ('PK  id', 'INTEGER (AUTO_INCREMENT)'),
        ('FK  donorId', 'INTEGER -> Users(id)'),
        ('FK  ngoId', 'INTEGER (Nullable) -> Users(id)'),
        ('FK  volunteerId', 'INTEGER (Nullable) -> Users(id)'),
        ('    foodDetails', 'VARCHAR(255) NOT NULL'),
        ('    quantity', 'VARCHAR(255) NOT NULL'),
        ('    expiryTime', 'DATETIME NOT NULL'),
        ('    status', 'ENUM(Available, Requested, Accepted, ...)'),
        ('    createdAt', 'DATETIME'),
        ('    updatedAt', 'DATETIME')
    ]
    for i, (col, typ) in enumerate(donation_fields):
        y = 145 + i * 34
        draw.text((595, y), col, fill='#0F172A', font=get_font(11, True if 'PK' in col or 'FK' in col else False))
        draw.text((710, y), typ, fill='#64748B', font=text_font)
        draw.line([(580, y + 24), (940, y + 24)], fill='#E2E8F0', width=1)
        
    # Relationship diamond
    draw.polygon([(460, 240), (500, 210), (540, 240), (500, 270)], fill='#FEF3C7', outline='#D97706', width=2)
    draw.text((475, 233), 'Has-Many', fill='#92400E', font=get_font(10, True))
    
    draw.line([(420, 240), (460, 240)], fill='#D97706', width=2)
    draw.line([(540, 240), (580, 240)], fill='#D97706', width=2)
    draw.text((430, 222), '1', fill='#D97706', font=header_font)
    draw.text((565, 222), 'N', fill='#D97706', font=header_font)
    
    img.save('design/diagram_renders/erd_diagram.png')

# 3. UML Use Case Diagram
def render_use_case():
    img = Image.new('RGB', (1000, 560), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font = get_font(18, True)
    header_font = get_font(13, True)
    text_font = get_font(11)
    
    draw.text((25, 15), 'Figure D.1: UML Use Case Diagram - System Actors & Operational Goals', fill='#0F172A', font=title_font)
    draw.line([(25, 45), (975, 45)], fill='#CBD5E1', width=2)
    
    # System boundary box
    draw.rectangle([250, 75, 750, 520], fill='#F8FAFC', outline='#0284C7', width=2)
    draw.text((430, 85), 'System: ReFood Connect', fill='#0369A1', font=header_font)
    
    # Use cases (Ovals)
    use_cases = [
        ('UC-01: Authenticate & Register (JWT)', 120),
        ('UC-02: Publish Surplus Food Batch', 175),
        ('UC-03: Browse & Search Available Listings', 230),
        ('UC-04: Request Food Claim Allocation', 285),
        ('UC-05: Accept Transit Logistics Task', 340),
        ('UC-06: Update Sequential Delivery State', 395),
        ('UC-07: Platform Governance & Real-Time Audits', 450)
    ]
    for text, y in use_cases:
        draw.ellipse([310, y, 690, y + 42], fill='#FFFFFF', outline='#2563EB', width=2)
        draw.text((345, y + 13), text, fill='#1E293B', font=text_font)
        
    # Actors (Left & Right)
    def draw_actor(x, y, name, color='#1E293B'):
        draw.ellipse([x - 12, y, x + 12, y + 24], fill='#FFFFFF', outline=color, width=2)
        draw.line([(x, y + 24), (x, y + 54)], fill=color, width=2) # body
        draw.line([(x - 18, y + 36), (x + 18, y + 36)], fill=color, width=2) # arms
        draw.line([(x, y + 54), (x - 14, y + 78)], fill=color, width=2) # leg
        draw.line([(x, y + 54), (x + 14, y + 78)], fill=color, width=2) # leg
        draw.text((x - 30, y + 84), name, fill=color, font=header_font)
        
    draw_actor(100, 120, 'Food Donor', '#16A34A')
    draw_actor(100, 320, 'NGO Recipient', '#2563EB')
    draw_actor(880, 120, 'Volunteer Runner', '#D97706')
    draw_actor(880, 320, 'Administrator', '#7C3AED')
    
    # Association lines
    draw.line([(150, 160), (310, 140)], fill='#94A3B8', width=1) # Donor -> UC01
    draw.line([(150, 160), (310, 195)], fill='#94A3B8', width=1) # Donor -> UC02
    draw.line([(150, 360), (310, 250)], fill='#94A3B8', width=1) # NGO -> UC03
    draw.line([(150, 360), (310, 305)], fill='#94A3B8', width=1) # NGO -> UC04
    draw.line([(830, 160), (690, 360)], fill='#94A3B8', width=1) # Vol -> UC05
    draw.line([(830, 160), (690, 415)], fill='#94A3B8', width=1) # Vol -> UC06
    draw.line([(830, 360), (690, 470)], fill='#94A3B8', width=1) # Admin -> UC07
    
    img.save('design/diagram_renders/use_case_diagram.png')

# 4. UML Sequence Diagram
def render_sequence():
    img = Image.new('RGB', (1000, 540), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font = get_font(18, True)
    header_font = get_font(12, True)
    text_font = get_font(10)
    
    draw.text((25, 15), 'Figure D.2: UML Sequence Diagram - Sequential Redistribution Lifecycle', fill='#0F172A', font=title_font)
    draw.line([(25, 45), (975, 45)], fill='#CBD5E1', width=2)
    
    lifelines = [
        ('Donor', 100),
        ('NGO', 280),
        ('Volunteer', 460),
        ('API Gateway', 640),
        ('MySQL DB', 840)
    ]
    for name, x in lifelines:
        draw.rectangle([x - 55, 65, x + 55, 100], fill='#0284C7', outline='#0F172A', width=1)
        draw.text((x - 40, 76), name, fill='#FFFFFF', font=header_font)
        draw.line([(x, 100), (x, 500)], fill='#94A3B8', width=1) # lifeline dashed
        
    messages = [
        (100, 640, 130, '1: POST /api/donations (Create Surplus Batch)'),
        (640, 840, 160, '2: INSERT INTO Donations (Status: Available)'),
        (280, 640, 210, '3: PUT /api/donations/:id (NGO Request Claim)'),
        (640, 840, 240, '4: UPDATE Status -> Requested'),
        (460, 640, 290, '5: PUT /api/donations/:id (Volunteer Accept)'),
        (640, 840, 320, '6: UPDATE Status -> Accepted'),
        (460, 640, 370, '7: PUT /api/donations/:id (Mark Picked Up)'),
        (640, 840, 400, '8: UPDATE Status -> Picked Up'),
        (460, 640, 450, '9: PUT /api/donations/:id (Confirm Delivered)'),
        (640, 840, 480, '10: UPDATE Status -> Delivered (Final Log)')
    ]
    for x1, x2, y, txt in messages:
        draw_arrow(draw, (x1, y), (x2, y), '', color='#1E293B')
        draw.text(((x1 + x2)/2 - 110, y - 13), txt, fill='#0369A1', font=text_font)
        
    img.save('design/diagram_renders/sequence_diagram.png')

# 5. UML Class Diagram
def render_class_diagram():
    img = Image.new('RGB', (1000, 520), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font = get_font(18, True)
    header_font = get_font(12, True)
    text_font = get_font(10)
    
    draw.text((25, 15), 'Figure D.3: UML Class Diagram - Layered Architectural Components', fill='#0F172A', font=title_font)
    draw.line([(25, 45), (975, 45)], fill='#CBD5E1', width=2)
    
    def draw_class(x, y, w, h, name, attrs, methods):
        draw.rectangle([x, y, x + w, y + h], fill='#F8FAFC', outline='#0284C7', width=2)
        draw.rectangle([x, y, x + w, y + 28], fill='#0284C7')
        draw.text((x + 10, y + 7), name, fill='#FFFFFF', font=header_font)
        
        curr_y = y + 36
        for attr in attrs:
            draw.text((x + 10, curr_y), attr, fill='#334155', font=text_font)
            curr_y += 18
            
        draw.line([(x, curr_y + 4), (x + w, curr_y + 4)], fill='#CBD5E1', width=1)
        curr_y += 12
        for m in methods:
            draw.text((x + 10, curr_y), m, fill='#0F172A', font=text_font)
            curr_y += 18
            
    # Controllers
    draw_class(40, 80, 260, 160, 'AuthController',
               ['- authService: AuthService'],
               ['+ register(req, res): Promise', '+ login(req, res): Promise'])
               
    draw_class(360, 80, 280, 160, 'DonationController',
               ['- donationService: DonationService'],
               ['+ createDonation(req, res)', '+ getDonations(req, res)', '+ updateStatus(req, res)'])
               
    draw_class(690, 80, 270, 160, 'AdminController',
               ['- adminService: AdminService'],
               ['+ getDashboardStats(req, res)', '+ listUsers(req, res)'])
               
    # Services
    draw_class(40, 300, 260, 170, 'AuthService',
               ['- User: Model', '- jwtSecret: string'],
               ['+ register(name, email, pwd)', '+ login(email, pwd): Token', '+ hashPassword(pwd)'])
               
    draw_class(360, 300, 280, 170, 'DonationService',
               ['- Donation: Model', '- User: Model'],
               ['+ createDonation(data)', '+ getByRole(user)', '+ updateStatus(id, state, user)'])
               
    draw_class(690, 300, 270, 170, 'AdminService',
               ['- Donation: Model', '- User: Model'],
               ['+ getAggregatedStats()', '+ getSystemAuditTrail()'])
               
    # Dependencies
    draw_arrow(draw, (170, 240), (170, 300), 'delegates to')
    draw_arrow(draw, (500, 240), (500, 300), 'delegates to')
    draw_arrow(draw, (825, 240), (825, 300), 'delegates to')
    
    img.save('design/diagram_renders/class_diagram.png')

render_dfd()
render_erd()
render_use_case()
render_sequence()
render_class_diagram()
print('All 5 diagrams generated successfully!')
