# GradebookMaker

Requires credentials json for Google Sheets API

NOTE: When first opening each workbook, you will have to give permission for each field to access the other workbooks

Inputs:
  - Username
  - URL for class roster workbook
    \ Class rosters should all be 2-column datasets, with unique student ID in the first column and name in the second column
    \ Each page of the workbook should be titled with the class section (6/1, 5/4, 1/1, etc.)
  - URL for the gradebook template workbook
  
Outputs:
  - Class roster file renamed with username
  - Gradebook main workbook with all fields initialized
  - Assignment workbook with all fields initialized and placeholder assignment result spreadsheets
  - Attendance workbook with 16 or 32 class sessions depending on frequency of class sessions
  - ALL ON GOOGLE DRIVE
