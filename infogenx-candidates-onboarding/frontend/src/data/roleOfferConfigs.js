// Role-specific offer letter configurations
export const ROLE_OFFER_CONFIGS = {
  'bde': {
    id: 'bde',
    title: 'Business Development Executive',
    department: 'Business Development & Client Relations',
    defaultSalary: '₹30,000 per month',
    openingStatement: 'Based on your sales acumen, communication skills, and assessment performance, we believe you will be instrumental in expanding our global client portfolio and commercial growth.',
    incentiveDescription: 'You are eligible for a Performance-Linked Incentive (PLI) for every enterprise contract and client account successfully closed and onboarded. The incentive is calculated based on gross project value and contract profitability.',
    targets: [
      { label: 'Initial Target', text: 'Generating a verified pipeline of prospective enterprise leads and meeting client outreach milestones within your first month.' },
      { label: 'Contract Continuity', text: 'Maintaining an active sales funnel and consistent lead-to-client conversion rate is required to ensure contract continuity.' },
      { label: 'Performance Review', text: 'A formal review will be conducted after six months. Upon achieving target revenue milestones, a 10% to 15% revision in base compensation and enhanced commission tier will be awarded.' }
    ],
    reportingTools: 'Zoho CRM and Google Sheets pipeline trackers'
  },
  'fullstack': {
    id: 'fullstack',
    title: 'Full Stack Developer',
    department: 'Software Engineering & Web Technologies',
    defaultSalary: '₹35,000 per month',
    openingStatement: 'Based on your technical proficiency in full-stack architecture, clean coding practices, and assessment performance, we believe you will be a core contributor to our product engineering lifecycle.',
    incentiveDescription: 'You are eligible for a Sprint Performance Incentive (SPI) for every milestone released on schedule with high test coverage and zero critical production defects.',
    targets: [
      { label: 'Initial Target', text: 'Rapid onboarding into our development stacks (MERN/MEAN), adhering to team coding conventions and completing designated sprint modules within your first month.' },
      { label: 'Contract Continuity', text: 'High code quality, timely pull requests, active peer code reviews, and meeting sprint delivery deadlines are required to ensure contract continuity.' },
      { label: 'Performance Review', text: 'A formal technical appraisal will be conducted after six months. Meeting software delivery benchmarks and architecture contributions will qualify you for a base salary revision.' }
    ],
    reportingTools: 'GitHub/GitLab commits, Jira sprint boards, and daily standup trackers'
  },
  'mobile': {
    id: 'mobile',
    title: 'Mobile Engineer (Flutter / React Native)',
    department: 'Mobile App Engineering',
    defaultSalary: '₹35,000 per month',
    openingStatement: 'Based on your mobile engineering skills, cross-platform UI mastery, and assessment performance, we believe you will elevate our native and cross-platform mobile offerings across Android and iOS.',
    incentiveDescription: 'You are eligible for a Milestone Delivery Incentive for successful store build releases (Google Play / Apple App Store) and maintaining 99.5%+ crash-free session rates.',
    targets: [
      { label: 'Initial Target', text: 'Successful build setup, component architecture, and delivery of responsive mobile screens within your first month.' },
      { label: 'Contract Continuity', text: 'Maintaining smooth 60fps UI performance, responsive layouts across device form factors, and timely bug fixes are required to ensure contract continuity.' },
      { label: 'Performance Review', text: 'A formal review will be conducted after six months. Demonstrating mobile platform ownership and automated release pipelines will qualify you for a base salary revision.' }
    ],
    reportingTools: 'GitHub Mobile Repositories, Jira Sprint Boards, and Firebase Crashlytics'
  },
  'cloud-devops': {
    id: 'cloud-devops',
    title: 'Cloud & DevOps Engineer',
    department: 'Cloud Infrastructure & DevOps',
    defaultSalary: '₹38,000 per month',
    openingStatement: 'Based on your knowledge of cloud architectures, CI/CD automation, containerization, and assessment performance, we believe you will guarantee the resilience and scalability of our infrastructure.',
    incentiveDescription: 'You are eligible for an Infrastructure Reliability Incentive based on achieving 99.9% uptime SLAs and automating deployment cycle times.',
    targets: [
      { label: 'Initial Target', text: 'Auditing existing cloud pipelines (AWS/GCP/Docker), establishing automated CI/CD workflows, and reducing deployment friction in your first month.' },
      { label: 'Contract Continuity', text: 'Infrastructure uptime, zero-downtime deployments, proactive security patching, and automated backup adherence are required to ensure contract continuity.' },
      { label: 'Performance Review', text: 'A formal review will be conducted after six months. Driving infrastructure cost optimization and cloud automation will qualify you for a base salary revision.' }
    ],
    reportingTools: 'Terraform/Git configurations, CloudWatch / Grafana monitoring alerts, and Jira'
  },
  'data-bi': {
    id: 'data-bi',
    title: 'Data & BI Analyst',
    department: 'Data Engineering & Business Intelligence',
    defaultSalary: '₹35,000 per month',
    openingStatement: 'Based on your analytical expertise, SQL/Python proficiency, data visualization capabilities, and assessment performance, we believe you will drive our data-informed decision making.',
    incentiveDescription: 'You are eligible for a Data Excellence Incentive for delivering automated ETL pipelines, verified data integrity, and high-impact Power BI executive dashboards.',
    targets: [
      { label: 'Initial Target', text: 'Structuring relational datasets, automating scheduled reporting queries, and publishing interactive dashboards within your first month.' },
      { label: 'Contract Continuity', text: 'Data accuracy, automated pipeline reliability, and delivering actionable business insights on schedule are required to ensure contract continuity.' },
      { label: 'Performance Review', text: 'A formal review will be conducted after six months. Demonstrating predictive modeling or advanced business analytics will qualify you for a base salary revision.' }
    ],
    reportingTools: 'Power BI Workspaces, SQL/Python ETL GitHub repositories, and ClickUp'
  },
  'ipa-automation': {
    id: 'ipa-automation',
    title: 'IPA & Automation Engineer',
    department: 'Intelligent Process Automation (IPA)',
    defaultSalary: '₹34,000 per month',
    openingStatement: 'Based on your workflow automation skills, robotic process development, and assessment performance, we believe you will drive our digital transformation and robotic automation efficiency.',
    incentiveDescription: 'You are eligible for a Process Efficiency Incentive for every automated workflow (n8n/UiPath/Power Automate) deployed that reduces measurable operational human-hours.',
    targets: [
      { label: 'Initial Target', text: 'Identifying repetitive operational bottlenecks, building pilot automation bots, and deploying error-tolerant webhooks within your first month.' },
      { label: 'Contract Continuity', text: 'Bot stability, exception handling, and continuous workflow optimization are required to ensure contract continuity.' },
      { label: 'Performance Review', text: 'A formal review will be conducted after six months. Demonstrating enterprise bot scalability will qualify you for a base salary revision.' }
    ],
    reportingTools: 'Central Automation Monitoring Dashboards, n8n webhook health logs, and Jira'
  },
  'ui-ux': {
    id: 'ui-ux',
    title: 'UI/UX Designer',
    department: 'Product Design & User Experience',
    defaultSalary: '₹32,000 per month',
    openingStatement: 'Based on your aesthetic excellence, user-centric thinking, prototyping prowess, and assessment performance, we believe you will shape the world-class visual identity of our products.',
    incentiveDescription: 'You are eligible for a Design Delivery Incentive for completing Figma design systems, interactive prototypes, and developer-ready handoff specs ahead of project deadlines.',
    targets: [
      { label: 'Initial Target', text: 'Establishing standardized Figma UI components, interactive user flows, and conducting usability audits within your first month.' },
      { label: 'Contract Continuity', text: 'Pixel-perfect design accuracy, responsive mobile/desktop wireframes, and collaborative developer handoffs are required to ensure contract continuity.' },
      { label: 'Performance Review', text: 'A formal review will be conducted after six months. Contributing to company-wide design systems and user satisfaction metrics will qualify you for a base salary revision.' }
    ],
    reportingTools: 'Figma Project Libraries, ClickUp Design Boards, and Loom walkthroughs'
  },
  'enterprise-consultant': {
    id: 'enterprise-consultant',
    title: 'Enterprise Solutions Consultant',
    department: 'Enterprise Solutions & ERP',
    defaultSalary: '₹36,000 per month',
    openingStatement: 'Based on your expertise in enterprise platforms (Zoho, Power Platform, Odoo, SAP) and assessment performance, we believe you will lead seamless ERP implementations for our enterprise clients.',
    incentiveDescription: 'You are eligible for an Implementation Success Incentive upon successful client ERP go-live and milestone sign-offs.',
    targets: [
      { label: 'Initial Target', text: 'Completing client requirement discovery, system blueprinting, and initial module configurations within your first month.' },
      { label: 'Contract Continuity', text: 'Smooth client deployment, user acceptance testing (UAT), and proactive client relationship management are required to ensure contract continuity.' },
      { label: 'Performance Review', text: 'A formal review will be conducted after six months with salary increment based on client retention and project delivery.' }
    ],
    reportingTools: 'Zoho Projects, client UAT milestone trackers, and Weekly Stakeholder reports'
  },
  'backend-dev': {
    id: 'backend-dev',
    title: 'PHP & Python Developer',
    department: 'Backend Engineering & APIs',
    defaultSalary: '₹34,000 per month',
    openingStatement: 'Based on your backend engineering skills, database design capabilities, and assessment performance, we believe you will build rock-solid server-side architectures and APIs.',
    incentiveDescription: 'You are eligible for an API Performance Incentive for delivering scalable microservices, low-latency database queries, and third-party integration milestones.',
    targets: [
      { label: 'Initial Target', text: 'Architecting robust RESTful endpoints, implementing JWT authentication, and integrating database schemas within your first month.' },
      { label: 'Contract Continuity', text: 'Code reliability, unit test coverage, and documentation via Swagger/Postman are required to ensure contract continuity.' },
      { label: 'Performance Review', text: 'A formal review will be conducted after six months with base salary revision upon meeting performance milestones.' }
    ],
    reportingTools: 'Git Repositories, Swagger/Postman API documentation, and Jira'
  },
  'hr-ops': {
    id: 'hr-ops',
    title: 'HR & Operations Executive',
    department: 'Human Resources & Talent Acquisition',
    defaultSalary: '₹30,000 per month',
    openingStatement: 'Based on your people skills, organizational acumen, and assessment performance, we believe you will be instrumental in scaling our candidate onboarding and people operations.',
    incentiveDescription: 'You are eligible for a Talent Onboarding Incentive for meeting recruitment turnaround targets, candidate verification quality, and smooth onboarding transitions.',
    targets: [
      { label: 'Initial Target', text: 'Managing candidate pipeline communications, scheduling technical assessments, and issuing onboarding packages within your first month.' },
      { label: 'Contract Continuity', text: 'High candidate satisfaction, zero SLA breaches in document verification, and accurate HR records are required to ensure contract continuity.' },
      { label: 'Performance Review', text: 'A formal review will be conducted after six months based on employee retention rates and talent acquisition milestones.' }
    ],
    reportingTools: 'HRMS candidate tracker, daily recruitment pipeline sheets, and weekly headcount reports'
  }
}

// Helper to detect best role key from user string
export function detectRoleKey(userOrRoleStr) {
  if (!userOrRoleStr) return 'bde'
  const str = typeof userOrRoleStr === 'string' ? userOrRoleStr.toLowerCase() : JSON.stringify(userOrRoleStr).toLowerCase()
  
  if (str.includes('fullstack') || str.includes('full stack') || str.includes('web') || str.includes('mern') || str.includes('developer')) {
    if (str.includes('php') || str.includes('python')) return 'backend-dev'
    return 'fullstack'
  }
  if (str.includes('mobile') || str.includes('flutter') || str.includes('react native') || str.includes('android') || str.includes('ios')) return 'mobile'
  if (str.includes('devops') || str.includes('cloud') || str.includes('aws') || str.includes('azure') || str.includes('docker')) return 'cloud-devops'
  if (str.includes('data') || str.includes('power bi') || str.includes('bi analyst') || str.includes('sql') || str.includes('analytics')) return 'data-bi'
  if (str.includes('ipa') || str.includes('automation') || str.includes('n8n') || str.includes('uipath') || str.includes('rpa')) return 'ipa-automation'
  if (str.includes('ui') || str.includes('ux') || str.includes('designer') || str.includes('figma')) return 'ui-ux'
  if (str.includes('enterprise') || str.includes('zoho') || str.includes('erp') || str.includes('odoo') || str.includes('sap')) return 'enterprise-consultant'
  if (str.includes('hr') || str.includes('recruitment') || str.includes('talent') || str.includes('operations')) return 'hr-ops'
  if (str.includes('bde') || str.includes('sales') || str.includes('business development')) return 'bde'
  
  return 'bde'
}
