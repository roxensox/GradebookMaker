# GradebookMaker

Class roster:
This is the main source file
Make a new sheet for each class and title it X/Y where X is grade level and Y is class number
Input student ID in column A
Input student nickname in column B

Attendance:
In cell B2, paste:
=importrange("CLASS_ROSTER_URL","SHEET_TITLE!A1:B50")

Replace “CLASS_ROSTER_URL” with the URL of your class roster workbook
Replace “SHEET_TITLE” with your class number before the exclamation point
Highlight columns B and C, press control-c and then control-shift-v
Press space on the checkboxes to toggle present/absent

Grades:
In cell B2, paste:  
=importrange("CLASS_ROSTER_URL","SHEET_TITLE!A1:B50")

In cell D2, paste: 
=ROUNDUP(10*(1-(VLOOKUP(B2,IMPORTRANGE("ATTENDANCE_URL","SHEET_TITLE!B2:G"),3,FALSE)/VLOOKUP(B2,IMPORTRANGE("ATTENDANCE_URL","SHEET_TITLE!B2:G"),6,FALSE))))

In cell I2, paste:
=VLOOKUP(B2,IMPORTRANGE("EXAMS_URL","SHEET_TITLE!B2:H50"),4,FALSE)

In cell T2, paste:
=VLOOKUP(B2,IMPORTRANGE("EXAMS_URL","SHEET_TITLE!B2:H50"),7,FALSE)

Drag cells B2, D2 and I2 down to the last row in the sheet

Exams:
Put the percentage grade for exams in the empty field, then a rounded score will appear in the next column
The score will automatically appear in the grades sheet
