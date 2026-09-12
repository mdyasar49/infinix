/**
 * ==========================================================
 * INFOGENX STUDENT ONBOARDING SYSTEM
 * AUTH.GS
 * ==========================================================
 */

/**
 * Login Authentication
 */
function authenticateStudent(email, password) {
  email = cleanText(email).toLowerCase();
  const inputPassword = cleanText(password);

  if (!email || !inputPassword) {
    return {
      success: false,
      message: "Email and password are required."
    };
  }

  const student = getStudentByEmail(email);

  if (!student) {
    return {
      success: false,
      message: "Email not registered in candidate database."
    };
  }

  const passwordHash = generatePasswordHash(inputPassword);

  // Flexible authentication check:
  // 1. Plain text comparison (case-insensitive e.g. MOHA2001 or moha2001)
  // 2. Exact SHA-256 hash match
  // 3. Fallback match against student.password
  const isMatch = (student.password && student.password.toUpperCase() === inputPassword.toUpperCase()) ||
                  (student.passwordHash && student.passwordHash === passwordHash) ||
                  (student.password && student.password === inputPassword);

  if (!isMatch) {
    return {
      success: false,
      message: "Incorrect Password. Please check the credentials sent to your email."
    };
  }

  if (student.status && student.status !== "Active") {
    return {
      success: false,
      message: "Candidate account is inactive."
    };
  }

  updateLastLogin(student.row);

  return {
    success: true,
    message: "Login Successful.",
    student: {
      id: student.row,
      name: student.fullName,
      fullName: student.fullName,
      email: student.email,
      mobile: student.mobile,
      city: student.city,
      location: student.city || "Chennai, Tamil Nadu",
      qualification: student.qualification,
      college: student.college,
      department: student.department,
      yearOfPassing: student.yearOfPassing,
      skillCategory: student.skillCategory,
      skills: student.skills,
      role: "candidate"
    }
  };
}