/**
 * ==========================================================
 * INFOGENX STUDENT ONBOARDING SYSTEM
 * FORM.GS
 * ==========================================================
 */

/**
 * ==========================================================
 * CREATE NEW REGISTRATION FORM
 * ==========================================================
 *
 * IMPORTANT:
 * Run this function ONLY when you actually need to create
 * a NEW registration form.
 *
 * Do NOT run this again if your existing form is already
 * connected and being used.
 */
function createRegistrationForm() {

  // Get Database ID
  const databaseId = PropertiesService
    .getScriptProperties()
    .getProperty("DATABASE_ID");

  if (!databaseId) {
    throw new Error(
      "DATABASE_ID not found. Run setupProject() first."
    );
  }

  // Open Spreadsheet
  const spreadsheet = SpreadsheetApp.openById(databaseId);

  // Create Google Form
  const form = FormApp.create(
    "Infogenx Internship Registration"
  );

  // Form title
  form.setTitle(
    "Infogenx Internship Registration"
  );

  // Form description
  form.setDescription(
    "Welcome to Infogenx Student Onboarding.\n\n" +
    "Please fill all the required details carefully.\n\n" +
    "Your password will be generated automatically and " +
    "sent to your registered email."
  );

  // Save Form ID
  PropertiesService
    .getScriptProperties()
    .setProperty("FORM_ID", form.getId());

  // Link Form to Spreadsheet
  form.setDestination(
    FormApp.DestinationType.SPREADSHEET,
    spreadsheet.getId()
  );


  /**
   * ========================================================
   * PERSONAL INFORMATION
   * ========================================================
   */

  form.addTextItem()
    .setTitle("Full Name")
    .setRequired(true);

  form.addDateItem()
    .setTitle("Date of Birth")
    .setRequired(true);

  form.addTextItem()
    .setTitle("Email Address")
    .setRequired(true);

  form.addTextItem()
    .setTitle("Mobile Number")
    .setRequired(true);

  form.addTextItem()
    .setTitle("City")
    .setRequired(true);


  /**
   * ========================================================
   * EDUCATION
   * ========================================================
   */

  form.addListItem()
    .setTitle("Highest Qualification")
    .setChoiceValues([
      "SSLC",
      "HSC",
      "Diploma",
      "UG",
      "PG",
      "Other"
    ])
    .setRequired(true);

  form.addTextItem()
    .setTitle("College Name")
    .setRequired(true);

  form.addTextItem()
    .setTitle("Department")
    .setRequired(true);

  form.addTextItem()
    .setTitle("Year of Passing")
    .setRequired(true);


  /**
   * ========================================================
   * SKILLS
   * ========================================================
   */

  form.addMultipleChoiceItem()
    .setTitle("Skill Category")
    .setChoiceValues([
      "IT",
      "Non-IT"
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("Skills")
    .setHelpText(
      "Example: HTML, CSS, JavaScript, React"
    )
    .setRequired(true);


  /**
   * ========================================================
   * EXPERIENCE
   * ========================================================
   */

  form.addMultipleChoiceItem()
    .setTitle("Experience Type")
    .setChoiceValues([
      "Fresher",
      "Experienced"
    ])
    .setRequired(true);

  form.addTextItem()
    .setTitle("Company Name")
    .setHelpText(
      "If Fresher, enter NA"
    )
    .setRequired(true);

  form.addTextItem()
    .setTitle("Experience (Years)")
    .setHelpText(
      "Example: 0, 1, 2.5"
    )
    .setRequired(true);

  form.addTextItem()
    .setTitle("Current Salary")
    .setHelpText(
      "If Fresher, enter NA"
    )
    .setRequired(true);

  form.addTextItem()
    .setTitle("Expected Salary")
    .setRequired(true);


  /**
   * ========================================================
   * RESUME
   * ========================================================
   */

  form.addTextItem()
    .setTitle("Resume Google Drive Link")
    .setRequired(true);


  /**
   * ========================================================
   * AVAILABILITY
   * ========================================================
   */

  form.addTextItem()
    .setTitle("Preferred Time")
    .setHelpText(
      "Example: Full-Time / Part-Time / Flexible"
    )
    .setRequired(true);


  /**
   * ========================================================
   * ADDITIONAL CANDIDATE INFORMATION
   * ========================================================
   */

  form.addTextItem()
    .setTitle("Certification")
    .setHelpText(
      "Enter your certification details. If none, enter NA."
    )
    .setRequired(true);

  form.addTextItem()
    .setTitle("LinkedIn Profile URL")
    .setHelpText(
      "Paste your LinkedIn profile URL."
    )
    .setRequired(true);

  form.addTextItem()
    .setTitle("Work Duration & Timings")
    .setHelpText(
      "Example: 10 AM - 7 PM / Full-Time"
    )
    .setRequired(true);

  form.addDateItem()
    .setTitle("Start Date")
    .setRequired(true);

  form.addTextItem()
    .setTitle(
      "Current Monthly Take Home Salary / Hourly Rate"
    )
    .setHelpText(
      "If not working, enter NA."
    )
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("Your Current Work Status")
    .setChoiceValues([
      "Freelancer",
      "Working in an Organisation",
      "Not working"
    ])
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle("If Working then")
    .setChoiceValues([
      "Hybrid",
      "WFH all days with Fixed Day/Hours",
      "Flexible"
    ])
    .setRequired(true);

  form.addParagraphTextItem()
    .setTitle("Preferred Availability")
    .setHelpText(
      "Mention your preferred weekday and weekend " +
      "time slots."
    )
    .setRequired(true);


  /**
   * ========================================================
   * LOGGING
   * ========================================================
   */

  Logger.log(
    "===================================="
  );

  Logger.log(
    "FORM CREATED SUCCESSFULLY"
  );

  Logger.log(
    "Form URL:"
  );

  Logger.log(
    form.getPublishedUrl()
  );

  Logger.log(
    "Form ID:"
  );

  Logger.log(
    form.getId()
  );

  Logger.log(
    "===================================="
  );
}


/**
 * ==========================================================
 * ADD ADDITIONAL FIELDS TO EXISTING FORM
 * ==========================================================
 *
 * IMPORTANT:
 * Use this function ONLY if the existing form was already
 * created using the old FORM.GS code.
 *
 * It will add ONLY the new fields.
 *
 * It will NOT create a new form.
 *
 * It will NOT duplicate the existing Resume field.
 * ==========================================================
 */
function addCandidateDetailsToExistingForm() {

  // Get existing Form ID
  const formId = PropertiesService
    .getScriptProperties()
    .getProperty("FORM_ID");

  if (!formId) {
    throw new Error(
      "FORM_ID not found. Please check Script Properties."
    );
  }

  // Open existing form
  const form = FormApp.openById(formId);

  /**
   * --------------------------------------------------------
   * Check existing item titles before adding anything.
   * This prevents accidental duplicate fields.
   * --------------------------------------------------------
   */

  const existingTitles = form
    .getItems()
    .map(function(item) {
      return item.getTitle();
    });


  /**
   * ========================================================
   * CERTIFICATION
   * ========================================================
   */

  if (!existingTitles.includes("Certification")) {

    form.addTextItem()
      .setTitle("Certification")
      .setHelpText(
        "Enter your certification details. If none, enter NA."
      )
      .setRequired(true);
  }


  /**
   * ========================================================
   * LINKEDIN
   * ========================================================
   */

  if (!existingTitles.includes("LinkedIn Profile URL")) {

    form.addTextItem()
      .setTitle("LinkedIn Profile URL")
      .setHelpText(
        "Paste your LinkedIn profile URL."
      )
      .setRequired(true);
  }


  /**
   * ========================================================
   * WORK DURATION & TIMINGS
   * ========================================================
   */

  if (!existingTitles.includes("Work Duration & Timings")) {

    form.addTextItem()
      .setTitle("Work Duration & Timings")
      .setHelpText(
        "Example: 10 AM - 7 PM / Full-Time"
      )
      .setRequired(true);
  }


  /**
   * ========================================================
   * START DATE
   * ========================================================
   */

  if (!existingTitles.includes("Start Date")) {

    form.addDateItem()
      .setTitle("Start Date")
      .setRequired(true);
  }


  /**
   * ========================================================
   * CURRENT TAKE HOME / HOURLY RATE
   * ========================================================
   */

  if (
    !existingTitles.includes(
      "Current Monthly Take Home Salary / Hourly Rate"
    )
  ) {

    form.addTextItem()
      .setTitle(
        "Current Monthly Take Home Salary / Hourly Rate"
      )
      .setHelpText(
        "If not working, enter NA."
      )
      .setRequired(true);
  }


  /**
   * ========================================================
   * CURRENT WORK STATUS
   * ========================================================
   */

  if (
    !existingTitles.includes(
      "Your Current Work Status"
    )
  ) {

    form.addMultipleChoiceItem()
      .setTitle(
        "Your Current Work Status"
      )
      .setChoiceValues([
        "Freelancer",
        "Working in an Organisation",
        "Not working"
      ])
      .setRequired(true);
  }


  /**
   * ========================================================
   * WORKING TYPE
   * ========================================================
   */

  if (
    !existingTitles.includes(
      "If Working then"
    )
  ) {

    form.addMultipleChoiceItem()
      .setTitle(
        "If Working then"
      )
      .setChoiceValues([
        "Hybrid",
        "WFH all days with Fixed Day/Hours",
        "Flexible"
      ])
      .setRequired(true);
  }


  /**
   * ========================================================
   * PREFERRED AVAILABILITY
   * ========================================================
   */

  if (
    !existingTitles.includes(
      "Preferred Availability"
    )
  ) {

    form.addParagraphTextItem()
      .setTitle(
        "Preferred Availability"
      )
      .setHelpText(
        "Mention your preferred weekday and weekend " +
        "time slots."
      )
      .setRequired(true);
  }


  /**
   * ========================================================
   * UPDATE FORM TITLE
   * ========================================================
   */

  form.setTitle(
    "Infogenx Internship Registration"
  );


  /**
   * ========================================================
   * LOGGING
   * ========================================================
   */

  Logger.log(
    "===================================="
  );

  Logger.log(
    "EXISTING FORM UPDATED SUCCESSFULLY"
  );

  Logger.log(
    "Form URL:"
  );

  Logger.log(
    form.getPublishedUrl()
  );

  Logger.log(
    "===================================="
  );
}