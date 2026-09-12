import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ProgressSidebar from '../../components/ProgressSidebar'
import { useAuth } from '../../hooks/useAuth'
import { onboardingWorkflow } from '../../services/authService'
import './JobRolesPage.css'

function JobRolesPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [activeCategory, setActiveCategory] = useState('all')

  const steps = onboardingWorkflow.map((step) => ({
    ...step,
    status: step.id === 3 ? 'current' : step.id < 3 ? 'complete' : 'locked',
  }))

  const roleCategories = [
    {
      id: 'web-mobile',
      title: '🌐 Web & Mobile Stacks',
      roles: [
        { title: 'Full Stack Developer', tech: ['MERN', 'MEAN', 'MEVN', 'LAMP'], desc: 'High-scalability web app development.' },
        { title: 'Mobile Engineer', tech: ['Flutter', 'React Native', 'Kotlin', 'Swift'], desc: 'Native & cross-platform iOS/Android development.' },
        { title: 'PHP & Python Developer', tech: ['Laravel', 'CodeIgniter', 'Django', 'Rails'], desc: 'Modern backend & API integrations.' },
      ]
    },
    {
      id: 'cloud-data',
      title: '☁ Cloud, Data & IPA',
      roles: [
        { title: 'Cloud & DevOps Engineer', tech: ['AWS', 'Azure', 'GCP', 'Docker'], desc: 'Infrastructure provisioning & CI/CD automation.' },
        { title: 'Data & BI Analyst', tech: ['Power BI', 'Python', 'SQL', 'Web Scraping'], desc: 'Business intelligence & data pipeline engineering.' },
        { title: 'IPA & Automation Engineer', tech: ['n8n', 'UiPath', 'Power Automate'], desc: 'Robotic process automation & workflow scripts.' },
      ]
    },
    {
      id: 'enterprise-nonit',
      title: '💼 Enterprise & Non-IT Roles',
      roles: [
        { title: 'Enterprise Solutions Consultant', tech: ['Power Platform', 'Zoho', 'Odoo', 'SAP'], desc: 'ERP & business system implementation.' },
        { title: 'UI/UX Designer', tech: ['Figma', 'Prototyping', 'Design Systems'], desc: 'Corporate portal UI and user experience.' },
        { title: 'HR & Operations Executive', tech: ['Recruitment', 'BDE', 'Admin', 'Content'], desc: 'Talent acquisition & client relations.' },
      ]
    }
  ]

  const filteredCategories = activeCategory === 'all'
    ? roleCategories
    : roleCategories.filter((cat) => cat.id === activeCategory)

  return (
    <div className="roles-shell">
      <ProgressSidebar steps={steps} />

      <main className="roles-main">
        <div className="roles-card">
          <div className="roles-header">
            <h2>Job Roles <span className="heading-accent">& Tech Stack Map</span></h2>
            <p>Explore target domain capabilities across Technical, Cloud, IPA, and Business Operations tracks.</p>
          </div>

          <div className="category-tabs">
            <button
              type="button"
              className={`cat-tab ${activeCategory === 'all' ? 'active' : ''}`}
              onClick={() => setActiveCategory('all')}
            >
              All Categories
            </button>
            <button
              type="button"
              className={`cat-tab ${activeCategory === 'web-mobile' ? 'active' : ''}`}
              onClick={() => setActiveCategory('web-mobile')}
            >
              🌐 Web & Mobile
            </button>
            <button
              type="button"
              className={`cat-tab ${activeCategory === 'cloud-data' ? 'active' : ''}`}
              onClick={() => setActiveCategory('cloud-data')}
            >
              ☁ Cloud, Data & IPA
            </button>
            <button
              type="button"
              className={`cat-tab ${activeCategory === 'enterprise-nonit' ? 'active' : ''}`}
              onClick={() => setActiveCategory('enterprise-nonit')}
            >
              💼 Enterprise & Non-IT
            </button>
          </div>

          {filteredCategories.map((cat) => (
            <section key={cat.id} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <h3>{cat.title}</h3>
              <div className="roles-grid">
                {cat.roles.map((role) => (
                  <div key={role.title} className="role-box">
                    <h4>{role.title}</h4>
                    <p>{role.desc}</p>
                    <div className="tech-pills">
                      {role.tech.map((t) => (
                        <span key={t} className="tech-pill">{t}</span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          ))}

          <div className="roles-actions">
            <button
              type="button"
              className="secondary-button"
              onClick={() => navigate('/recruitment-process')}
            >
              ← Back to Recruitment Process
            </button>
            <button
              type="button"
              className="primary-button"
              onClick={() => navigate('/assessment')}
            >
              Proceed to Technical Assessment →
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default JobRolesPage
