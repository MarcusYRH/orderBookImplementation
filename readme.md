***Main flow explained***
1) Load entire file into a pandas dataframe
2) Start reading from top-down, and mark records that are read
3) For each row whether buy/sell, check the df for eligible marked records and resolve the order accordingly

***Main assumptions made***:

1) Price/Time priority follows for both buy and sell orders i.e. when a buy order is read in, we check for the most expensive sell order, then take the earliest order with price corresponding to that which we chose, and vice versa.
2) The input file given will demand the top-down flow be respected for judging when an order was placed.
3) I chose Pandas over generic python since my first thought was that Pandas is much faster than generic python with handling very large datasets as it uses numpy under the hood, which is written in c and implements highly efficient array operations. (even when iterating row by row, and I used itertuples to iterate over which I understand is very efficient even compared to a generic for loop over a list/array)
   

***Performance and testability notes***
1) Overall time complexity can be said roughly to be O(N^2) or in smaller datasets, O(N*m) where m is the number of matching records eligible for order resolution. m << N where m is sometimes very much smaller than N
2) This is still very unoptimised since the general rule of thumb in pandas is to avoid iterating row by row. I intend to look up more into pandas methods to find out how I can fully avoid using a for loop.
3) Unit testability is compromised (for me personally) since unit testing in pandas and numpy is less mature than generic python unit testing (using generic data structures like dictionaries for e.g.)
4) Load test results to be shared below

**Partial conclusion**: 

It might be better to instead use a Dictionary since lookup time complexity is O(1) on average and O(N) amortised worse case, so it might be faster to use a Dictionary within a for loop, instead of using Pandas to search for eligible orders per row within a for loop. 

This is because pandas .loc which i used to pull eligible order records per row is on average O(N) in time complexity.


***LOAD TEST RESULTS***

0) 12 records - 0.015823 sec
1) 1000 records - 1.587653 sec
2) 5000 records - 14.673910 sec
3) 10,000 records - 44 sec 
4) 20,000 records - 150 Sec 
