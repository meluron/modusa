from line_profiler import LineProfiler

import modusa as ms

lp = LineProfiler()
lp.add_function(ms.load.audio)
lp.run('ms.load.audio("/Users/ankitanand/myspace/meluron/modusa/tests/testdata/audio-formats/sample.mp3", sr=16000, ch=1)')
lp.print_stats()
