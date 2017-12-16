checking .gpx files for speeding on restricted segments and electronic marshaling.
Built in python with [gpxpy](https://github.com/tkrajina/gpxpy).

### Speeding ###

Check all the .gpx files in the folder and producing a report of speeding in the restricted segments. can have as many segments as needed.

accept lat/long of strating point, lat/long of finish point and restricted speed.

run: python rally_speeding_folder.py 45.49222,5.90380 45.49885,5.90372 70 45.49222,5.90380 45.49885,5.90372 65

see [zzz_spedding_results.txt](https://github.com/amirsher/py_gpx_check/blob/master/zzz_spedding_results.txt) for sample report.

### Marshaling ###

Check all the .gpx files in the folder and producing a report of electronic marshaling. can have as many marshals as needed.

accept lat/long for each marshal.

run: python rally_marshal_folder.py 45.48612,5.909551 45.49593,5.90369 45.50341,5.90479 45.51386,5.90625

see [zzz_marshal_results.txt](https://github.com/amirsher/py_gpx_check/blob/master/zzz_marshal_results.txt) for sample report.

### Track Ploting ###

Added ploting of the tracks using [matplotlib](https://matplotlib.org/)

[zzz_marshal_plot_results.txt](https://github.com/amirsher/py_gpx_check/blob/master/zzz_marshal_plot_results.txt)
