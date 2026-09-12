import express from "express";
import nodemailer from "nodemailer";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const router = express.Router();

function getTransporter() {
  const host = process.env.SMTP_HOST || "smtp.gmail.com";
  const port = parseInt(process.env.SMTP_PORT || "587", 10);
  const user = process.env.SMTP_USER;
  const pass = process.env.SMTP_PASSWORD;

  if (!user || !pass) {
    throw new Error("SMTP credentials are not configured in backend/.env");
  }

  return nodemailer.createTransport({
    host,
    port,
    secure: port === 465,
    auth: { user, pass },
    tls: { rejectUnauthorized: false }
  });
}

function getFormattedDate(d = new Date()) {
  const day = d.getDate();
  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  const suffix = (day === 1 || day === 21 || day === 31) ? "st" :
                 (day === 2 || day === 22) ? "nd" :
                 (day === 3 || day === 23) ? "rd" : "th";
  return `${day}${suffix} ${monthNames[d.getMonth()]} ${d.getFullYear()}`;
}

router.post("/send-email", async (req, res) => {
  try {
    const {
      candidateName,
      candidateEmail,
      role = "Business Development Executive",
      department = "Business Development & Client Relations",
      salary = "₹30,000 per month",
      signatureDataUrl,
      pdfBase64,
      startDate,
      openingStatement,
      incentiveDescription,
      targets,
      reportingTools
    } = req.body;

    if (!candidateEmail || !candidateName) {
      return res.status(400).json({
        success: false,
        message: "Candidate name and email are required"
      });
    }

    const todayStr = getFormattedDate();
    const formattedStartDate = startDate || getFormattedDate(new Date(Date.now() + 7 * 24 * 60 * 60 * 1000));

    const defaultOpening = `Based on your technical proficiency, aptitude, and outstanding performance in our technical assessment, we believe you will be a valuable asset to our global operations.`;
    const resolvedOpening = openingStatement || defaultOpening;
    const resolvedIncentive = incentiveDescription || `You are eligible for a Performance-Linked Incentive (PLI) for every milestone successfully completed. The incentive is calculated based on milestone delivery, quality metrics, and profitability.`;
    const resolvedReporting = reportingTools || `the company's designated tracking systems (Google Sheets / Zoho CRM / Git Repositories)`;

    let targetsHtml = `
      <li><strong>Initial Target:</strong> Consistent output and adherence to project deliverables within your first month.</li>
      <li><strong>Contract Continuity:</strong> This offer is performance-linked. Maintaining quality output and proactive communication is required to ensure contract continuity.</li>
      <li><strong>Performance Review:</strong> A formal review will be conducted after six months. Upon satisfactory appraisal, a revision in base compensation and incentive tier will be evaluated.</li>
    `;
    if (Array.isArray(targets) && targets.length > 0) {
      targetsHtml = targets.map(t => `<li><strong>${t.label}:</strong> ${t.text}</li>`).join("\n");
    }

    // Paths to reference assets
    const headerPath = path.join(__dirname, "../assets/infogenx_header.jpeg");
    const directorSigPath = path.join(__dirname, "../assets/director_signature.jpeg");

    const attachments = [];

    // Header image CID
    if (fs.existsSync(headerPath)) {
      attachments.push({
        filename: "infogenx_header.jpeg",
        path: headerPath,
        cid: "infogenx_header"
      });
    }

    // Director signature CID
    if (fs.existsSync(directorSigPath)) {
      attachments.push({
        filename: "director_signature.jpeg",
        path: directorSigPath,
        cid: "director_sig"
      });
    }

    // Candidate signature CID or data URL
    let candidateSigHtml = `<span style="font-family: 'Brush Script MT', cursive; font-size: 22px; color: #00123C; border-bottom: 1px solid #00123C; padding: 0 10px;">${candidateName}</span>`;
    if (signatureDataUrl && signatureDataUrl.startsWith("data:image")) {
      const base64Data = signatureDataUrl.split(",")[1];
      attachments.push({
        filename: "candidate_signature.png",
        content: Buffer.from(base64Data, "base64"),
        cid: "candidate_sig"
      });
      candidateSigHtml = `<img src="cid:candidate_sig" alt="Candidate Signature" style="max-height: 50px; max-width: 220px; object-fit: contain; vertical-align: middle;" />`;
    }

    // PDF attachment if provided
    if (pdfBase64) {
      const cleanBase64 = pdfBase64.includes(",") ? pdfBase64.split(",")[1] : pdfBase64;
      attachments.push({
        filename: `OfferLetter-${candidateName.replace(/[^a-zA-Z0-9]/g, "_")}.pdf`,
        content: Buffer.from(cleanBase64, "base64"),
        contentType: "application/pdf"
      });
    }

    const htmlContent = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; color: #1e293b; background: #f8fafc; padding: 20px; margin: 0; line-height: 1.6; }
    .container { max-width: 720px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; border: 1px solid #e2e8f0; box-shadow: 0 4px 20px rgba(0,0,0,0.05); }
    .header-img { width: 100%; max-height: 120px; object-fit: contain; margin-bottom: 25px; }
    h1 { font-size: 20px; color: #00123C; margin: 0 0 10px; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #E65525; padding-bottom: 8px; }
    h2 { font-size: 15px; color: #00123C; margin: 20px 0 8px; text-transform: uppercase; font-weight: 700; }
    p { margin: 8px 0; font-size: 14px; }
    ul { margin: 8px 0 16px 20px; padding: 0; font-size: 14px; }
    li { margin-bottom: 6px; }
    .meta-date { text-align: right; font-size: 14px; color: #64748b; font-weight: 600; margin-bottom: 20px; }
    .salutation { font-size: 16px; font-weight: 700; color: #00123C; margin-bottom: 14px; }
    .highlight { background: #FFF8F3; border-left: 4px solid #E65525; padding: 12px 16px; margin: 15px 0; border-radius: 4px; font-weight: 600; }
    .sign-section { margin-top: 35px; border-top: 2px solid #e2e8f0; padding-top: 25px; }
    .sign-grid { display: table; width: 100%; margin-top: 15px; }
    .sign-col { display: table-cell; width: 50%; vertical-align: top; padding-right: 15px; }
    .sign-title { font-weight: 700; font-size: 14px; color: #00123C; margin-bottom: 8px; }
    .sign-box { min-height: 60px; margin: 10px 0; }
    .footer { text-align: center; margin-top: 35px; font-size: 12px; color: #94a3b8; border-top: 1px solid #f1f5f9; padding-top: 15px; }
  </style>
</head>
<body>
  <div class="container">
    <div style="text-align: center;">
      <img src="cid:infogenx_header" class="header-img" alt="Infogenx Private Limited" />
    </div>

    <div class="meta-date">Date: ${todayStr}</div>

    <div class="salutation">Dear ${candidateName},</div>

    <p>
      We are pleased to offer you the position of <strong>${role}</strong> in our <strong>${department}</strong> division at <strong>Infogenx Private Limited</strong>.
      ${resolvedOpening}
    </p>

    <p>Your employment will be governed by the following terms and conditions:</p>

    <h2>1. Remuneration & Compensation</h2>
    <ul>
      <li><strong>Fixed Monthly Compensation:</strong> You will receive a consolidated gross salary of <strong>${salary}</strong>.</li>
      <li><strong>Performance Incentives:</strong> ${resolvedIncentive}</li>
      <li><strong>Payment Schedule:</strong> Salary and earned incentives will be transferred to your designated bank account during the first week of every month, following the verification of your performance reports.</li>
    </ul>

    <h2>2. Performance Expectations & Targets</h2>
    <ul>
      ${targetsHtml}
    </ul>

    <h2>3. Reporting & Operations</h2>
    <p>
      As part of our data-driven approach, you are required to maintain a daily log of your activities and project statuses in the company's designated operational systems (<strong>${resolvedReporting}</strong>).
    </p>

    <h2>4. Acceptance and Commencement</h2>
    <p>
      Your official start date is scheduled for <strong>${formattedStartDate}</strong>.
      This letter constitutes our formal offer. By signing below, you acknowledge and agree to these terms.
    </p>

    <div class="sign-section">
      <div class="sign-grid">
        <div class="sign-col">
          <div class="sign-title">Authorization (For Infogenx Private Limited):</div>
          <div class="sign-box">
            <img src="cid:director_sig" alt="Director Signature" style="max-height: 45px; object-fit: contain;" />
          </div>
          <p style="margin: 2px 0;"><strong>Nithyanand Arumugham</strong><br>Director</p>
          <p style="margin: 2px 0; font-size: 13px; color: #64748b;">Phone: +91 97878 06366<br>Email: nithyanand.a@infogenx.com.au</p>
          <p style="margin: 4px 0; font-size: 13px;">Date: ${todayStr}</p>
        </div>

        <div class="sign-col" style="border-left: 1px dashed #cbd5e1; padding-left: 20px;">
          <div class="sign-title">Candidate Acceptance:</div>
          <p style="font-size: 13px; margin: 4px 0;">
            I, <strong>${candidateName}</strong>, accept the offer of employment as <strong>${role}</strong> under the terms outlined above.
          </p>
          <div class="sign-box">
            ${candidateSigHtml}
          </div>
          <p style="margin: 2px 0;"><strong>${candidateName}</strong></p>
          <p style="margin: 4px 0; font-size: 13px;">Date of Signing: ${todayStr}</p>
        </div>
      </div>
    </div>

    <div class="footer">
      Infogenx Private Limited • Official Candidate Onboarding System<br>
      Website: <a href="https://infogenx.com" style="color: #E65525;">https://infogenx.com</a> • Portal: <a href="https://candidates.infogenx.com" style="color: #E65525;">https://candidates.infogenx.com</a>
    </div>
  </div>
</body>
</html>
    `;

    const transporter = getTransporter();

    const mailOptions = {
      from: `"Infogenx HR Team" <${process.env.SMTP_USER}>`,
      to: candidateEmail,
      cc: "admin@infogenx.com",
      subject: `🎉 Congratulations! Your Official Infogenx Offer Letter - ${candidateName}`,
      html: htmlContent,
      attachments
    };

    const info = await transporter.sendMail(mailOptions);
    console.log(`[OfferLetter] Email sent successfully to ${candidateEmail}. Message ID: ${info.messageId}`);

    return res.json({
      success: true,
      message: `Offer Letter successfully emailed to ${candidateEmail}`,
      messageId: info.messageId,
      acceptedDate: todayStr
    });

  } catch (err) {
    console.error("[OfferLetter] Error sending offer letter email:", err);
    return res.status(500).json({
      success: false,
      message: err.message || "Failed to send Offer Letter email"
    });
  }
});

export default router;
