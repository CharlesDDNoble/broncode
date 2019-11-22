import subprocess
import os

class RMarkdownRenderer():
    def __init__(self):
        self.msg_error = "There was an error calling Rscript or rmarkdown::render on the lesson."
        self.is_rmarkdown = False
        self.had_comp_error = False
        self.log = ""

    # compile lesson_string into html using Rscript and rmarkdown.
    # ToDo: consider os.chdir(/some/specific/directory/to/store/these)
    def render(self,lesson_name,lesson_string):
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

        # cleanup
        if os.path.exists(rmd_file_name):
            os.remove(rmd_file_name)

        if os.path.exists(outfile):
            os.remove(outfile)

        return html

