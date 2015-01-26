## What do these scripts do and how?

This is a set of scripts that cooperate to test the claim that all even solutions to
the P1xP1 diophantine equation can be obtained by Seiberg dual operation on the P1xP1 adjacency matrix.

Firstly, we use "**adjacency_p1xp1.py**" to generate a database that contains a large amount of edge number combinations that are obtained from Seiberg duality. The results are store in a text file named "**solutions.txt**". Next, we use "**diophantine_p1xp1.py**" to generate all even solutions with values within certain range and the results are stored in a file named "**database.txt**". Lastly we use "**check.py**" to test that all solutions form a subset of the database. If there are any exceptions that do not fall into the database, they will be stored in a file named "**exceptions.txt**". Fortunately, there are none, at least in those we have checked.

## License

This project is licensed under the terms of the MIT license.