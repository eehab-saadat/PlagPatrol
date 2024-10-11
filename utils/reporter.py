from fpdf import FPDF
import os
import datetime

class PDF(FPDF):
    '''
    PDF class is inherited from buit-in FPDF class (base class)
    '''

    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation=orientation, unit=unit, format=format)
        self.parent_dir = os.path.dirname((os.path.dirname(__file__)))

    def Addlogo(self):
        '''
        this method is to create the title page of report with logo
        '''
        self.image(f'{self.parent_dir}/static/assets/plag_patrol_logo.png', 62, 2, 83,48)  # adds a logo on top of first page
        self.line(10, 52, 200, 52)
        # set font is a precondition to add a cell
        self.set_font('times', 'BUI', 22)
        self.cell(0, 30, ln=1, border=0)
        self.ln(16)

    def footer(self):
        '''
        extending footer to include page numbers.
        is called everytme a page is created
        '''

        self.set_y(-15)  # -15 from the bottom
        self.set_font('times', 'I', 12)
        # f'string to store the page number
        page = f'Page # {self.page_no()} of {{nb}}'
        self.cell(0, 12, page, align='R')

    def header(self):
        '''
        extending header method to add watermark on every page created in the report
        '''
        self.image(f"{self.parent_dir}/static/assets/plagpetrol watermark.png", 20, 125, 180)

    def metaData(self, wordCount: int, instancesOfPlagerism: int, plagIndex: float):
        '''
        to add meta data like plag percentag, instances of plagiarism and date and time of
        creation of plagiarism report
        '''
        plagIndex = float(plagIndex) * 100
        self.set_line_width(1)
        self.set_font('times', 'BI', 16)  # bold and italic
        # all variables to be added as meta data
        current = datetime.datetime.now()
        curr_date: str = f'Date of Creation = ({current.day}-{current.month}-{current.year})'
        curr_time = f'Time Of Creation = {current.hour}:{current.minute}:{current.second}'
        a = f'{curr_date}              |            {curr_time}'
        x: str = f'Word Count = {wordCount}'
        y: str = f'Total Instances of Plagiarism = {instancesOfPlagerism}'
        z: str = f'Plagiarism Percetage = {plagIndex}%'
        # adding text to report
        self.multi_cell(0, 8, a, ln=1, border=1)
        self.cell(0, 8, x, ln=1, border=1)
        self.cell(0, 8, y, ln=1, border=1)
        self.cell(0, 8, z, ln=1, border=1)

    def addNormally(self, x: str):
        '''
        add the text to pdf as it is
        '''
        self.multi_cell(0, 6, x, ln=1)
        self.ln(5)

    def addHighlighted(self, x: str, webLink):
        '''
        adds the passed (plagiarised) text to pdf as highlighted as well as
        the link of website from which plag was detected
        '''
        # add the plagiarised phrase
        self.set_draw_color(0, 0, 0)
        self.set_fill_color(220, 1, 1)  # highlight the cell as red
        text_length = self.get_string_width(x)+2
        self.multi_cell(0, 8, x, ln=1, fill=1, border=1)
        # add the relevant link
        self.set_font('DejaVuSans', 'U', 14)
        self.set_text_color(0)
    
        self.multi_cell(0, 8, f'Found on :\n{webLink}', ln=1, fill=0, border=1)
        self.ln(5)
        self.set_font('DejaVuSans', '', 14)

    def addBulletList(self, references: set):
        '''
        adds a list as bullet points in the pdf
        '''
        self.set_font('DejaVuSans', 'U', 14)
        for url in references:

            self.multi_cell(0, 6, f'\u2022{url}', ln=True)
            self.ln(4)
        self.set_font('DejaVuSans', '', 14)


def generate_report(filename: str, plagIndex: float, results: dict[str, str], wordCount: int, charCount: int, downloadFolder: str) -> None:
    '''
    create a pdf only if more than 10 words are present
    '''

    if (wordCount >= 10):

        # stores the number of sources from which plagiarism was detected
        instancesOfPlagiarism: int = 0
        references = set() # A set of all urls in dict
        # pdf = an object of PDF class thta'll be used to create the report
        pdf = PDF(orientation='P', unit='mm', format='A4')
        # getting a unicode font for universal use
        current_path = os.path.dirname(__file__)
        pdf.add_font('DejaVuSans','',f'{current_path}/DejaVuSans.ttf', uni=True)

    # creating a set of all references to be added as a list at the end of report
        x = 0
        for phrase in results:
            '''
            makes a set of references present in dict -> references:str
            and their count -> instancesOfPlagiarism
            '''
            if results[phrase] != '' :
                references.add(results[phrase])
            instancesOfPlagiarism = len(references)

        # metaData of report.pdf file
        pdf.set_author('Team PlagPatrol')
        pdf.set_title('plagiarism report by PlagPatrol')

        # adding page & setting font
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()
        pdf.set_font('DejaVuSans', '', 22)  # font (font style, bold/U/Italic, size)

        # creating header of first page with logo
        pdf.Addlogo()
        # adding meta data to report
        pdf.metaData(wordCount, instancesOfPlagiarism, plagIndex)
        pdf.ln(10)

        # adding the data in dict passed by web scrapper
        pdf.set_font('DejaVuSans', '', 14)
        phrases = list(results.keys())
        webLinks = list(results.values())
        i = 0
        while i < len(results):

            if webLinks[i] == '':

                textToAdd: str = ''
                while (i < len(webLinks)) and (webLinks[i] == ''):
                    textToAdd += phrases[i]
                    i += 1

                pdf.addNormally(textToAdd)
            else:
                pdf.addHighlighted(phrases[i], webLinks[i])
                i += 1

        # adding a refernce list at the end
        pdf.add_page()
        pdf.set_font('times', 'BU', 20)
        pdf.cell(0,20,"References",align='C',ln=True)
        pdf.addBulletList(references)

        # output the report
        os.chdir(downloadFolder)#specifies which directory to create the report.pdf in
        print(downloadFolder)
        filename = f'{downloadFolder}/{filename}_plagiarism_report.pdf'
        pdf.output(filename)
        print('report created')
        #os.path.remove(filename)#to delete the og file
        return filename
