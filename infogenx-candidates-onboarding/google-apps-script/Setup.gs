/**
 * ==========================================================
 * INFOGENX STUDENT ONBOARDING SYSTEM
 * SETUP.GS
 * ==========================================================
 */

const PROJECT_NAME = "Infogenx Student Onboarding";
const DATABASE_NAME = "Infogenx Student Database";

/**
 * ----------------------------------------------------------
 * CREATE PROJECT DATABASE
 * ----------------------------------------------------------
 */
function setupProject() {

  // Create Spreadsheet
  const spreadsheet = SpreadsheetApp.create(DATABASE_NAME);

  // Save Database ID
  PropertiesService.getScriptProperties().setProperty(
    "DATABASE_ID",
    spreadsheet.getId()
  );

  // Rename Default Sheet
  const studentsSheet = spreadsheet.getSheets()[0];
  studentsSheet.setName("Students");

  // Create Config Sheet
  const configSheet = spreadsheet.insertSheet("Config");

  // -----------------------------
  // Students Sheet Headers
  // -----------------------------
  const headers = [[
    "Registration Date",
    "Full Name",
    "Date of Birth",
    "Email",
    "Generated Password",
    "Password Hash",
    "Mobile Number",
    "City",
    "Highest Qualification",
    "College Name",
    "Department",
    "Year of Passing",
    "Skill Category",
    "Skills",
    "Experience Type",
    "Company Name",
    "Experience (Years)",
    "Current Salary",
    "Expected Salary",
    "Resume Link",
    "Preferred Time",
    "Status",
    "Created At",
    "Last Login"
  ]];

  studentsSheet
    .getRange(1, 1, 1, headers[0].length)
    .setValues(headers);

  studentsSheet
    .getRange(1, 1, 1, headers[0].length)
    .setFontWeight("bold")
    .setFontColor("#FFFFFF")
    .setBackground("#0F62FE")
    .setHorizontalAlignment("center");

  studentsSheet.setFrozenRows(1);
  studentsSheet.autoResizeColumns(1, headers[0].length);

  // -----------------------------
  // Config Sheet
  // -----------------------------
  const configData = [
    ["Project Name", PROJECT_NAME],
    ["Version", "1.0"],
    ["Database Name", DATABASE_NAME],
    ["Created On", new Date()],
    ["Default Status", "Active"],
    ["Password Rule", "First 4 letters of Name + Birth Year"],
    ["Developer", "Infogenx"]
  ];

  configSheet
    .getRange(1, 1, configData.length, 2)
    .setValues(configData);

  configSheet
    .getRange(1, 1, configData.length, 1)
    .setFontWeight("bold")
    .setBackground("#E8F0FE");

  configSheet.autoResizeColumns(1, 2);

  Logger.log("====================================");
  Logger.log("PROJECT CREATED SUCCESSFULLY");
  Logger.log("Spreadsheet URL:");
  Logger.log(spreadsheet.getUrl());
  Logger.log("====================================");
}