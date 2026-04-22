## LessScary 🟢

LessScary is a simple Python tool that turns confusing error messages into clear explanations with fixes.

### 🚀 How to use

1. Download `LessScary.py`
2. Put it in the same folder as your Python file
3. Add these 2 lines at the top of your code:

`import LessScary`   
`LessScary.activate()`

4. Run your code

#### 💡 Example error:  
`5 + "hello"`
##### Python says:  
`TypeError: unsupported operand type(s) for +: 'int' and 'str'`  

##### LessScary says:  
`❌ You are trying to combine a whole number and text.`  
`💡 Fix: convert them to the same type before combining them`

#### ⚠️ Notes
- Works best in Spyder
- In Spyder, use **Run Selection (F9)** for best results
- This is an early version - Some syntax and indentation errors may not be caught yet

#### Feedback
Suggestions and improvements are welcome!  
📧 prana.n88@gmail.com
