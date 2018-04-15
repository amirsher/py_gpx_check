checking .gpx files for speeding on restricted segments and electronic marshaling.
Built in python with [gpxpy](https://github.com/tkrajina/gpxpy).

[pyqt_tabed.py](https://github.com/amirsher/py_gpx_check/blob/master/pyqt_tabed.py) is a GUI built on [pyqt5](https://pypi.python.org/pypi/PyQt5).

Accept lat/long in decimal (30.1749997,35.0642141) or min/sec (29.58.42.516,34.56.03.523) without N S E W

If .gpx file contain more the 1 segment, use [split_gpx_to_segments.py](https://github.com/amirsher/py_gpx_check/blob/master/split_gpx_to_segments.py) to split to individual files, otherwise the result will be currupt. 

### Speeding ###

Check all the .gpx files in the folder and producing a report of speeding in the restricted segments. can have as many segments as needed.

accept lat/long of strating point, lat/long of finish point and restricted speed.

NOT accepting waypoints gpx file.

run: python speeding.py 45.49222,5.90380 45.49885,5.90372 70 45.49222,5.90380 45.49885,5.90372 65

see [spedding_results.txt](https://github.com/amirsher/py_gpx_check/blob/master/spedding_results.txt) for sample report.

### Marshaling ###

Check all the .gpx files in the folder and producing a report of electronic marshaling. can have as many marshals as needed.

accepts lat/long for each marshal.

accepts waypoints gpx file.

run: python marshaling.py 45.48612,5.909551 45.49593,5.90369 45.50341,5.90479 45.51386,5.90625

see [marshaling_results.txt](https://github.com/amirsher/py_gpx_check/blob/master/marshaling_results.txt) for sample report.

### Track Ploting and Web Map ###

Added ploting of the tracks using [matplotlib](https://matplotlib.org/), and displaying on a web page


for sample reports see:

"line"
![speeding line](https://github.com/amirsher/py_gpx_check/blob/master/line.png)
[SpeedingMap.html](https://github.com/amirsher/py_gpx_check/blob/master/SpeedingMap.html)

"points"
![speeding points](https://github.com/amirsher/py_gpx_check/blob/master/points.png)

"marshaling"
![marshal point](https://github.com/amirsher/py_gpx_check/blob/master/marshal.png)
[TrackingMap.html](https://github.com/amirsher/py_gpx_check/blob/master/TrackingMap.html)

plot
![marshal point](https://github.com/amirsher/py_gpx_check/blob/master/tracking.png)


