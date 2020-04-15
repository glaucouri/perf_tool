# perf_timer
Another performance tool for python


Suppose you have to maintain a complex algorihm or pieces of code stratified in months or years by many developer.
Suppose you have to investigate where some code take more time to execute.
Suppose you have an engine for a complex report that increase running time inexplicably.

Often base profiler cannot be used because it is too much detailed, if you use library as numpy, scipy, pandas it is useless.



Here some production examples

```
task                     |aver(s) |sum(s)  |count   |std     
Definition set value     |   0.006| 111.786|   17199|   0.013
  +-Tmatrix call         |   0.003|   0.043|      13|   0.000
  +-Transition call      |   0.009|  37.078|    4056|   0.009
    +-calculate cache    |   0.018|  36.941|    2016|   0.002
      +-aggregate        |   0.012|  23.772|    2016|   0.002
  +-Staging call         |   0.083|  30.259|     364|   0.031
    +-aggregate          |   0.091|  16.431|     180|   0.011
    +-agg+pivot          |   0.092|  13.200|     144|   0.011
  +-G Loans call         |   0.001|   1.607|    2626|   0.002
  +-Matrix call          |   0.005|   0.061|      13|   0.000
Transition set value     |   1.054|  41.113|      39|   1.497
  +-Transition compute al|   3.163|  41.113|      13|   0.244
    +-Transition tmx     |   0.301|  15.675|      52|   0.014
      +-Broker call      |   0.005|   9.377|    1872|   0.001
        +-Tmatrix call   |   0.003|   6.372|    1872|   0.001
    +-Transition staging |   0.097|   4.650|      48|   0.124
      +-Broker call      |   0.029|   4.220|     144|   0.041
        +-Staging call   |   0.028|   3.985|     144|   0.041
          +-aggregate    |   0.086|   3.851|      45|   0.010
    +-Transition gloans  |   0.056|   2.670|      48|   0.008
      +-Broker call      |   0.003|   1.215|     432|   0.002
        +-G Loans call   |   0.001|   0.522|     432|   0.002
Matrix set value         |   0.665|  17.300|      26|   0.719
  +-Matrix compute all   |   1.441|  17.296|      12|   0.037
    +-call transform     |   0.415|  14.935|      36|   0.019
      +-Broker call      |   0.010|  11.894|    1152|   0.009
        +-Transition call|   0.009|  10.519|    1152|   0.009
          +-calculate cac|   0.018|  10.470|     576|   0.003
            +-agg all    |   0.012|   7.000|     576|   0.002
    +-retrieve data      |   0.003|   0.448|     144|   0.000
```


