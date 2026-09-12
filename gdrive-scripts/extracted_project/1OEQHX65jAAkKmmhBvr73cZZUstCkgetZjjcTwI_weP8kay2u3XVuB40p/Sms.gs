/**
 * ==========================================================
 * INFOGENX STUDENT ONBOARDING SYSTEM
 * SMS.GS
 * ==========================================================
 */

// Twilio Dialer API
const DIALER_SMS_URL = "https://twilliodialer.infogenx.com/dialer/send-sms/";
const DIALER_API_KEY = "infogenx-secret-2026"; // Replace with new key

// HR Mobile Number
const HR_MOBILE = "+919787806366";

/**
 * ----------------------------------------------------------
 * Send SMS
 * ----------------------------------------------------------
 */
function sendSMSMessage(mobile, message) {

  if (!mobile) {
    Logger.log("SMS Failed : Mobile number missing.");
    return false;
  }

  let formattedMobile = String(mobile).trim();

  if (!formattedMobile.startsWith("+")) {

    if (formattedMobile.length === 10) {
      formattedMobile = "+91" + formattedMobile;
    } else {
      formattedMobile = "+" + formattedMobile;
    }

  }

  const payload = {
    to: formattedMobile,
    message: message,
    company: "Infogenx",
    lead_source: "Student Onboarding"
  };

  const options = {
    method: "post",
    contentType: "application/json",
    headers: {
      "X-API-Key": DIALER_API_KEY
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  try {

    const response = UrlFetchApp.fetch(
      DIALER_SMS_URL,
      options
    );

    Logger.log(response.getContentText());

    return true;

  } catch (err) {

    Logger.log(err);

    return false;

  }

}

/**
 * ----------------------------------------------------------
 * Candidate Welcome SMS
 * ----------------------------------------------------------
 */
function sendCandidateSMS(student, password) {

  const message =
`Dear ${student.fullName},

Welcome to Infogenx.

Your registration has been completed successfully.

Login Portal:
https://infogenx-candidates-onboarding.netlify.app/

Email:
${student.email}

Password:
${password}

Thank you,
Infogenx HR`;

  return sendSMSMessage(
    student.mobile,
    message
  );

}

/**
 * ----------------------------------------------------------
 * HR Notification SMS
 * ----------------------------------------------------------
 */
function sendHRSMS(student) {

  const message =
`New Student Registration

Name : ${student.fullName}

Mobile : ${student.mobile}

Email : ${student.email}

City : ${student.city}

Qualification :
${student.qualification}

College :
${student.college}

Department :
${student.department}

Experience :
${student.experienceType}

Resume :
${student.resumeLink}`;

  return sendSMSMessage(
    HR_MOBILE,
    message
  );

}