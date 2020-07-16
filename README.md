# pyCsvExtractor
Extractor, modifier of csv files

```shell
usage: pyCsvExtractor.py [-h] -i INPUT [-d [DECIMALPOINT]] [-s [SEPARATOR]]
                         [-df [DATEFORMAT]] [-df2 [DATEFORMAT2]]
                         [-x SYNCHRONIZE_WITH_FILE] [-r REMOVEEQUALTO] [-rms]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input .csv file
  -d [DECIMALPOINT], --decimalpoint [DECIMALPOINT]
                        Data CSV separator
  -s [SEPARATOR], --separator [SEPARATOR]
                        Data CSV separator
  -df [DATEFORMAT], --dateformat [DATEFORMAT]
                        Data time format
  -df2 [DATEFORMAT2], --dateformat2 [DATEFORMAT2]
                        Data time format
  -x SYNCHRONIZE_WITH_FILE, --synchronize-with-file SYNCHRONIZE_WITH_FILE
                        Synchronize timestamps with file
  -r REMOVEEQUALTO, --removeEqualTo REMOVEEQUALTO
                        Remove all elements equal to.
  -rms, --removems      Remove miliseconds from all datetime fields.

```
