from rmarkdownrenderer import RMarkdownRenderer

def main():
    name1 = "NoRmarkdownLesson"
    lesson_string1 ="\n" \
                    "### This is a paragraph in  with some *generic* markdown.\n" \
                    "\n" \
                    "Below is a **code** chunk:\n" \
                    "\n" \
                    "```r\n" \
                    "fit = lm(dist ~ speed, data = cars)\n" \
                    "b   = coef(fit)\n" \
                    "plot(cars)\n" \
                    "abline(fit)\n" \
                    "```\n" \
                    "\n" \
                    "The slope of the regression is `r b[1]`.\n" \
                    "\n" \
                    "```r\n" \
                    "mtcars\n" \
                    "```\n"

    name2 = "RmarkdownLesson"
    lesson_string2 = "rmarkdown\n" \
                    "---\n" \
                    "title: Hello R Markdown\n" \
                    "author: Awesome Me\n" \
                    "date: 2018-02-14\n" \
                    "output: html_document\n" \
                    "---\n" \
                    "\n" \
                    "This is a paragraph in an R Markdown document.\n" \
                    "\n" \
                    "Below is a code chunk:\n" \
                    "\n" \
                    "```{r}\n" \
                    "fit = lm(dist ~ speed, data = cars)\n" \
                    "b   = coef(fit)\n" \
                    "plot(cars)\n" \
                    "abline(fit)\n" \
                    "```\n" \
                    "\n" \
                    "The slope of the regression is `r b[1]`.\n" \
                    "\n" \
                    "```{r}\n" \
                    "mtcars\n" \
                    "```\n" 

    name3 = "ErrorTest"
    lesson_string3 =    "rmarkdown\n" \
                        "```{r}\n" \
                        "i <- 1000\n" \
                        "i/nonDeclaredNumber\n" \
                        "```\n"

    # should print only the given lesson string
    renderer = RMarkdownRenderer()
    lesson = renderer.render(name1,lesson_string1)
    if renderer.had_comp_error:
        print(renderer.log)
    else:
        print(lesson)

    print("\n")

    # should print html
    renderer = RMarkdownRenderer()
    lesson = renderer.render(name2,lesson_string2)
    if renderer.had_comp_error:
        print(renderer.log)
    else:
        print(lesson)

    print("\n")

    # should have error
    renderer = RMarkdownRenderer()
    lesson = renderer.render(name3,lesson_string3)
    if renderer.had_comp_error:
        print(renderer.log)
    else:
        print(lesson)

if __name__ == "__main__":
    main()