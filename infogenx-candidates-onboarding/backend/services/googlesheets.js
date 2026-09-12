import { google } from "googleapis";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const auth = new google.auth.GoogleAuth({
  keyFile: path.join(__dirname, "../credentials/service-account.json"),
  scopes: ["https://www.googleapis.com/auth/spreadsheets.readonly"],
});

const sheets = google.sheets({
  version: "v4",
  auth,
});

export async function getStudents() {
  const response = await sheets.spreadsheets.values.get({
    spreadsheetId: process.env.SPREADSHEET_ID,
    range: "Students!A:O",
  });

  const rows = response.data.values || [];

  if (rows.length <= 1) {
    return [];
  }

  const headers = rows[0];

  return rows.slice(1).map((row) => {
    const student = {};

    headers.forEach((header, index) => {
      student[header] = row[index] || "";
    });

    return student;
  });
}