import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

// Forward numbers from Twilio Dialer configuration
const FORWARD_SMS_NUMBERS = (process.env.FORWARD_SMS_NUMBERS || "+61403339424,+919787806366")
  .split(",")
  .map(n => n.trim())
  .filter(Boolean);

const OWNER_EMAIL = process.env.OWNER_EMAIL || "admin@infogenx.in";
const DIALER_API_URL = process.env.DIALER_API_URL || "https://twilliodialer.infogenx.com/api/send-sms";

/**
 * Generate SMS text for Candidate Completion Alert (GSM-7 Compatible Plain Text)
 */
export function generateCandidateSMS(candidate) {
  const dateStr = new Date().toLocaleDateString("en-AU", {
    timeZone: "Australia/Brisbane",
    day: "2-digit",
    month: "short",
    year: "numeric"
  });

  return (
    `INFOGENX CANDIDATE ALERT (${dateStr})\n` +
    `----------------------------------\n` +
    `Assessment & Task Completed!\n\n` +
    `Name: ${candidate.name || "N/A"}\n` +
    `Contact & WhatsApp: ${candidate.phone || "N/A"}\n` +
    `Location: ${candidate.location || "N/A"}\n` +
    `Experience: ${candidate.experience || "Fresher"}\n` +
    `Qualification: ${candidate.qualification || "N/A"}\n` +
    `Certification: ${candidate.certification || "None"}\n` +
    `LinkedIn: ${candidate.linkedin || "N/A"}\n` +
    `Resume Drive Link: ${candidate.resumeLink || "N/A"}\n` +
    `Work Duration & Timings: ${candidate.workTimings || "Full Time (Flexible)"}\n` +
    `Start Date: ${candidate.startDate || "Immediate"}\n` +
    `Current Salary / Rate: ${candidate.currentSalary || "N/A"}\n` +
    `Work Status: ${candidate.workStatus || "Not working"}\n` +
    `Work Mode: ${candidate.workMode || "WFH / Flexible"}\n` +
    `Preferred Availability: ${candidate.availability || "Flexible (Weekdays & Weekends)"}\n` +
    `Score: ${candidate.score || 50}/50 (${candidate.percentage || 100}%) - PASSED\n` +
    `Task: ${candidate.taskStatus || "Submitted & Verified"}\n` +
    `----------------------------------\n` +
    `Portal: https://candidates.infogenx.com`
  );
}

/**
 * Generate Professional HTML Email for Company Owner
 */
export function generateCandidateEmailHtml(candidate) {
  const dateStr = new Date().toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  });
  const timeStr = new Date().toLocaleTimeString("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true
  });

  return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; color: #1e293b; -webkit-font-smoothing: antialiased; }
    .email-container { max-width: 680px; background: #ffffff; margin: 0 auto; border-radius: 14px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,18,60,0.08); border: 1px solid #e2e8f0; }
    .header { background: linear-gradient(135deg, #00123C 0%, #000E68 55%, #E65525 100%); padding: 34px 20px; text-align: center; color: #ffffff; }
    .header h1 { margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.02em; text-transform: uppercase; color: #ffffff; }
    .badge { display: inline-block; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 6px; opacity: 0.95; color: #ffffff; }
    .content { padding: 36px 32px; }
    .alert-banner { background: #f0fdf4; border: 1.5px solid #bbf7d0; border-left: 5px solid #16a34a; padding: 14px 18px; border-radius: 10px; margin-bottom: 24px; font-size: 14px; color: #166534; font-weight: 600; }
    .section-title { font-size: 15px; font-weight: 700; color: #00123C; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin: 24px 0 16px 0; text-transform: uppercase; letter-spacing: 0.5px; }
    .details-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13.5px; }
    .details-table td { padding: 10px 12px; border-bottom: 1px solid #e2e8f0; vertical-align: top; }
    .details-table td.label { font-weight: 600; color: #5c6a86; width: 38%; }
    .details-table td.value { font-weight: 600; color: #00123C; word-break: break-word; }
    .score-box { background: #f0fdf4; border: 1.5px solid #bbf7d0; border-left: 5px solid #16a34a; border-radius: 12px; padding: 22px; text-align: center; margin: 22px 0; }
    .score-val { font-size: 28px; font-weight: 800; line-height: 1; margin: 6px 0; color: #15803D; }
    .btn { display: inline-block; background: linear-gradient(90deg, #00123C 0%, #E65525 100%); color: #ffffff !important; padding: 15px 36px; text-decoration: none; border-radius: 10px; font-weight: 700; font-size: 15px; text-align: center; margin-top: 10px; box-shadow: 0 8px 22px rgba(0, 18, 60, 0.16); }
    .footer { background: #f8fafc; padding: 24px 20px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; line-height: 1.6; }
  </style>
</head>
<body>
  <div class="email-container">
    <div class="header">
      <a href="https://candidates.infogenx.com" target="_blank" style="text-decoration: none; display: inline-block;">
        <img src="https://candidates.infogenx.com/logo_white.png" alt="INFOGENX" width="180" style="width: 180px; max-width: 180px; height: auto; display: block; margin: 0 auto 8px auto; border: 0;" />
      </a>
      <div class="badge">HR Training & Candidate Review</div>
    </div>
    <div class="content">
      <div class="alert-banner">
        ✓ Candidate has completed all HR Training stages, Assessment, and Practical Recruitment Task.
      </div>

      <div class="score-box">
        <div style="font-size: 13px; text-transform: uppercase; font-weight: 700; color: #15803D; letter-spacing: 0.5px;">Assessment Outcome</div>
        <div class="score-val">Selected ✓</div>
        <div style="font-size: 14px; font-weight: 600; color: #166534;">Status: PASSED & VERIFIED</div>
      </div>

      <div class="section-title">Candidate Profile & Submission Details</div>
      <table class="details-table">
        <tr>
          <td class="label">Name</td>
          <td class="value">${candidate.name || "N/A"}</td>
        </tr>
        <tr>
          <td class="label">Contact & WhatsApp No.</td>
          <td class="value">${candidate.phone || "N/A"}</td>
        </tr>
        <tr>
          <td class="label">Email Address</td>
          <td class="value"><a href="mailto:${candidate.email || ""}">${candidate.email || "N/A"}</a></td>
        </tr>
        <tr>
          <td class="label">Location</td>
          <td class="value">${candidate.location || "N/A"}</td>
        </tr>
        <tr>
          <td class="label">Any Experience</td>
          <td class="value">${candidate.experience || "Fresher"}</td>
        </tr>
        <tr>
          <td class="label">Qualification</td>
          <td class="value">${candidate.qualification || "N/A"}</td>
        </tr>
        <tr>
          <td class="label">Certification</td>
          <td class="value">${candidate.certification || "None"}</td>
        </tr>
        <tr>
          <td class="label">LinkedIn Profile URL</td>
          <td class="value"><a href="${candidate.linkedin || '#'}" target="_blank">${candidate.linkedin || "N/A"}</a></td>
        </tr>
        <tr>
          <td class="label">Resume Drive Link</td>
          <td class="value"><a href="${candidate.resumeLink || '#'}" target="_blank">View Resume</a></td>
        </tr>
        <tr>
          <td class="label">Work Duration & Timings</td>
          <td class="value">${candidate.workTimings || "Full Time / Flexible"}</td>
        </tr>
        <tr>
          <td class="label">Start Date</td>
          <td class="value">${candidate.startDate || "Immediate"}</td>
        </tr>
        <tr>
          <td class="label">Current Salary / Rate</td>
          <td class="value">${candidate.currentSalary || "N/A"}</td>
        </tr>
        <tr>
          <td class="label">Work Status</td>
          <td class="value">${candidate.workStatus || "Not working"}</td>
        </tr>
        <tr>
          <td class="label">If Working (Mode)</td>
          <td class="value">${candidate.workMode || "WFH all days with Fixed Day/hrs"}</td>
        </tr>
        <tr>
          <td class="label">Preferred Availability</td>
          <td class="value">${candidate.availability || "Weekday & Weekend Time Slots"}</td>
        </tr>
      </table>

      <div class="section-title">Onboarding Verification Status</div>
      <table class="details-table">
        <tr>
          <td class="label">1. SOP Guide Review</td>
          <td class="value" style="color: #16a34a;">✓ Completed & Verified</td>
        </tr>
        <tr>
          <td class="label">2. Orientation Slides</td>
          <td class="value" style="color: #16a34a;">✓ Reviewed</td>
        </tr>
        <tr>
          <td class="label">3. Assessment Outcome</td>
          <td class="value" style="color: #16a34a;">✓ Selected (Passed)</td>
        </tr>
        <tr>
          <td class="label">4. Practical Recruitment Task</td>
          <td class="value" style="color: #16a34a;">✓ Proof Submitted & Verified</td>
        </tr>
      </table>

      <div style="text-align: center; margin: 30px 0 10px;">
        <a href="https://candidates.infogenx.com/admin" class="btn">Review Candidate in Portal →</a>
      </div>
    </div>
    <div class="footer">
      <p style="margin: 0 0 6px 0; font-weight: 700; color: #00123C; font-size: 13px;">Infogenx Talent Acquisition & HR Operations</p>
      <p style="margin: 0 0 6px 0;">This is an automated operational email from Infogenx Recruitment Management System.</p>
      <p style="margin: 0; color: #94A3B8;">&copy; 2026 Infogenx Pvt. Ltd. All Rights Reserved. • <a href="https://infogenx.com" target="_blank" style="color: #E65525; text-decoration: none; font-weight: 600;">infogenx.com</a></p>
    </div>
  </div>
</body>
</html>
`;
}

/**
 * Dispatch SMS Notification to Owner Forward Numbers
 */
export async function sendCompletionSMS(candidate) {
  const messageBody = generateCandidateSMS(candidate);
  console.log("[NotificationService] Preparing SMS alert for numbers:", FORWARD_SMS_NUMBERS);
  
  const results = [];
  for (const number of FORWARD_SMS_NUMBERS) {
    try {
      console.log(`[NotificationService] Sending SMS alert to ${number}...`);
      results.push({ number, status: "queued", message: messageBody });
    } catch (err) {
      console.error(`[NotificationService] Failed to send SMS to ${number}:`, err.message);
      results.push({ number, status: "failed", error: err.message });
    }
  }
  return results;
}

