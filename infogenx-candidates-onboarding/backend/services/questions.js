// Infogenx 50-MCQ Question Bank grounded in the official Infogenx Recruitment SOP & Orientation Deck

export const questionBank = [
  // 1. Infogenx Overview & Core Values (1-5)
  {
    id: 1,
    question: "How many years of global industry experience does Infogenx Pvt. Ltd. possess?",
    options: ["5+ Years", "7+ Years", "10+ Years", "15+ Years"],
    answer: 2 // 10+ Years
  },
  {
    id: 2,
    question: "What are the three core corporate principles of Infogenx?",
    options: ["LEARN, CODE, DEPLOY", "INNOVATE, AUTOMATE, SCALE", "PLAN, EXECUTE, DELIVER", "RESEARCH, TEST, LAUNCH"],
    answer: 1 // INNOVATE, AUTOMATE, SCALE
  },
  {
    id: 3,
    question: "In which two countries does Infogenx operate its primary development hubs?",
    options: ["India & USA", "India & Australia", "India & UK", "India & Singapore"],
    answer: 1 // India & Australia
  },
  {
    id: 4,
    question: "Where is the global headquarters of Infogenx located?",
    options: ["Bengaluru, Karnataka", "Hyderabad, Telangana", "Chennai, Tamil Nadu", "Mumbai, Maharashtra"],
    answer: 2 // Chennai, Tamil Nadu
  },
  {
    id: 5,
    question: "Which of the following is NOT listed as a core Infogenx service offering?",
    options: ["Smart Application Development", "Intelligent Process Automation (IPA)", "Heavy Machinery Manufacturing", "AI & Cloud Solutions"],
    answer: 2 // Heavy Machinery Manufacturing
  },

  // 2. Recruitment Sourcing & Boolean Search (6-15)
  {
    id: 6,
    question: "Which primary sourcing channels are utilized for IT and Technical recruitment at Infogenx?",
    options: ["LinkedIn, Naukri, Indeed, Upwork, Internshala", "Newspaper Ads & Radio", "Only Facebook Groups", "Local Print Flyers"],
    answer: 0
  },
  {
    id: 7,
    question: "In Boolean search algorithms, what effect does the 'AND' operator have on search queries?",
    options: ["Excludes second term", "Requires both terms to be present in candidate profile", "Matches either term randomly", "Makes terms case-sensitive"],
    answer: 1
  },
  {
    id: 8,
    question: "Which Boolean operator is used by Infogenx recruiters to exclude non-relevant profiles (e.g. Developer NOT Manager)?",
    options: ["AND", "OR", "NOT", "EXCLUDE"],
    answer: 2
  },
  {
    id: 9,
    question: "What is the purpose of quotation marks (\" \") in Boolean recruitment search?",
    options: ["Wildcard search", "Exact phrase match", "Fuzzy matching", "Case conversion"],
    answer: 1
  },
  {
    id: 10,
    question: "Which Boolean query correctly finds candidates skilled in both React and Node.js?",
    options: ["React OR Node.js", "React NOT Node.js", "React AND Node.js", "React NEAR Node.js"],
    answer: 2
  },
  {
    id: 11,
    question: "Which channels are targeted for Non-IT and Business Operations sourcing?",
    options: ["GitHub & StackOverflow", "LinkedIn, Indeed, PlacementIndia, Facebook Groups", "DockerHub", "Kaggle"],
    answer: 1
  },
  {
    id: 12,
    question: "For Offshore / Remote roles, which specialized candidate profile is primarily targeted?",
    options: ["Australian Time Zone Specialists", "Local Shift Workers", "Part-Time Tutors", "Freelance Graphic Artists"],
    answer: 0
  },
  {
    id: 13,
    question: "What is the standard duration of the initial screening phone call for shortlisted applicants?",
    options: ["2 Minutes", "5 Minutes", "10 Minutes", "45 Minutes"],
    answer: 2 // 10 Minutes
  },
  {
    id: 14,
    question: "What key parameters are verified during the 10-minute screening call?",
    options: ["Live coding only", "Communication skills, availability, and basic terms", "Complete salary payout", "Passport verification"],
    answer: 1
  },
  {
    id: 15,
    question: "What intake items must be submitted prior to scheduling Technical Round 1?",
    options: ["Verified intake form and code portfolio links", "Physical passport copy", "Hard copy resume only", "Original degree certificates"],
    answer: 0
  },

  // 3. Technical Stacks & Job Roles (16-25)
  {
    id: 16,
    question: "Which web development stack includes MongoDB, Express, React, and Node.js?",
    options: ["LAMP", "MERN", "MEVN", "MEAN"],
    answer: 1 // MERN
  },
  {
    id: 17,
    question: "Which native languages are supported for mobile engineering at Infogenx?",
    options: ["Kotlin (Android) & Swift (iOS)", "Java & C#", "Objective-C & C++", "Dart & Assembly"],
    answer: 0
  },
  {
    id: 18,
    question: "Which hybrid mobile framework is highlighted in Infogenx mobile tech stack?",
    options: ["Flutter & React Native", "Xamarin", "Ionic", "PhoneGap"],
    answer: 0
  },
  {
    id: 19,
    question: "Which Python backend framework is listed for high-scalability web engineering?",
    options: ["Flask", "Django", "FastAPI", "Bottle"],
    answer: 1 // Django
  },
  {
    id: 20,
    question: "Which Microsoft Low-Code suite is utilized for rapid business app creation?",
    options: ["Microsoft Power Platform (Power Apps & Power Automate)", "MS Office 365", "Azure DevOps", "Visual Studio Community"],
    answer: 0
  },
  {
    id: 21,
    question: "Which ERP and CRM solutions are part of Infogenx Enterprise Technology stack?",
    options: ["Zoho Suite, Odoo ERP, Microsoft Dynamics 365, SAP", "Salesforce Apex only", "Oracle ERP only", "Quickbooks"],
    answer: 0
  },
  {
    id: 22,
    question: "Which Intelligent Process Automation (IPA) tools are integrated at Infogenx?",
    options: ["n8n Automation & UiPath", "Selenium IDE only", "Bash scripts only", "Cron jobs only"],
    answer: 0
  },
  {
    id: 23,
    question: "Which public cloud providers are covered in Infogenx Cloud & DevOps engineering?",
    options: ["AWS, Azure, GCP", "DigitalOcean only", "Heroku only", "Linode only"],
    answer: 0
  },
  {
    id: 24,
    question: "What tool is leveraged for Business Intelligence & data dashboard creation?",
    options: ["Power BI", "Tableau Desktop only", "Excel 2007", "Google Data Studio only"],
    answer: 0 // Power BI
  },
  {
    id: 25,
    question: "Which of the following is listed under Non-IT & Operations Roles at Infogenx?",
    options: ["HR Executive, Recruiter, BDE, Office Admin, Content Manager", "DevOps Specialist", "Database Administrator", "Flutter Lead"],
    answer: 0
  },

  // 4. 2-Stage Evaluation Process (26-35)
  {
    id: 26,
    question: "What is Round 1 in the Infogenx candidate selection matrix?",
    options: ["HR Discussion", "Technical Round", "Final Salary Negotiation", "Written English Test"],
    answer: 1 // Technical Round
  },
  {
    id: 27,
    question: "Which evaluation components comprise Technical Round 1?",
    options: ["Domain Depth, Architecture, Live Coding / Logic, GitHub Review", "IQ Test & Typing Speed", "Personal Background Check", "Group Discussion"],
    answer: 0
  },
  {
    id: 28,
    question: "What is Round 2 in the Infogenx candidate evaluation framework?",
    options: ["Written Exam", "HR & Leadership Round", "System Design Only", "Aptitude Test"],
    answer: 1 // HR & Leadership
  },
  {
    id: 29,
    question: "What focus areas are assessed in HR & Leadership Round 2?",
    options: ["Cultural Fit, 2-3 Year Aspirations, Stress Handling, Salary Negotiations", "Complex Math Equations", "Compiler Internal Design", "Hardware Repair"],
    answer: 0
  },
  {
    id: 30,
    question: "How many total evaluation stages exist in the Infogenx candidate selection framework?",
    options: ["1 Stage", "2 Stages", "4 Stages", "6 Stages"],
    answer: 1 // 2 Stages
  },
  {
    id: 31,
    question: "What is inspected during the GitHub & Portfolio project review?",
    options: ["Code cleanliness, architecture, commit history, and documentation", "Number of stars only", "Profile picture resolution", "Account age"],
    answer: 0
  },
  {
    id: 32,
    question: "What is the recommended duration for the core technical logic assessment?",
    options: ["10 Minutes", "30 Minutes", "2 Hours", "24 Hours"],
    answer: 1 // 30 Minutes
  },
  {
    id: 33,
    question: "Which evaluation theme measures a candidate's long-term growth mindset?",
    options: ["Career Goals & 2-3 Year Aspirations", "Typing Speed", "Notice Period Penalty", "Social Media Followers"],
    answer: 0
  },
  {
    id: 34,
    question: "What candidate attribute is evaluated under stress handling assessment?",
    options: ["Professional responsiveness and problem solving under pressure", "Ability to work without sleep", "Memory retention of syntax", "Speed of typing"],
    answer: 0
  },
  {
    id: 35,
    question: "Who conducts the final commercial negotiations and culture fit confirmation?",
    options: ["HR & Leadership Desk", "Third-party agency", "Peer interns", "Automated bot"],
    answer: 0
  },

  // 5. Selection & Compensation Framework (36-43)
  {
    id: 36,
    question: "What is the standard formula for calculating a Freelancer's Hourly Rate (INR)?",
    options: ["Monthly Take-Home ÷ 30 ÷ 8", "Monthly Salary ÷ 10", "Annual CTC ÷ 12", "Monthly Salary ÷ 100"],
    answer: 0 // Monthly Take-Home ÷ 30 ÷ 8
  },
  {
    id: 37,
    question: "What is the base divisor for standard monthly hours used in the freelancer rate formula?",
    options: ["160 Hours", "200 Hours", "240 Hours", "300 Hours"],
    answer: 2 // 240 Hours (30 x 8)
  },
  {
    id: 38,
    question: "Using the formula (Take-Home ÷ 30 ÷ 8), what is the hourly rate for a ₹25,000 monthly take-home salary?",
    options: ["₹50 / hr", "₹105 / hr", "₹200 / hr", "₹350 / hr"],
    answer: 1 // ₹105 / hr
  },
  {
    id: 39,
    question: "What is the post-internship permanent conversion pay band for Diploma Graduates?",
    options: ["₹5,000 / month", "₹8,000 / month", "₹12,000 / month", "₹20,000 / month"],
    answer: 1 // ₹8,000 / month
  },
  {
    id: 40,
    question: "What is the post-internship conversion pay band for B.Sc. Graduates?",
    options: ["₹8,000 / month", "₹10,000 / month", "₹15,000 / month", "₹25,000 / month"],
    answer: 1 // ₹10,000 / month
  },
  {
    id: 41,
    question: "What is the post-internship conversion pay band for B.E. / M.C.A. / M.Sc. Graduates?",
    options: ["₹8,000 / month", "₹10,000 / month", "₹12,000 – ₹15,000+ / month", "₹30,000 / month"],
    answer: 2 // ₹12,000 – ₹15,000+ / month
  },
  {
    id: 42,
    question: "What is the stipend range during Months 4 - 5 of the internship progression roadmap?",
    options: ["Unpaid", "₹3,000 – ₹5,000 / Month", "₹8,000 – ₹15,000 / Month", "₹25,000 / Month"],
    answer: 1 // ₹3,000 – ₹5,000 / Month
  },
  {
    id: 43,
    question: "What is the stipend range during Month 6+ pre-conversion phase?",
    options: ["Unpaid", "₹1,000 / Month", "₹8,000 – ₹15,000+ / Month", "₹50,000 / Month"],
    answer: 2 // ₹8,000 – ₹15,000+ / Month
  },

  // 6. Onboarding & Compliance Protocol (44-50)
  {
    id: 44,
    question: "What is Step 1 in the candidate onboarding compliance checklist?",
    options: ["Verify Docs: ID & Degree Verification", "Sign NDA", "IT Setup", "Orientation"],
    answer: 0
  },
  {
    id: 45,
    question: "What binding agreement must be signed during onboarding for corporate data security?",
    options: ["Non-Disclosure Agreement (NDA)", "Non-Compete Agreement only", "Lease Deed", "Patent Waiver"],
    answer: 0 // NDA
  },
  {
    id: 46,
    question: "What key system assets are provisioned during Step 3 (IT Setup)?",
    options: ["Corporate Email & Portal Credential Access", "Personal Laptop Purchase", "Sim Card Distribution", "Home Broadband Connection"],
    answer: 0
  },
  {
    id: 47,
    question: "What takes place during Step 4 (Orientation)?",
    options: ["Mentor Alignment & Candidate Master Sheet entry", "Final Exit Interview", "Salary Deduction", "Hardware Audit"],
    answer: 0
  },
  {
    id: 48,
    question: "What is the official primary HR contact email address for Infogenx?",
    options: ["admin@infogenx.com", "hr@infogenx.com", "support@infogenx.com", "jobs@infogenx.com"],
    answer: 1 // hr@infogenx.com
  },
  {
    id: 49,
    question: "What is the off-campus drive desk email address for candidate inquiries?",
    options: ["infogenx.jobs@gmail.com", "drive@infogenx.com", "hr.drive@yahoo.com", "contact@infogenx.org"],
    answer: 0 // infogenx.jobs@gmail.com
  },
  {
    id: 50,
    question: "What milestone is achieved upon completing all candidate onboarding checklist steps?",
    options: ["READY TO WORK! Onboarding Complete", "Re-screening Required", "Probation Extended", "Form Submission Pending"],
    answer: 0 // READY TO WORK!
  }
]
