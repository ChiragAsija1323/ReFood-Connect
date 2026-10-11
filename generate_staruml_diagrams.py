import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    try:
        font_name = 'arialbd.ttf' if bold else 'arial.ttf'
        return ImageFont.truetype(font_name, size)
    except:
        return ImageFont.load_default()

# Colors mimicking classic StarUML / Rational Rose
# Canvas: White
# Boxes / Shapes: Very pale yellow / cream (#FFFFE0 or #FEFDE8), borders clean black or dark grey (#000000)
# Text: Pure black (#000000)
# Lines: Black (#000000)

FILL_COLOR = '#FFFFCC'  # classic StarUML element fill
LINE_COLOR = '#000000'  # crisp black border
TEXT_COLOR = '#000000'

def draw_arrow(draw, p1, p2, label='', dashed=False):
    x1, y1 = p1
    x2, y2 = p2
    draw.line([p1, p2], fill=LINE_COLOR, width=1)
    # arrowhead
    if x2 > x1:
        draw.polygon([(x2, y2), (x2-8, y2-4), (x2-8, y2+4)], fill=LINE_COLOR)
    elif x2 < x1:
        draw.polygon([(x2, y2), (x2+8, y2-4), (x2+8, y2+4)], fill=LINE_COLOR)
    elif y2 > y1:
        draw.polygon([(x2, y2), (x2-4, y2-8), (x2+4, y2-8)], fill=LINE_COLOR)
    elif y2 < y1:
        draw.polygon([(x2, y2), (x2-4, y2+8), (x2+4, y2+8)], fill=LINE_COLOR)
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - 12
        draw.text((mx - 20, my), label, fill=TEXT_COLOR, font=get_font(10))

# 1. StarUML Class Diagram
def render_staruml_class():
    img = Image.new('RGB', (950, 520), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font = get_font(14, True)
    class_font = get_font(11, True)
    text_font = get_font(10)
    
    draw.text((20, 15), 'Class Diagram: ReFood Connect Architecture (StarUML)', fill=TEXT_COLOR, font=title_font)
    draw.line([(20, 35), (930, 35)], fill='#888888', width=1)
    
    def draw_uml_box(x, y, w, h, name, stereotype, attrs, methods):
        draw.rectangle([x, y, x + w, y + h], fill=FILL_COLOR, outline=LINE_COLOR, width=1)
        # Header section
        header_h = 32 if stereotype else 24
        draw.line([(x, y + header_h), (x + w, y + header_h)], fill=LINE_COLOR, width=1)
        if stereotype:
            draw.text((x + 10, y + 4), stereotype, fill='#444444', font=get_font(9))
            draw.text((x + 10, y + 16), name, fill=TEXT_COLOR, font=class_font)
        else:
            draw.text((x + 10, y + 6), name, fill=TEXT_COLOR, font=class_font)
            
        # Attrs section
        curr_y = y + header_h + 6
        for a in attrs:
            draw.text((x + 8, curr_y), a, fill=TEXT_COLOR, font=text_font)
            curr_y += 15
            
        # Divider
        draw.line([(x, curr_y + 4), (x + w, curr_y + 4)], fill=LINE_COLOR, width=1)
        curr_y += 10
        # Methods
        for m in methods:
            draw.text((x + 8, curr_y), m, fill=TEXT_COLOR, font=text_font)
            curr_y += 15
            
    # Controllers
    draw_uml_box(30, 60, 260, 160, 'AuthController', '<<controller>>',
                 ['- authService: AuthService'],
                 ['+ register(req, res): Promise', '+ login(req, res): Promise'])
                 
    draw_uml_box(340, 60, 270, 160, 'DonationController', '<<controller>>',
                 ['- donationService: DonationService'],
                 ['+ createDonation(req, res)', '+ getDonations(req, res)', '+ updateStatus(req, res)'])
                 
    draw_uml_box(660, 60, 260, 160, 'AdminController', '<<controller>>',
                 ['- adminService: AdminService'],
                 ['+ getDashboardStats(req, res)', '+ listUsers(req, res)'])
                 
    # Services
    draw_uml_box(30, 290, 260, 170, 'AuthService', '<<service>>',
                 ['- User: Model', '- jwtSecret: String'],
                 ['+ register(name, email, pwd)', '+ login(email, pwd): Token', '+ hashPassword(pwd)'])
                 
    draw_uml_box(340, 290, 270, 170, 'DonationService', '<<service>>',
                 ['- Donation: Model', '- User: Model'],
                 ['+ createDonation(data)', '+ getByRole(user)', '+ updateStatus(id, state, user)'])
                 
    draw_uml_box(660, 290, 260, 170, 'AdminService', '<<service>>',
                 ['- Donation: Model', '- User: Model'],
                 ['+ getAggregatedStats()', '+ getSystemAuditTrail()'])
                 
    # Association lines with open arrows / dependency
    draw_arrow(draw, (160, 220), (160, 290), 'uses')
    draw_arrow(draw, (475, 220), (475, 290), 'uses')
    draw_arrow(draw, (790, 220), (790, 290), 'uses')
    
    img.save('design/diagram_renders/class_diagram.png')

# 2. StarUML Use Case Diagram
def render_staruml_usecase():
    img = Image.new('RGB', (950, 540), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font = get_font(14, True)
    actor_font = get_font(11, True)
    uc_font = get_font(10)
    
    draw.text((20, 15), 'Use Case Diagram: ReFood Connect (StarUML)', fill=TEXT_COLOR, font=title_font)
    draw.line([(20, 35), (930, 35)], fill='#888888', width=1)
    
    # System boundary box (plain white with black border)
    draw.rectangle([250, 60, 720, 510], fill='#FFFFFF', outline=LINE_COLOR, width=1)
    draw.text((410, 70), 'ReFood Connect System', fill=TEXT_COLOR, font=get_font(12, True))
    
    use_cases = [
        ('Register & Login (JWT)', 110),
        ('Create Food Surplus Listing', 170),
        ('Browse Available Food', 230),
        ('Request Food Allocation', 290),
        ('Accept Delivery Task', 350),
        ('Update Status (Picked Up / Delivered)', 410),
        ('View Admin Governance Dashboard', 470)
    ]
    for name, y in use_cases:
        draw.ellipse([300, y, 670, y + 36], fill=FILL_COLOR, outline=LINE_COLOR, width=1)
        draw.text((370, y + 11), name, fill=TEXT_COLOR, font=uc_font)
        
    def draw_stick_actor(x, y, name):
        draw.ellipse([x - 10, y, x + 10, y + 20], fill=FILL_COLOR, outline=LINE_COLOR, width=1)
        draw.line([(x, y + 20), (x, y + 48)], fill=LINE_COLOR, width=1) # torso
        draw.line([(x - 15, y + 32), (x + 15, y + 32)], fill=LINE_COLOR, width=1) # arms
        draw.line([(x, y + 48), (x - 12, y + 72)], fill=LINE_COLOR, width=1) # leg left
        draw.line([(x, y + 48), (x + 12, y + 72)], fill=LINE_COLOR, width=1) # leg right
        draw.text((x - 25, y + 78), name, fill=TEXT_COLOR, font=actor_font)
        
    draw_stick_actor(100, 110, 'Food Donor')
    draw_stick_actor(100, 290, 'NGO Recipient')
    draw_stick_actor(840, 150, 'Volunteer')
    draw_stick_actor(840, 380, 'Administrator')
    
    # Association straight lines
    draw.line([(150, 150), (300, 128)], fill=LINE_COLOR, width=1)
    draw.line([(150, 150), (300, 188)], fill=LINE_COLOR, width=1)
    draw.line([(150, 330), (300, 248)], fill=LINE_COLOR, width=1)
    draw.line([(150, 330), (300, 308)], fill=LINE_COLOR, width=1)
    draw.line([(800, 190), (670, 368)], fill=LINE_COLOR, width=1)
    draw.line([(800, 190), (670, 428)], fill=LINE_COLOR, width=1)
    draw.line([(800, 420), (670, 488)], fill=LINE_COLOR, width=1)
    
    img.save('design/diagram_renders/use_case_diagram.png')

# 3. StarUML Sequence Diagram
def render_staruml_sequence():
    img = Image.new('RGB', (950, 520), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font = get_font(14, True)
    header_font = get_font(11, True)
    msg_font = get_font(10)
    
    draw.text((20, 15), 'Sequence Diagram: Donation Lifecycle (StarUML)', fill=TEXT_COLOR, font=title_font)
    draw.line([(20, 35), (930, 35)], fill='#888888', width=1)
    
    lifelines = [
        ('Donor : Actor', 80),
        ('NGO : Actor', 250),
        ('Volunteer : Actor', 430),
        (': Server API', 620),
        (': Database', 820)
    ]
    for name, x in lifelines:
        draw.rectangle([x - 50, 60, x + 50, 88], fill=FILL_COLOR, outline=LINE_COLOR, width=1)
        draw.text((x - 38, 68), name, fill=TEXT_COLOR, font=header_font)
        # dashed lifeline
        for ly in range(95, 480, 10):
            draw.line([(x, ly), (x, ly + 5)], fill='#666666', width=1)
            
    messages = [
        (80, 620, 120, '1: createDonation(details, qty, expiry)'),
        (620, 820, 150, '2: save (status: Available)'),
        (250, 620, 200, '3: requestDonation(id)'),
        (620, 820, 230, '4: update (status: Requested, ngoId)'),
        (430, 620, 280, '5: acceptPickup(id)'),
        (620, 820, 310, '6: update (status: Accepted, volId)'),
        (430, 620, 360, '7: markPickedUp(id)'),
        (620, 820, 390, '8: update (status: Picked Up)'),
        (430, 620, 440, '9: markDelivered(id)'),
        (620, 820, 470, '10: update (status: Delivered)')
    ]
    for x1, x2, y, txt in messages:
        draw.line([(x1, y), (x2, y)], fill=LINE_COLOR, width=1)
        draw.polygon([(x2, y), (x2-6, y-3), (x2-6, y+3)], fill=LINE_COLOR)
        draw.text(((x1 + x2)/2 - 90, y - 12), txt, fill=TEXT_COLOR, font=msg_font)
        
    img.save('design/diagram_renders/sequence_diagram.png')

# 4. StarUML Entity-Relationship Diagram (ERD)
def render_staruml_erd():
    img = Image.new('RGB', (950, 500), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font = get_font(14, True)
    entity_font = get_font(11, True)
    text_font = get_font(10)
    
    draw.text((20, 15), 'Entity-Relationship Diagram: ReFood Connect Database (StarUML)', fill=TEXT_COLOR, font=title_font)
    draw.line([(20, 35), (930, 35)], fill='#888888', width=1)
    
    # Entity: USERS
    draw.rectangle([80, 80, 380, 390], fill=FILL_COLOR, outline=LINE_COLOR, width=1)
    draw.rectangle([80, 80, 380, 110], fill='#E6E6A8', outline=LINE_COLOR, width=1)
    draw.text((180, 88), 'USERS', fill=TEXT_COLOR, font=entity_font)
    
    u_fields = [
        ('PK  id', 'INT (Auto-Increment)'),
        ('    name', 'VARCHAR(255)'),
        ('    email', 'VARCHAR(255) UNIQUE'),
        ('    password', 'VARCHAR(255)'),
        ('    role', 'ENUM(donor, ngo, volunteer, admin)'),
        ('    createdAt', 'DATETIME'),
        ('    updatedAt', 'DATETIME')
    ]
    for i, (f, t) in enumerate(u_fields):
        y = 125 + i * 36
        draw.text((95, y), f, fill=TEXT_COLOR, font=get_font(10, True if 'PK' in f else False))
        draw.text((200, y), t, fill='#555555', font=text_font)
        draw.line([(80, y + 25), (380, y + 25)], fill='#E0E0C0', width=1)
        
    # Entity: DONATIONS
    draw.rectangle([560, 80, 890, 450], fill=FILL_COLOR, outline=LINE_COLOR, width=1)
    draw.rectangle([560, 80, 890, 110], fill='#E6E6A8', outline=LINE_COLOR, width=1)
    draw.text((670, 88), 'DONATIONS', fill=TEXT_COLOR, font=entity_font)
    
    d_fields = [
        ('PK  id', 'INT (Auto-Increment)'),
        ('FK  donorId', 'INT (Users.id)'),
        ('FK  ngoId', 'INT (Nullable, Users.id)'),
        ('FK  volunteerId', 'INT (Nullable, Users.id)'),
        ('    foodDetails', 'VARCHAR(255)'),
        ('    quantity', 'VARCHAR(255)'),
        ('    expiryTime', 'DATETIME'),
        ('    status', 'ENUM(...)'),
        ('    createdAt', 'DATETIME'),
        ('    updatedAt', 'DATETIME')
    ]
    for i, (f, t) in enumerate(d_fields):
        y = 120 + i * 32
        draw.text((575, y), f, fill=TEXT_COLOR, font=get_font(10, True if 'PK' in f or 'FK' in f else False))
        draw.text((680, y), t, fill='#555555', font=text_font)
        draw.line([(560, y + 22), (890, y + 22)], fill='#E0E0C0', width=1)
        
    # Crow's Foot / ER Relationship Line
    draw.line([(380, 220), (560, 220)], fill=LINE_COLOR, width=1)
    # '1' side indicator
    draw.line([(400, 212), (400, 228)], fill=LINE_COLOR, width=1)
    draw.text((390, 198), '1', fill=TEXT_COLOR, font=entity_font)
    # 'N' side crow foot
    draw.line([(545, 212), (560, 220)], fill=LINE_COLOR, width=1)
    draw.line([(545, 228), (560, 220)], fill=LINE_COLOR, width=1)
    draw.text((535, 198), 'N', fill=TEXT_COLOR, font=entity_font)
    draw.text((440, 202), 'creates / claims', fill='#444444', font=text_font)
    
    img.save('design/diagram_renders/erd_diagram.png')

# 5. StarUML / Classic DFD
def render_staruml_dfd():
    img = Image.new('RGB', (950, 480), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font = get_font(14, True)
    elem_font = get_font(11, True)
    text_font = get_font(10)
    
    draw.text((20, 15), 'Data Flow Diagram (DFD Level 1): ReFood Connect (StarUML)', fill=TEXT_COLOR, font=title_font)
    draw.line([(20, 35), (930, 35)], fill='#888888', width=1)
    
    # External entities (simple rectangles)
    entities = [
        ('Donor', (40, 80)),
        ('NGO', (40, 220)),
        ('Volunteer', (40, 360)),
        ('Administrator', (780, 220))
    ]
    for name, (x, y) in entities:
        draw.rectangle([x, y, x + 120, y + 50], fill='#F0F0F0', outline=LINE_COLOR, width=1)
        draw.text((x + 25, y + 17), name, fill=TEXT_COLOR, font=elem_font)
        
    # Processes (Circles / Rounded Rects in StarUML)
    processes = [
        ('1.0 - User Auth', (240, 80)),
        ('2.0 - Post Surplus', (240, 220)),
        ('3.0 - Food Claim', (500, 220)),
        ('4.0 - Transit Logistics', (500, 360)),
        ('5.0 - Admin Audits', (760, 80))
    ]
    for txt, (x, y) in processes:
        draw.rounded_rectangle([x, y, x + 130, y + 55], radius=15, fill=FILL_COLOR, outline=LINE_COLOR, width=1)
        draw.text((x + 12, y + 20), txt, fill=TEXT_COLOR, font=elem_font)
        
    # Data store
    draw.line([(480, 85), (640, 85)], fill=LINE_COLOR, width=1)
    draw.line([(480, 125), (640, 125)], fill=LINE_COLOR, width=1)
    draw.text((500, 98), 'D1 | MySQL Database', fill=TEXT_COLOR, font=text_font)
    
    draw_arrow(draw, (160, 105), (240, 105), 'credentials')
    draw_arrow(draw, (160, 245), (240, 245), 'food details')
    draw_arrow(draw, (370, 245), (500, 245), 'available listing')
    draw_arrow(draw, (160, 385), (500, 385), 'accept task')
    draw_arrow(draw, (565, 360), (565, 275), 'delivered')
    draw_arrow(draw, (630, 245), (780, 245), 'audit log')
    draw_arrow(draw, (825, 135), (825, 220), 'metrics')
    
    img.save('design/diagram_renders/dfd_diagram.png')

render_staruml_class()
render_staruml_usecase()
render_staruml_sequence()
render_staruml_erd()
render_staruml_dfd()
print('All 5 StarUML styled diagrams rendered cleanly!')
