import express from "express";
import { getStudents } from "../services/googleSheets.js";

const router = express.Router();

router.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({
        success: false,
        message: "Email and Password are required",
      });
    }

    const normalizedEmail = email.trim().toLowerCase();
    const adminEmail = process.env.ADMIN_EMAIL?.trim().toLowerCase();
    const adminPassword = process.env.ADMIN_PASSWORD;

    if (adminEmail && adminPassword && normalizedEmail === adminEmail && password === adminPassword) {
      return res.json({
        success: true,
        message: "Login Successful",
        student: {
          name: "Infogenx Administrator",
          email: adminEmail,
          role: "ADMIN",
        },
      });
    }

    const students = await getStudents();

    const student = students.find(
      (s) =>
        s["Email"]?.trim().toLowerCase() === normalizedEmail
    );

    if (!student) {
      return res.status(401).json({
        success: false,
        message: "Email not found",
      });
    }

    if (student["Generated Password"] !== password) {
      return res.status(401).json({
        success: false,
        message: "Invalid password",
      });
    }

    return res.json({
      success: true,
      message: "Login Successful",
      student: {
        name: student["Full Name"],
        email: student["Email"],
        mobile: student["Mobile Number"],
        qualification: student["Highest Qualification"],
        college: student["College Name"],
        department: student["Department"],
        skills: student["Skills"],
        role: "CANDIDATE",
      },
    });
  } catch (err) {
    console.error(err);

    return res.status(500).json({
      success: false,
      message: err.message,
    });
  }
});

export default router;
