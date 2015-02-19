# LM317 Calculator ver. 1.0
### Author: Maciej Kopeć
Simple LM317 voltage regulator calculator which can give the voltage value with given resistors or scan a resistor series to find combination that gives the closest nominal voltages. The calculator takes into account the adjustment current (assumed 100 uA).

To use this calculator just run `python LM317_calc.py` - no shebang.
The app can be run with the following options:
- `-s e96` or `--series=e96` - causes app to search for resistors in e96 value series. Series values are located in `*.txt` files in the same folders. The file has to be named with the series name that is desired to be used in the app, so to use calc with option `-s e123` file needs to be named `e123.txt`. Files are whitespace separated, whitespace count does not matter. Default value is e24.
- `-p 1` or `--precision=1` - gives the precision (in percent) with which minimum and maximum resistor values are counted. This is used further to count the lowest and highest possible voltage. Default value is 5.
- `-v 3.3` or `--voltage=3.3` - gives the app the desired voltage (in volts) to look for. Default value is 5.
- `-t` - makes the app to display the results in a table. This won't work if there is not `terminaltables` installed. App running without that option will display results as plain text.
- `--R1=100` and `--R2=250` - gives the values of the resistors to calculate output voltage for. Giving at least one of the values overwrites sweeping mode (only one voltage for given resistors will be counted if at least one resistance is given). It works with `-p` and `-t`, other options are ignored. Default values are 0 so if you give only one, the other is treated as 0.
