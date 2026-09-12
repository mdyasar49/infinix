/**
 * ==========================================================
 * INFOGENX STUDENT ONBOARDING SYSTEM
 * API.GS - WEBHOOK & HTTP HANDLER
 * ==========================================================
 */

function doGet(e) {
  return jsonResponse({
    success: true,
    service: "Infogenx Candidate Onboarding Automation Engine",
    status: "ONLINE",
    account: "infogenx.jobs@gmail.com",
    timestamp: new Date().toISOString()
  });
}

function doPost(e) {
  try {
    let request = {};

    if (e.parameter && Object.keys(e.parameter).length > 0) {
      request = e.parameter;
    } else if (e.postData && e.postData.contents) {
      try {
        request = JSON.parse(e.postData.contents);
      } catch (parseErr) {
        request = e.parameter || {};
      }
    }

    const action = request.action || "register";

    switch (action) {
      case "register":
      case "onboard":
        return jsonResponse(onStudentRegistration({ student: request }));

      case "login":
      case "auth":
        return jsonResponse(authenticateStudent(request.email, request.password));

      case "health":
      case "ping":
        return jsonResponse({ success: true, status: "READY" });

      default:
        return jsonResponse({
          success: false,
          message: "Unknown action: " + action
        });
    }

  } catch (err) {
    return jsonResponse({
      success: false,
      message: err.message
    });
  }
}

function jsonResponse(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}