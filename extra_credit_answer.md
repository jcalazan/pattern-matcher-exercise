Extra Credit
============

Since I'm using a nested for loop (to iterate through the paths, then iterating through the patterns to find a match for each path), the algorithmic complexity is O(n^2).

As the inputs increase, the program will run noticeably slower, and will hit a point where it would run very slow.

When given hundreds of thousands of patterns and paths, my program probably won't scale.  A faster solution is to run the pattern matching in parallel.

For example, since the pattern matching for each path can be ran independently, we can spawn a process for each path to find a match and combine the results when finished.  This way, there's no need to wait for each path to find a match before going to the next.

Another possible solution is, for each path, split the list of patterns into smaller chunks and spawn multiple threads, assigning a smaller subset of patterns to each thread.  If a worker thread finds an exact match, notify the master thread, print out the result, and go to the next one.  If multiple possible wildcard matches are found, we'll need to wait for all worker threads to finish and figure out the best match.  Since we know the number of inputs, we can try and divide the work as evenly as we can to minimize waiting.
