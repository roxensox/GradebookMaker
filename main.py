import ezsheets, session_checker

# This function loads the master class roster file using the roster's url and user-selected title
def loadRoster(rosterurl,title):
    print('loading roster...')
    sourceRoster = ezsheets.Spreadsheet(rosterurl)
    returnroster = ezsheets.createSpreadsheet(f'{title}_roster')
    for sheet in sourceRoster.sheetTitles:
        sourceRoster[sheet].copyTo(returnroster)
        returnroster[f'Copy of {sheet}'].title = sheet
    returnroster['Sheet1'].delete()
    print('roster loaded')
    return returnroster

# This function makes the attendance book using the roster object, attendance template and a pre-initialized target wb
def makeAttendance(roster,template,target):
    print('working on attendance book...')
    sessDict = session_checker.session_checker(roster.sheetTitles)
    for sec in roster.sheetTitles:
        rows = roster[sec].rowCount+2
        if sessDict[sec] == '1':
            template['ATTENDANCE_TEMPLATE16'].copyTo(target)
            target['Copy of ATTENDANCE_TEMPLATE16'].title = sec
        elif sessDict[sec] == '2':
            template['ATTENDANCE_TEMPLATE32'].copyTo(target)
            target['Copy of ATTENDANCE_TEMPLATE32'].title = sec
        target[sec]['B3'] = f'=IMPORTRANGE("{roster.url}","{sec}!A:B")'
        target[sec].rowCount = rows
    target[0].delete()
    print('attendance book generated')
    return target

# Does the same as the function above, but for assignments
def makeAssignment(roster,template,target):
    print('working on assignment book...')
    gradelevels = []
    for sec in roster.sheetTitles:
        if sec[0] not in gradelevels:
            gradelevels.append(sec[0])
    for l in gradelevels:
        for i in [1,2,3]:
            target.createSheet(f'M{l}Pre-Assign{i}')
            target.createSheet(f'M{l}Post-Assign{i}')

    # Make a template for each grade level using the formulas below to populate the fields to save requests
    for l in gradelevels:
        template[1].copyTo(target)
        target['Copy of ASSIGNMENTS_TEMPLATE'].title = f'M{l}_Template'
        for i in range(3,50):
            # Put score calculation in pre-midterm sections
            target[sec][f'D{i}'] = f"=IFNA(ROUNDUP(VLOOKUP(B{i},'M{l}Pre-Assign1'!$C:$D,2,FALSE)/$D$2,0)*10,0)"
            target[sec][f'E{i}'] = f"=IFNA(ROUNDUP(VLOOKUP(B{i},'M{l}Pre-Assign2'!$C:$D,2,FALSE)/$E$2,0)*10,0)"
            target[sec][f'F{i}'] = f"=IFNA(ROUNDUP(VLOOKUP(B{i},'M{l}Pre-Assign3'!$C:$D,2,FALSE)/$F$2,0)*10,0)"
            # Put score calculation in post-midterm sections
            target[sec][f'N{i}'] = f"=IFNA(ROUNDUP(VLOOKUP(B{i},'M{l}Post-Assign1'!$C:$D,2,FALSE)/$N$2,0)*10,0)"
            target[sec][f'O{i}'] = f"=IFNA(ROUNDUP(VLOOKUP(B{i},'M{l}Post-Assign2'!$C:$D,2,FALSE)/$O$2,0)*10,0)"
            target[sec][f'P{i}'] = f"=IFNA(ROUNDUP(VLOOKUP(B{i},'M{l}Post-Assign3'!$C:$D,2,FALSE)/$P$2,0)*10,0)"
    # Iterate through each class section and fill the fields in the template
    for sec in roster.sheetTitles:
        rows = roster[sec].rowCount+2
        target[f'M{sec[0]}_Template'].copyTo(target)
        target[f'Copy of M{sec[0]}'].title = sec
        target[sec]['B3'] = f'=IMPORTRANGE("{roster.url}","{sec}!A:B")'
        target[sec].rowCount = rows
    target[0].delete()
    for l in gradelevels:
        target[f'M{l}_Template'].delete()
    seclist = list(roster.sheetTitles)
    seclist.reverse()
    for sec in seclist:
        target[sec].index = 0
    print('assignment book generated')
    return target

# Does the same as the above, but also populates the grading components with formulas that link to the correct sources
def makeGradebook(roster, template, target, attendance, assignment):
    print('working on gradebook...')
    templatesheet = template[0]
    for section in roster.sheetTitles:
        rows = roster[section].rowCount + 1
        templatesheet.copyTo(target)
        target['Copy of GB_TEMPLATE'].title = section
        targsheet = target[section]
        targsheet.rowCount = rows
        rowslist = [targsheet.getRow(1)]
        for rownum in range(2, rows + 1):
            rowlist = [targsheet[f'A{rownum}'], '', '']
            rowlist.append(f'=ROUNDUP(10*(1-(VLOOKUP(B{rownum},IMPORTRANGE("{attendance.url}","{section}!B:I"),3,FALSE)/VLOOKUP(B2,IMPORTRANGE("{attendance.url}","{section}!B:I"),6,FALSE))))')
            rowlist.append(f'=VLOOKUP(B{rownum},IMPORTRANGE("{assignment.url}","{section}!B:Z"),6,FALSE)')
            rowlist.append(f'=VLOOKUP(B{rownum},IMPORTRANGE("{assignment.url}","{section}!B:Z"),8,FALSE)')
            rowlist.append(f'=sum(D{rownum}:F{rownum})')
            rowlist.append('')
            rowlist.append(f'=VLOOKUP(B{rownum},IMPORTRANGE("{assignment.url}","{section}!B:Z"),11,FALSE)')
            rowlist.append('')
            rowlist.append(f'=SUM(G{rownum},I{rownum})')
            rowlist.append('')
            rowlist.append(f'=ROUNDUP(10*(1-(VLOOKUP(B{rownum},IMPORTRANGE("{attendance.url}","{section}!B:I"),4,FALSE)/VLOOKUP(B2,IMPORTRANGE("{attendance.url}","{section}!B:I"),7,FALSE))))')
            rowlist.append(f'=VLOOKUP(B{rownum},IMPORTRANGE("{assignment.url}","{section}!B:Z"),16,FALSE)')
            rowlist.append(f'=VLOOKUP(B{rownum},IMPORTRANGE("{assignment.url}","{section}!B:Z"),18,FALSE)')
            rowlist.append(f'=SUM(M{rownum}:O{rownum})')
            rowlist.append('')
            rowlist.append(f'=SUM(P{rownum},K{rownum})')
            rowlist.append('')
            rowlist.append(f'=VLOOKUP(B{rownum},IMPORTRANGE("{assignment.url}","{section}!B:Z"),21,FALSE)')
            rowlist.append('')
            rowlist.append(f'=SUM(T{rownum},R{rownum})')
            rowslist.append(rowlist)
        targsheet.updateRows(rowslist)
        targsheet['B2'] = f'=IMPORTRANGE("{roster.url}","{section}!A:B")'
    target[0].delete()

def main(name, rosterUrl, gradebook_template_url):
    # Collects the class roster and template urls
    classroster = loadRoster(rosterUrl,name)

    '''PLEASE REMEMBER TO DO THIS!!!!
    MAKE SURE ALL LOADED TEMPLATES REFERENCE THE WORKBOOK WITH ALL THE TEMPLATES IN IT'''

    # Loads the template files
    print('loading templates...')
    u_template = ezsheets.Spreadsheet(gradebook_template_url)
    print('templates loaded')

    # Initializes the target files
    print('initializing gradebook...')
    gradebook = ezsheets.createSpreadsheet(f'{name}_GradeBook')
    print('gradebook initialized')
    print('initializing attendance book...')
    attendance_target = ezsheets.createSpreadsheet(f'{name}_Attendance')
    attendanceUrl = attendance_target.url
    print('attendance book initialized')
    print('initializing assignment book...')
    assignment_target = ezsheets.createSpreadsheet(f'{name}_Assignments')
    assignmentUrl = assignment_target.url
    print('assignment book initialized')

    # Makes the attendance and assignment workbooks
    attendsheet = makeAttendance(classroster,u_template,attendance_target)
    assignsheet = makeAssignment(classroster,u_template,assignment_target)

    # Takes the attendance and assignment wb objects and creates the gradebook
    makeGradebook(classroster,u_template,gradebook,attendsheet,assignsheet)
    print('done.')