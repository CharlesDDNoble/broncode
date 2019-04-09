Components that may be used in our project frontend using template includes

-InstructionsComponent.html
Uses the block "instructions"
In your view, store the instructions in the variable "instructions" formatted in markdown

-CodeMirrorComponent.html
Uses a POST form 
	flags can be caught in a view request under the key "compileFlags"
	code can be caught in a view request under the key "codearea"
Uses the block "codemirror"
Store default flags in variable "defaultFlags"
Store default code text in variable "codeText"

-OutputConsole.html
Uses the block "outputConsole"
In your view, store the output results in the variable "testResult" formatted in markdown
