CC = gcc
CFLAGS_COMMON = -Wall -Wextra
CFLAGS_SLOW = $(CFLAGS_COMMON) -O0 -g
CFLAGS_FAST = $(CFLAGS_COMMON) -O3 -mavx2 -g

all: prog_slow prog_fast

prog_slow: src/matrix.c
	$(CC) $(CFLAGS_SLOW) src/matrix.c -o prog_slow

prog_fast: src/matrix_opt.c
	$(CC) $(CFLAGS_FAST) src/matrix_opt.c -o prog_fast

clean:
	rm -f prog_slow prog_fast perf.data*
