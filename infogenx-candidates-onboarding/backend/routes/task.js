import express from "express";

const router = express.Router();

// Store task submissions in memory
const taskSubmissions = {};

// POST /api/task/submit
router.post("/submit", (req, res) => {
  const { email, formLink, postLink, evidenceLink } = req.body;

  if (!email) {
    return res.status(400).json({ success: false, message: "Email is required" });
  }

  const cleanEmail = email.trim().toLowerCase();

  taskSubmissions[cleanEmail] = {
    formLink: formLink || "",
    postLink: postLink || "",
    evidenceLink: evidenceLink || "",
    submittedAt: new Date().toISOString(),
    status: "SUBMITTED",
  };

  return res.json({
    success: true,
    message: "Recruitment Task Evidence Submitted Successfully!",
    submission: taskSubmissions[cleanEmail],
  });
});

// GET /api/task/status?email=...
router.get("/status", (req, res) => {
  const email = (req.query.email || "").trim().toLowerCase();
  const submission = taskSubmissions[email] || null;

  return res.json({
    success: true,
    submitted: !!submission,
    submission,
  });
});

export default router;
