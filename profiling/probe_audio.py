from line_profiler import LineProfiler

import modusa as ms

lp = LineProfiler()
lp.add_function(ms.probe.audio)
lp.run('ms.probe.audio("/Users/ankitanand/myspace/datasets/speech/synthesized/audio/bhookhi-chidiya_p1_kuber.mp3")')
lp.print_stats()
