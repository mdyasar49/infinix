import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from '../pages/Auth/LoginPage'
import PdfLearningPage from '../pages/Learning/PdfLearningPage'
import PresentationPage from '../pages/Learning/PresentationPage'
import AssessmentPage from '../pages/Assessment/AssessmentPage'
import ResultPage from '../pages/Assessment/ResultPage'
import TaskPage from '../pages/Tasks/TaskPage'
import OfferLetterView from '../pages/HR/OfferLetterView'
import DashboardPage from '../pages/Dashboard/DashboardPage'
import LearningMaterialsPage from '../pages/Learning/LearningMaterialsPage'
import TrainingPage from '../pages/Learning/TrainingPage'
import JobRolesPage from '../pages/HR/JobRolesPage'
import HRInterviewPage from '../pages/HR/HRInterviewPage'
import RecruitmentProcessPage from '../pages/Tasks/RecruitmentProcessPage'
import OnboardingPage from '../pages/Onboarding/OnboardingPage'
import SignaturePage from '../pages/Onboarding/SignaturePage'
import SOPPage from '../pages/Onboarding/SOPPage'
import TermsConditionsPage from '../pages/Onboarding/TermsConditionsPage'
import CompletionPage from '../pages/Dashboard/CompletionPage'
import AdminOfferReviewPage from '../pages/Admin/AdminOfferReviewPage'
import ProtectedRoute from '../components/ProtectedRoute'
import VisualTheme from '../components/VisualTheme'

function AppRoutes() {
  return (
    <BrowserRouter>
      <VisualTheme />
      <Routes>
        <Route path="/" element={<Navigate to="/pdf" replace />} />
        <Route path="/login" element={<LoginPage />} />

        {/* 6-Stage Core Learning & Assessment Flow */}
        <Route path="/pdf" element={<ProtectedRoute><PdfLearningPage /></ProtectedRoute>} />
        <Route path="/pdf-learning" element={<Navigate to="/pdf" replace />} />

        <Route path="/ppt" element={<ProtectedRoute><PresentationPage /></ProtectedRoute>} />
        <Route path="/ppt-learning" element={<Navigate to="/ppt" replace />} />

        <Route path="/assessment" element={<ProtectedRoute><AssessmentPage /></ProtectedRoute>} />
        <Route path="/result" element={<ProtectedRoute><ResultPage /></ProtectedRoute>} />
        <Route path="/offer-letter" element={<ProtectedRoute><OfferLetterView /></ProtectedRoute>} />
        <Route path="/task" element={<ProtectedRoute><TaskPage /></ProtectedRoute>} />

        {/* HR & Careers */}
        <Route path="/hr-interview" element={<ProtectedRoute><HRInterviewPage /></ProtectedRoute>} />
        <Route path="/job-roles" element={<ProtectedRoute><JobRolesPage /></ProtectedRoute>} />
        <Route path="/signature" element={<ProtectedRoute><SignaturePage /></ProtectedRoute>} />

        {/* Learning & Orientation */}
        <Route path="/materials" element={<ProtectedRoute><LearningMaterialsPage /></ProtectedRoute>} />
        <Route path="/training" element={<ProtectedRoute><TrainingPage /></ProtectedRoute>} />
        <Route path="/sop" element={<ProtectedRoute><SOPPage /></ProtectedRoute>} />
        <Route path="/recruitment-process" element={<ProtectedRoute><RecruitmentProcessPage /></ProtectedRoute>} />

        {/* Portal, Dashboard & Completion */}
        <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/onboarding" element={<ProtectedRoute><OnboardingPage /></ProtectedRoute>} />
        <Route path="/terms" element={<ProtectedRoute><TermsConditionsPage /></ProtectedRoute>} />
        <Route path="/completion" element={<ProtectedRoute><CompletionPage /></ProtectedRoute>} />

        {/* Admin Offer Review & Approval Console */}
        <Route path="/admin/offer-review" element={<AdminOfferReviewPage />} />
        <Route path="/admin/offers" element={<ProtectedRoute><AdminOfferReviewPage /></ProtectedRoute>} />

        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRoutes

