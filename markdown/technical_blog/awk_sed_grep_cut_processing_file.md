

# awk
* `awk '/pattern/ {print $1}'`
This line of code will print out the first column of the line that contain the pattern in the file.
The idea is you want to do something on the line that contain the pattern. Inside the `{}` is the action you want to do. $columns is which column you want to edit on.

* `awk -F"=" '{print $NF}' inputfile > outputfile`

# sed
Some actions: `d` means delete, `p` means print, `s` means substitution. In order to check if the command is right, use `ed` for testing.
* `g/regular/d` represent deleting all the lines that contain "regular" globally(putting g at the beginning means search for the whole context)
* `[address]s/pattern/replacement/flag` [address] means which line you want to substitute, s means substitution, pattern means the line that match the pattern, replacement means the string you want to substitute with and flag means how you want deal with for the line in the address that you specified.
  * `s/regular/complex/` means replace regular with complex in the current line.
  * `s/regular/complex/g` means globally.
  * `/regular/s/regular/complex/g` means replace all regular with complex for the first line that matches the pattern which is containing the regular.
  * `g/regular/s/regular/complex/g` is an extension for the previous line meaning for every line instead for the first line(the first g is global of the whole file, the second is global in the line).
  * `grep` is short for `g/re/p`
In a nut shell,  
For `substitution`: [flag/line pattern/s/word pattern/replacement/flag] if the word pattern is the same as the line pattern, then you can just use //.  
For `print`: [g/line pattern/p]

`sed -f scriptfile inputfile`

`sed 's/^.*sum=//' inpufile > outputfile`

#### 3 ways of executing several command at a time from the terminal
* use ";" to separate the commands:
```
sed ’s/ MA/, Massachusetts/; s/ PA/, Pennsylvania/’ filename
```
* Precede each instruction by -e:
```
sed -e ’s/ MA/, Massachusetts/’ -e ’s/ PA/, Pennsylvania/’ filename
```
* press enter after the first single quote:
```
$ sed ’
> s/ MA/, Massachusetts/
> s/ PA/, Pennsylvania/
> s/ CA/, California/’ list
```
> remember this won't change the result input file but just displaying on the screen.

#### executing sed script
`sed -f scriptfile file`



# grep
