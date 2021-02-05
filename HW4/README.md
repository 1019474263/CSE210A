# HW4: Small step WHILE

---

#### Requirement:

run `pip install lark-parser --upgrade` to install `lark`, which is a parsing library I used.

#### How to run:

`python3` is needed to run the file. `Makefile` generates an executable called `while-ss`, or simply run `python while.py`.

#### The custom test cases are in the file [hard.bats](cse210A-asgtest-hw2-while/tests/hard.bats)

There's a bug with the code, that plus/minus has the same precedence as mul/div. I tried to fix that but it seems to take to many changes. For my structure, I'll need to add an extra layer used to determine if it is plus/minus or mul/div. So I decided not to do that.