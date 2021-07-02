# WebChecker

[Usage]
1. Add some websites in source.txt
2. Run the program
3. Check target.csv

[Options]
1. TIME_OUT = 5
2. Number of Threads = 200 (maxworkers)

[How it works]
1. It checks two ways(http, https).
2. Because it is I/O bound job, multi-thread is used.
