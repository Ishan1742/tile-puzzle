==================================
# tile-puzzle
==================================
Search based algorithms to solve a linear tiling puzzle
==================================
### Execution
==================================
- Install python virutal environment package
```bash
$ sudo pip3 install pipenv
```
- Go inside the project folder and Install the dependencies
```bash
$ cd tile-puzzle/
$ pipenv install
```
- Run the virtual environment and execute the code
```bash
$ pipenv shell
$ python3 main.py
```
- Remove the virtual environment
```bash
$ pipenv --rm
```

==================================
### Input Format
==================================
- Input is a string indicating the start state.
- Example input "B_BBWWW".
- The B implies Black Tiles.
- The W implies White Tiles.
- The _ implies the space.
==================================
### Output
==================================
- Relevant outputs are shown in the console.
- There is a log file which stores outputs for all the runs. "output.log".
- To see the data of every node that is being explored. Replace "level=logging.INFO" to "level=logging.DEBUG" in main.py. The output.log file will now contain every node that is explored with the f g h values.
- There is a graph which is plotted during execution and is stored as "output.png".