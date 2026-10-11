import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "ReFood Connect — Digital Assignment 3 (DA-3 / Review 3)")
            self.drawRightString(558, 755, "VIT Chennai | BCSE301L")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 747, 558, 747)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.drawString(54, 40, "Confidential & Academic Evaluation Material — ReFood Connect")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 50, 558, 50)
        self.restoreState()

def build_pdf(filename, title, subtitle, story_elements):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    doc.build(story_elements, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")

def get_custom_styles():
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1E293B'),
        spaceAfter=6,
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#16A34A'),
        spaceAfter=15,
        alignment=0
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F8FAFC'),
        borderColor=colors.HexColor('#E2E8F0'),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        'CustomMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#475569')
    )

    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'h1': h1_style,
        'h2': h2_style,
        'body': body_style,
        'code': code_style,
        'meta': meta_style
    }

def generate_evidence_pdf():
    styles = get_custom_styles()
    story = []

    # Title block
    story.append(Paragraph("ReFood Connect — Quality Assurance & Testing Evidence Portfolio", styles['title']))
    story.append(Paragraph("Digital Assignment 3 (Part A Evaluation) | Software Engineering (BCSE301L)", styles['subtitle']))
    
    meta_text = """
    <b>Academic Institution:</b> Vellore Institute of Technology (VIT), Chennai Campus<br/>
    <b>Authors:</b> Chirag Asija (24BDS1073) & Saanvi Gupta (24BDS1023)<br/>
    <b>Official GitHub Repository:</b> https://github.com/ChiragAsija1323/ReFood-Connect<br/>
    <b>Verification Milestone:</b> Review 3 / DA-3 Single Compiled Quality PDF
    """
    story.append(Paragraph(meta_text, styles['meta']))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=12))

    # Section 1: Executive Summary Table
    story.append(Paragraph("1. Quality Verification Executive Summary", styles['h1']))
    summary_data = [
        [Paragraph("<b>Verification Target</b>", styles['body']), Paragraph("<b>Observed Result</b>", styles['body']), Paragraph("<b>Compliance Status</b>", styles['body'])],
        [Paragraph("Integration & Unit Suites", styles['body']), Paragraph("27/27 Tests Passed (100% Pass Rate)", styles['body']), Paragraph("VERIFIED (PASS)", styles['body'])],
        [Paragraph("Test Execution Time", styles['body']), Paragraph("5.32 seconds (In-Memory SQLite Isolation)", styles['body']), Paragraph("OPTIMAL", styles['body'])],
        [Paragraph("Mutation Testing Tool", styles['body']), Paragraph("StrykerJS v8.7 with Jest Runner", styles['body']), Paragraph("VERIFIED", styles['body'])],
        [Paragraph("Baseline Mutation Score", styles['body']), Paragraph("60.31% (79 Killed, 15 Survived, 37 Uncovered)", styles['body']), Paragraph("RECORDED", styles['body'])],
        [Paragraph("Hardened Mutation Score", styles['body']), Paragraph("<b>84.73%</b> (111 Killed, 14 Survived, 6 Uncovered)", styles['body']), Paragraph("EXCELLENT (+24.4%)", styles['body'])],
        [Paragraph("Frontend Production Build", styles['body']), Paragraph("Vite 8.1.5 build completed in 1.61 seconds", styles['body']), Paragraph("VERIFIED (PASS)", styles['body'])],
        [Paragraph("Docker Compose Specification", styles['body']), Paragraph("Multi-container config verified (client, server, db)", styles['body']), Paragraph("VERIFIED (PASS)", styles['body'])],
        [Paragraph("RBAC & State Machine Integrity", styles['body']), Paragraph("Admin dashboard, volunteer transit guards enforced", styles['body']), Paragraph("VERIFIED (PASS)", styles['body'])],
    ]
    t = Table(summary_data, colWidths=[160, 240, 104])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # Section 2: Automated Testing Evidence
    story.append(Paragraph("2. Automated Integration & Regression Testing Evidence", styles['h1']))
    story.append(Paragraph("The test harness combines Jest, Supertest, and SQLite memory mode to execute tests with zero environmental dependencies.", styles['body']))
    
    test_run_text = """
    $ cd server && npm test<br/>
    &gt; cross-env NODE_ENV=test jest --detectOpenHandles --forceExit<br/>
    PASS  __tests__/auth.test.js (5 tests passed)<br/>
    PASS  __tests__/donations.test.js (7 tests passed)<br/>
    PASS  __tests__/regression.test.js (7 tests passed)<br/>
    PASS  __tests__/donationService.test.js (8 tests passed)<br/>
    <b>Test Suites: 4 passed, 4 total | Tests: 27 passed, 27 total | Time: 5.323 s</b>
    """
    story.append(Paragraph(test_run_text, styles['code']))
    
    # Section 3: Mutation Testing
    story.append(Paragraph("3. StrykerJS Mutation Testing Evidence & Analysis", styles['h1']))
    story.append(Paragraph("StrykerJS was configured to mutate <code>server/services/donationService.js</code> to test state machine transitions and boundary validations.", styles['body']))
    
    mut_table_data = [
        [Paragraph("<b>Metric</b>", styles['body']), Paragraph("<b>Baseline Run</b>", styles['body']), Paragraph("<b>Hardened Run</b>", styles['body']), Paragraph("<b>Analysis / Outcome</b>", styles['body'])],
        [Paragraph("Total Mutants Evaluated", styles['body']), Paragraph("131 mutants", styles['body']), Paragraph("131 mutants", styles['body']), Paragraph("Full AST syntax coverage", styles['body'])],
        [Paragraph("Mutants Killed (✓)", styles['body']), Paragraph("79 mutants", styles['body']), Paragraph("<b>111 mutants</b>", styles['body']), Paragraph("+32 mutants caught (+40.5%)", styles['body'])],
        [Paragraph("Mutants Survived (✘)", styles['body']), Paragraph("15 mutants", styles['body']), Paragraph("14 mutants", styles['body']), Paragraph("Non-critical edge logic", styles['body'])],
        [Paragraph("Uncovered Mutants (∅)", styles['body']), Paragraph("37 mutants", styles['body']), Paragraph("<b>6 mutants</b>", styles['body']), Paragraph("Dropped by 83.8%", styles['body'])],
        [Paragraph("Covered Mutation Score", styles['body']), Paragraph("84.04%", styles['body']), Paragraph("<b>88.80%</b>", styles['body']), Paragraph("High mutation accuracy", styles['body'])],
        [Paragraph("<b>Total Mutation Score</b>", styles['body']), Paragraph("60.31%", styles['body']), Paragraph("<b>84.73%</b>", styles['body']), Paragraph("<b>Grade A Verification (+24.42%)</b>", styles['body'])],
    ]
    mt = Table(mut_table_data, colWidths=[130, 95, 95, 184])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(mt)
    story.append(Spacer(1, 10))

    # Section 4: System Building & Version Management
    story.append(Paragraph("4. System Building & Version Management Evidence", styles['h1']))
    story.append(Paragraph("<b>Frontend Build (Vite 8.1.5):</b>", styles['h2']))
    story.append(Paragraph("<code>vite build<br/>dist/index.html (0.46 kB) | dist/assets/index.js (296.81 kB gzip: 95 kB)<br/>✓ built in 1.61s</code>", styles['code']))
    
    story.append(Paragraph("<b>Docker Compose Orchestration:</b>", styles['h2']))
    story.append(Paragraph("<code>docker compose config<br/>Services: client (5173), server (8000), db (mysql:8.0:3306 with healthcheck ping)<br/>Status: Validation successful (Exit code 0)</code>", styles['code']))

    story.append(Paragraph("<b>Version Management (Git Log History):</b>", styles['h2']))
    git_log_text = """
    * a038c11 [DA-3] Implement Admin governance, volunteer status transitions, test harness, Stryker mutation testing<br/>
    * 55da35f Update UI screenshots with higher resolution images<br/>
    * 3a12bb3 Final README cleanup<br/>
    * c14c4f8 Update README with accurate DA-2 software design details and tech stack<br/>
    * 96d28d4 Embed Architecture Diagram and UI screenshots directly into Design Document<br/>
    * 1074b67 DA-2: Add complete Architecture Draw.io, UI wireframes, and Software Design Document
    """
    story.append(Paragraph(git_log_text, styles['code']))

    # Section 5: Screenshot Checklist
    story.append(Paragraph("5. Functionalities & Screenshot Gallery Guide", styles['h1']))
    story.append(Paragraph("The visual proof checklist confirms working execution across all 5 user roles:", styles['body']))
    checklist_data = [
        [Paragraph("<b>Figure ID</b>", styles['body']), Paragraph("<b>Component / Screen</b>", styles['body']), Paragraph("<b>Demonstrated Behavior</b>", styles['body'])],
        [Paragraph("Figure 1", styles['body']), Paragraph("Terminal / Jest Execution", styles['body']), Paragraph("27/27 integration and regression tests passing", styles['body'])],
        [Paragraph("Figure 2", styles['body']), Paragraph("Stryker Mutation Report", styles['body']), Paragraph("84.73% mutation score on donationService.js", styles['body'])],
        [Paragraph("Figure 3", styles['body']), Paragraph("Git Version Management", styles['body']), Paragraph("Linear chronological commit history from DA-1 to DA-3", styles['body'])],
        [Paragraph("Figure 4", styles['body']), Paragraph("Vite Production Build", styles['body']), Paragraph("Production client build completing in 1.61 seconds", styles['body'])],
        [Paragraph("Figure 5", styles['body']), Paragraph("Docker Compose Validation", styles['body']), Paragraph("Orchestration syntax and healthcheck validation", styles['body'])],
        [Paragraph("Figure 6", styles['body']), Paragraph("User Registration", styles['body']), Paragraph("Role-based account registration with password hashing", styles['body'])],
        [Paragraph("Figure 7", styles['body']), Paragraph("Food Donor Dashboard", styles['body']), Paragraph("Creating surplus listing in 'Available' status", styles['body'])],
        [Paragraph("Figure 8", styles['body']), Paragraph("NGO Dashboard", styles['body']), Paragraph("Discovering and requesting meals (Status -> Requested)", styles['body'])],
        [Paragraph("Figure 9", styles['body']), Paragraph("Volunteer Dashboard", styles['body']), Paragraph("Accepting task and updating transit (-> Delivered)", styles['body'])],
        [Paragraph("Figure 10", styles['body']), Paragraph("Administrator Dashboard", styles['body']), Paragraph("Live platform statistics, audit table, registered users", styles['body'])],
    ]
    ct = Table(checklist_data, colWidths=[70, 160, 274])
    ct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(ct)

    build_pdf("docs/DA3_Evidence_Report.pdf", "ReFood Connect — Evidence Report", "DA-3 Testing & Quality Portfolio", story)

def generate_project_report_pdf():
    styles = get_custom_styles()
    story = []

    # Title block
    story.append(Paragraph("ReFood Connect — Smart Food Waste Redistribution Platform", styles['title']))
    story.append(Paragraph("Comprehensive Project Report | Digital Assignment 3 (BCSE301L)", styles['subtitle']))
    
    meta_text = """
    <b>Academic Institution:</b> Vellore Institute of Technology (VIT), Chennai Campus<br/>
    <b>Course Title & Code:</b> Software Engineering (BCSE301L)<br/>
    <b>Student Team:</b> Chirag Asija (24BDS1073) & Saanvi Gupta (24BDS1023)<br/>
    <b>Official GitHub Repository:</b> https://github.com/ChiragAsija1323/ReFood-Connect<br/>
    <b>Evaluation Milestone:</b> Review 3 (DA-3 Final Project Report & Appendices)
    """
    story.append(Paragraph(meta_text, styles['meta']))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=12))

    # 1. Problem Statement
    story.append(Paragraph("1. Problem Statement & Objectives", styles['h1']))
    story.append(Paragraph("Every day, commercial food establishments discard edible surplus food due to event completion or overproduction, while shelters and underprivileged communities suffer from nutritional insecurity. Manual coordination via phone calls and messaging apps results in perishability failures and zero traceability. ReFood Connect automates the surplus redistribution lifecycle by unifying Food Donors, NGOs, Volunteers, and Administrators in an audited, role-governed platform.", styles['body']))

    # 2. User Stories
    story.append(Paragraph("2. User Stories Across Defined Personas", styles['h1']))
    us_data = [
        [Paragraph("<b>ID</b>", styles['body']), Paragraph("<b>Persona</b>", styles['body']), Paragraph("<b>User Story Summary</b>", styles['body']), Paragraph("<b>Priority</b>", styles['body'])],
        [Paragraph("US-01", styles['body']), Paragraph("Donor", styles['body']), Paragraph("Register and log in securely with JWT issuance", styles['body']), Paragraph("Must Have", styles['body'])],
        [Paragraph("US-02", styles['body']), Paragraph("Donor", styles['body']), Paragraph("Post surplus batch with quantity and expiry timestamp", styles['body']), Paragraph("Must Have", styles['body'])],
        [Paragraph("US-03", styles['body']), Paragraph("NGO", styles['body']), Paragraph("Browse available listings and submit request claims", styles['body']), Paragraph("Must Have", styles['body'])],
        [Paragraph("US-04", styles['body']), Paragraph("Volunteer", styles['body']), Paragraph("Accept transport tasks and update transit to Delivered", styles['body']), Paragraph("Must Have", styles['body'])],
        [Paragraph("US-05", styles['body']), Paragraph("Admin", styles['body']), Paragraph("Access governance dashboard with real-time analytics", styles['body']), Paragraph("Must Have", styles['body'])],
        [Paragraph("US-06", styles['body']), Paragraph("All", styles['body']), Paragraph("Enforce salted password hashing and role access control", styles['body']), Paragraph("Must Have", styles['body'])],
    ]
    ut = Table(us_data, colWidths=[50, 70, 314, 70])
    ut.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(ut)
    story.append(Spacer(1, 10))

    # 3. System Architecture
    story.append(Paragraph("3. System Architecture & Design Principles", styles['h1']))
    story.append(Paragraph("ReFood Connect implements a Layered Client-Server Architecture utilizing the Service Layer Pattern. The React 19 frontend is decoupled from the Express 5 backend via a centralized Axios instance. Business logic is strictly contained within service classes (authService, donationService, adminService), while Sequelize ORM abstracts database persistence across MySQL (production) and SQLite (in-memory test isolation).", styles['body']))

    # 4. Design of Tests
    story.append(Paragraph("4. Design of Tests & Execution Results", styles['h1']))
    story.append(Paragraph("The empirical test suite consists of 27 automated tests across 4 test suites:", styles['body']))
    test_summary_text = """
    • Integration Tests (IT-01 to IT-12): Registration, Login, Donation creation, NGO claiming, Volunteer transit, DB persistence.<br/>
    • Regression Tests (RT-01 to RT-07): RBAC unauthorized rejection (403), Admin dashboard data integrity, invalid status transitions.<br/>
    • Unit / Mutation Tests (UT-01 to UT-08): Direct service validation, empty string rejection, role-specific query filtering.<br/>
    <b>Result: 27/27 Tests Passed (100% Pass Rate) | Execution Time: 5.32 seconds</b>
    """
    story.append(Paragraph(test_summary_text, styles['code']))

    # 5. Appendices
    story.append(Paragraph("5. Appendices", styles['h1']))
    
    story.append(Paragraph("Appendix A: Software Requirements Specification (SRS)", styles['h2']))
    story.append(Paragraph("<b>Functional:</b> Role-based JWT authentication; surplus batch creation with expiry validation; NGO request claiming; volunteer sequential transit tracking; admin analytics. <br/><b>Non-Functional:</b> Sub-second test execution via in-memory SQLite; bcrypt password hashing; SQL injection prevention via ORM; Docker containerization.", styles['body']))

    story.append(Paragraph("Appendix B: Data Flow Diagrams (DFD)", styles['h2']))
    story.append(Paragraph("<b>Level 0:</b> Food Donors submit food listings; NGOs submit donation claims; Volunteers receive transport routes and submit delivery status; Administrators receive aggregated redistribution metrics.<br/><b>Level 1:</b> Decomposed into Process 1.0 (Auth & Session), Process 2.0 (Donation Creation), Process 3.0 (Donation Allocation), Process 4.0 (Delivery Transit Management), and Process 5.0 (Admin Governance).", styles['body']))

    story.append(Paragraph("Appendix C: Entity-Relationship Diagram (ERD)", styles['h2']))
    story.append(Paragraph("<b>Users Entity:</b> id (PK), name, email (Unique), password (Hashed), role (donor|ngo|volunteer|admin).<br/><b>Donations Entity:</b> id (PK), donorId (FK -> Users.id), ngoId (FK -> Users.id), volunteerId (FK -> Users.id), foodDetails, quantity, expiryTime, status (Available|Requested|Accepted|Picked Up|Delivered).", styles['body']))

    story.append(Paragraph("Appendix D: Unified Modeling Language (UML) Diagrams", styles['h2']))
    story.append(Paragraph("<b>Use Cases:</b> Manage Donations, Claim Deliveries, View Admin Analytics.<br/><b>Sequence:</b> Donor posts -> NGO requests -> Volunteer accepts -> Volunteer picks up -> Volunteer delivers -> Status persisted in MySQL.<br/><b>Class Diagram:</b> Strict separation between Controllers, Services, and Models.", styles['body']))

    story.append(Paragraph("Appendix E: Code Listing & Repository Link", styles['h2']))
    story.append(Paragraph("Official GitHub Repository: <b>https://github.com/ChiragAsija1323/ReFood-Connect</b><br/>All source code, Docker configs, test suites, and documentation are committed on branch <code>main</code>.", styles['body']))

    build_pdf("docs/DA3_Project_Report.pdf", "ReFood Connect — Project Report", "DA-3 Full Report & Appendices", story)

if __name__ == '__main__':
    generate_evidence_pdf()
    generate_project_report_pdf()
