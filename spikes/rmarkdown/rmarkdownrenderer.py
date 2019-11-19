import subprocess
import os

class RMarkdownRenderer():
    def __init__(self):
        self.msg_error = "There was an error calling Rscript or rmarkdown::render on the lesson."
        self.is_rmarkdown = False
        self.had_comp_error = False
        self.log = ""

    def render(self,lesson_name,lesson_string):
        if self.should_compile(lesson_name,lesson_string):
            self.is_rmarkdown = True
            return self.compile_rmarkdown(lesson_name,lesson_string[lesson_string.find('\n')+1:])
        else:
            return lesson_string

    # check to see if the lesson is rmarkdown and should be compiled to html
    # and return true or false
    def should_compile(self,lesson_name,lesson_string):
        line_end = lesson_string.find('\n')
        line = lesson_string[0:line_end]
        return (line == "rmarkdown")

    # compile lesson_string into html using Rscript and rmarkdown.
    # ToDo: consider os.chdir(/some/specific/directory/to/store/these)
    def compile_rmarkdown(self,lesson_name,lesson_string):
        html = ""
        rmd_file_name = lesson_name+".rmd"
        outfile = lesson_name+".html"
        cmd = ["Rscript", "-e", "rmarkdown::render(\'"+rmd_file_name+"\')"]
        done_process = None

        # Write lesson_string to .rmd file
        with open(rmd_file_name,"w") as f:
            f.write(lesson_string)

        # default out file for rmarkdown::render is <lesson_name>.html
        done_process = subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        
        if done_process.returncode:
            self.had_comp_error = True
            self.log += self.msg_error
        else:
            # get all html code into a string
            with open(outfile,"r") as f:
                for line in f:
                    html += line

        self.log += done_process.stdout.decode("utf-8")
        return html

