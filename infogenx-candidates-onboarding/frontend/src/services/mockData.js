export const studentProfile = {
  name: 'Aarna Mehta',
  id: 'INF-2026-0145',
  role: 'Student Onboarding Learner',
  batch: 'Summer 2026',
  location: 'Bengaluru, India',
  progressPercentage: 78,
  nextStep: 'Learning Materials',
}

export const onboardingSteps = [
  {
    id: 1,
    title: 'Login',
    description: 'Access the portal with your credentials.',
    route: '/login',
    status: 'complete',
  },
  {
    id: 2,
    title: 'Dashboard',
    description: 'Review your onboarding journey.',
    route: '/dashboard',
    status: 'complete',
  },
  {
    id: 3,
    title: 'Learning Materials',
    description: 'Complete the learning modules.',
    route: '/materials',
    status: 'current',
  },
  {
    id: 4,
    title: 'Terms & Conditions',
    description: 'Accept the onboarding agreement.',
    route: '/terms',
    status: 'locked',
  },
  {
    id: 5,
    title: 'Assessment',
    description: 'Complete the knowledge check.',
    route: '/assessment',
    status: 'locked',
  },
  {
    id: 6,
    title: 'Result',
    description: 'Review your assessment outcome.',
    route: '/result',
    status: 'locked',
  },
  {
    id: 7,
    title: 'Offer Letter',
    description: 'Review your premium offer.',
    route: '/offer-letter',
    status: 'locked',
  },
  {
    id: 8,
    title: 'Signature',
    description: 'Confirm the offer digitally.',
    route: '/signature',
    status: 'locked',
  },
  {
    id: 9,
    title: 'Training',
    description: 'Review your day-one onboarding plan.',
    route: '/training',
    status: 'locked',
  },
  {
    id: 10,
    title: 'Completion',
    description: 'Finalize your onboarding journey.',
    route: '/completion',
    status: 'locked',
  },
]

export const learningMaterials = [
  {
    id: 1,
    title: 'Infogenx Welcome Guide',
    type: 'PDF',
    description: 'An introduction to company culture, values, and onboarding expectations.',
    duration: '5 min read',
    status: 'completed',
  },
  {
    id: 2,
    title: 'Welcome to Infogenx',
    type: 'Video',
    description: 'A premium overview of Infogenx, teams, and career pathways.',
    duration: '12 min watch',
    status: 'current',
  },
  {
    id: 3,
    title: 'Security & Compliance',
    type: 'Document',
    description: 'A short guide to data privacy, security protocols and workplace conduct.',
    duration: '8 min read',
    status: 'locked',
  },
]

export const termsAgreement = {
  title: 'Infogenx Student Onboarding Terms & Conditions',
  sections: [
    {
      heading: 'Welcome to Infogenx',
      body: 'By continuing with this onboarding journey, you agree to follow the company code of conduct, complete assigned learning tasks and participate in scheduled assessments. The Infogenx onboarding portal provides access to training materials, evaluation checklists and corporate policies.',
    },
    {
      heading: 'Data Privacy & Compliance',
      body: 'All personal details and onboarding activity are handled according to Infogenx privacy guidelines. Students must maintain confidentiality, follow data handling best practices, and report any suspicious activity to the program administrator.',
    },
    {
      heading: 'Assessment & Eligibility',
      body: 'Completion of learning materials and assessments is required to move forward in the onboarding workflow. Assessment results are used to verify readiness for the next stage of the program and are not a formal employment evaluation.',
    },
    {
      heading: 'Offer Acceptance',
      body: 'After completing the assessment, you will review the offer letter, provide a digital signature, and confirm your acceptance. This portal is designed to capture your consent and prepare your onboarding path efficiently.',
    },
  ],
}

export const assessmentInfo = {
  title: 'Core Onboarding Assessment',
  description: 'A short knowledge check to confirm your readiness for Infogenx workflows and compliance guidelines.',
  duration: '15 Minutes',
  questions: 12,
  passScore: '70%',
  details: [
    'Multiple choice questions on company culture and policy.',
    'Scenario based queries for onboarding best practices.',
    'Instant summary of results after completion.',
  ],
}

export const resultSummary = {
  score: 88,
  total: 100,
  grade: 'Excellent',
  eligibility: 'Cleared for onboarding continuation',
  nextAction: 'Review Offer Letter',
}

export const offerLetter = {
  candidate: 'Aarna Mehta',
  role: 'Onboarding Trainee',
  location: 'Bengaluru, India',
  salary: '₹6,50,000 / annum',
  startDate: '01 August 2026',
  referenceId: 'INF-OL-2026-0917',
  summary: 'We are pleased to extend this premium offer as part of your Infogenx onboarding journey. Review the details carefully and proceed with signature confirmation to secure your placement.',
  benefits: [
    'Comprehensive onboarding support',
    'Buddy mentorship program',
    'Access to premium learning resources',
  ],
}

export const trainingPlan = {
  intro: 'Your first-day training plan is tailored for fast ramp-up and seamless orientation at Infogenx. Review the links and tasks below to stay on track.',
  resources: [
    {
      title: 'Team Introduction Guide',
      type: 'Guide',
      url: '#',
    },
    {
      title: 'HR Onboarding Checklist',
      type: 'Checklist',
      url: '#',
    },
    {
      title: 'Workplace Safety Brief',
      type: 'Video',
      url: '#',
    },
  ],
  tasks: [
    {
      title: 'Complete profile verification',
      status: 'Pending',
    },
    {
      title: 'Attend welcome session',
      status: 'Scheduled',
    },
    {
      title: 'Set up workspace access',
      status: 'Pending',
    },
  ],
}

export const completionData = {
  title: 'Onboarding Completed',
  message: 'Congratulations! You have successfully completed your Infogenx onboarding path. Your profile is now fully activated and ready for the next phase.',
  summary: [
    'All required materials completed',
    'Assessment reviewed and cleared',
    'Offer letter confirmed',
    'Digital acceptance captured',
  ],
}
