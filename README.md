# PyRarCrack
Bruteforce attack for .rar using unrar

```
usage: pyrarcrack.py [-h] [--start START] [--stop STOP] [--verbose VERBOSE]
                     [--alphabet ALPHABET] [--file FILE]

Python combination generator to unrar

optional arguments:
  -h, --help                Show this help message and exit
  --start START             Number of characters of the initial string [1 -> "a", 2-> "aa"]
  --stop STOP               Number of characters of the final string [3 -> "ßßß"]
  --verbose VERBOSE         Show combintations
  --alphabet ALPHABET       Alternative chars to combinations
  --file FILE               .rar file [file.rar]
  --unrar_path UNRAR_PATH   Defines the path to the unrar executable, defaulting to the value from environment variables
  --unrar_lang UNRAR_LANG   Specifies the language for unrar messages, which is necessary to detect when an operation is successful. ['eng'/'pt-br']
```


#### Example

```
$ python pyrarcrack.py --start 10 --stop 10 --file example_path.rar --alphabet 1234567890

Password found: 1234567890
Time: 0.06715750694274902
```
