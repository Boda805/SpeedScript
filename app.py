import tkinter as tk
from tkinter import filedialog
from subprocess import Popen
import pandas as pd
import pypyodbc

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.create_status_bar()

    def create_widgets(self):
        self.template = tk.Button(self, text='Template File',command=self.open_template_file)
        self.template.pack(side=tk.TOP)
        
        self.upload = tk.Button(self, text='Upload File',command=self.upload_file)
        self.upload.pack(side=tk.TOP)

        self.submit = tk.Button(self, text='Submit file',command=self.submit_file)
        self.submit.pack(side=tk.TOP)

    def create_status_bar(self):
        self.status_bar = tk.Label(self, text='Status', bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def open_template_file(self):
        template_file = Popen('Upload_Template.xlsx', shell=True)
        return template_file

    def upload_file(self):
        self.file = filedialog.askopenfilename()
        df = pd.read_excel(self.file, converters={'stateID':str, 'grade':str})
        df = df.where(df.notnull(), '')
        
        conn = pypyodbc.connect('''DRIVER={Driver};
                                   SERVER=Server;
                                   DATABASE=DB;
                                   UID=UN;
                                   PWD=PW''')

        cursor = conn.cursor()

        cursor.execute('''TRUNCATE TABLE [dbo].[SpeedScript_Staging]''')

        cols = ",".join([str(i) for i in df.columns.tolist()])

        for i,row in df.iterrows():
            sql = """INSERT INTO [DB].[dbo].[SpeedScript_Staging] (%s) VALUES """ % (cols) + str(tuple(row))
            cursor.execute(sql)
            conn.commit()
            
            sql = """INSERT INTO [dbo].[SpeedScript_Log] (%s) VALUES """ % (cols) + str(tuple(row))
            cursor.execute(sql)
            conn.commit()
        
        row_check = cursor.execute('''select count(personID) from .[dbo].[SpeedScript_Staging] ss
                                    join [dbo].[Person] p on ss.[stateID] = p.[stateID] ''').fetchone()
        
        cursor.close()
        conn.close()

        if len(df) == row_check[0]:
            self.status_bar['text'] = 'Upload Succesful'
        
        else: 
            self.status_bar['text'] = 'Upload unsuccesful, please check spreadsheet for errors/typos'

    def submit_file(self):   
        conn = pypyodbc.connect('''DRIVER={Driver};
                                   SERVER=Server;
                                   DATABASE=DB;
                                   UID=UN;
                                   PWD=PW''')

        cursor = conn.cursor()

        sql = '''declare @TranscriptCredit Table (
		                    transcriptID      Int,
		                    personID	      Int,
		                    standardID        Int,
		                    creditsEarned     decimal(6,3),
		                    creditsAttempted  decimal(6,3)
		                    )

            insert into dbo.TranscriptCourse (personID, CourseNumber, courseName, stateCode, schoolName, date, startYear, endYear, grade, score, gpaWeight,gpaValue, gpaMax
            ,startTerm, endTerm, termsLong, actualTerm, distanceCode, unweightedGPAValue, districtID, termStartDate, termEndDate, specialGPA, summerSchool, transcriptField3, transcriptField4, transcriptField5)
            output inserted.transcriptID, inserted.personID, inserted.transcriptfield3, inserted.transcriptfield4, inserted.transcriptfield5
            into @TranscriptCredit (transcriptID, personID, standardID, creditsEarned, creditsAttempted)

            select p.personID, [courseNumber], [courseName], ss.[stateCode], [schoolName],cast(getdate() as smalldatetime), startYear, endYear, [grade], ss.[score], [gpaWeight], sli.gpaValue, gpaMax
            ,[startTerm], [endTerm], [termsLong], [actualTerm], [distanceCode], sli.unweightedGPAValue, 255
            ,[termStartDate], [termEndDate], specialGPA, summerSchool, standardID, [creditsEarned], [creditsAttempted]
            FROM dbo.[SpeedScript_Staging] ss
            join dbo.Person p on ss.[stateID] = p.stateID
            join dbo.CurriculumStandard cs on ss.[creditName] = cs.name and cs.parentID = 1 and cs.standardID != 71
            join dbo.ScoreListItem sli on ss.score = sli.score and sli.scoreGroupID = 1

            insert into dbo.TranscriptCredit (transcriptID, personID, standardID, creditsEarned, creditsAttempted)
            select transcriptID, personID, standardID, creditsEarned, creditsAttempted
            from @TranscriptCredit

            update dbo.TranscriptCourse
            set transcriptField3=Null, transcriptField4=Null, transcriptField5=Null
            from TranscriptCourse tc
            join @TranscriptCredit temp on tc.transcriptID = temp.transcriptID'''

        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()

if __name__=='__main__':        
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
