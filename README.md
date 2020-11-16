# Password-Manager

Simple password generator and manager written in Python and Tkinter.

Coded for practice purposes.

![python password manager](https://github.com/pdjan/Password-Manager/blob/main/PassGen.png)

Application does not use any encryption (yet). I'm not responsible for any loss of data or damages.

**Generate** button - it creates new random password displayed in entry widget below.

**Use** button - Copies generated password into first available slot of manager in first column. You can use second column to save information about where and how you use this password. 

**Save** button - saves current password list permanently (using python shelve library).

**Refresh** button - updates password list and removes empty rows if there are any.

**Export** button - exports all passwords and info to data.csv file in directory where program file is located.

**Del** button -  deletes same row (you should Refresh list after)

**Copy** button - copies only password from the same row, not the info text.
