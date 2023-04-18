from fpdf import FPDF
import os
import datetime

class PDF(FPDF): 
    '''
    PDF class is inherited from buit-in FPDF class (base class)
    '''
    def Addlogo(self):
        '''
        this method is to create the title page of report with logo
        '''

        self.image('logo.jpg',70,5,70)#adds a logo on top of first page
        self.line(10,35,200,35)
        self.set_font('times', 'BUI', 22)#set font is a precondition to add a cell
        self.cell(0,30,ln=1,border=0)

    def footer(self):
        '''
        extending footer to include page numbers.
        is called everytme a page is created
        '''

        self.set_y(-15)#-15 from the bottom
        self.set_font('times', 'I', 12)
        #f'string to store the page number
        page=f'Page # {self.page_no()} of {{nb}}'
        self.cell(0,12,page,align='R')
        
    def header(self):
        '''
        extending header method to add watermark on every page created in the report
        '''
        self.image('palgpetrol watermartk.png',26,105,160)

    def metaData(self,wordCount:int,instancesOfPlagerism: int,plagIndex:float):
        '''
        to add meta data like plag percentag, instances of plagiarism and date and time of
        creation of plagiarism report
        '''

        self.set_line_width(1)
        self.set_font('times', 'BI', 16)#bold and italic
        #all variables to be added as meta data
        current=datetime.datetime.now()
        curr_date:str=f'Date of Creation = ({current.day}-{current.month}-{current.year})'
        curr_time = f'Time Of Creation = {current.hour}:{current.minute}:{current.second}'
        a=f'{curr_date}                           {curr_time}'
        x:str=f'Word Count = {wordCount}'
        y:str=f'Total Instances of Plagiarism = {instancesOfPlagerism}'
        z:str=f'Plagiarism Percetage = {plagIndex * 100}%'
        #adding text to report
        self.multi_cell(0,8,a,ln=1,border=1)
        #self.set_x=(self.w)/2-5
        #self.multi_cell(((self.w)/2-15),8,curr_time,ln=1,border=1)
        self.cell(0,8,x,ln=1,border=1)
        self.cell(0,8,y,ln=1,border=1)
        self.cell(0,8,z,ln=1,border=1)

    def addNormally(self,x :str):
        '''
        add the text to pdf as it is
        '''
        
        text_length=self.get_string_width(x)+2
        self.multi_cell(0,8,x,ln=1)

    def addHighlighted(self,x:str,webLink):
        '''
        adds the passed (plagiarised) text to pdf as highlighted as well as
        the link of website from which plag was detected
        '''
        #add the plagiarised phrase
        self.ln(8)
        self.set_draw_color(0,0,0)
        self.set_fill_color(200,1,1)#highlight the cell as red
        text_length = self.get_string_width(x)+2
        self.multi_cell(0,8,x,ln=1,fill=1,border=1)
        #add the relevant link
        w = self.get_string_width(webLink) + 6
        self.set_font('times', 'U', 16)
        self.set_text_color()
        self.multi_cell(w,8,webLink,ln=1,fill=0,border=1)
        self.ln(8)
        self.set_font('times', '', 16)
        
def generate_report(filename: str, plagIndex: float, results: dict[str, str], wordCount: int, charCount: int, downloadFolder: str) -> None:
    '''
    create a pdf only if more than 10 words are present
    '''
    if(wordCount>=10):

        instancesOfPlagiarism:int=0#stores the number of sources from which plagiarism was detected
        references:str=['']#A set of all urls in dict
        pdf=PDF(orientation='P',unit='mm',format='A4')#pdf = an object of PDF class thta'll be used to create the report

        for phrase in results:
            '''
            makes a set of references present in dict -> references:str
            and their count -> instancesOfPlagiarism
            '''
            webLink=results[phrase]
            if webLink!='':
                if webLink not in references:
                    references.append(webLink)
                    instancesOfPlagiarism+=1

        #metaData of report.pdf file
        pdf.set_author('Team PlagPatrol')
        pdf.set_title('plagiarism report by PlagPatrol')

        # adding page & setting font
        pdf.set_auto_page_break(auto=True,margin=20)
        pdf.add_page()
        pdf.set_font('times', '', 22)# font (font style, bold/U/Italic, size)

        #creating header of first page with logo
        pdf.Addlogo()
        #adding meta data to report
        pdf.metaData(wordCount, instancesOfPlagiarism, plagIndex)
        pdf.ln(10)

        #adding the data in dict passed by web scrapper
        pdf.set_font('times', '', 16)

        phrases=list(results.keys())
        webLinks=list(results.values())
        i=0
        while i < len(results):

            if webLinks[i] == '':
                print(i)
                textToAdd:str = ''
                while (webLinks[i] == '') and (i < len(results)) :
                     textToAdd+=phrases[i];i+=1
                     
                pdf.addNormally(textToAdd)

            else:
                pdf.addHighlighted(phrases[i],webLinks[i])
                i+=1

           # else:
            #all plagiarised phrases with non-empty value in results are highlighted in the pdf
               # pdf.addHighlighted(phrase,webLink)
         
        #output the report
        os.chdir(downloadFolder)#specifies which directory to create the report.pdf in
        pdf.output(f'{filename}_plagiarism_report.pdf')
        os.path.remove(filename)#to delete the og file
