CC = gcc

all: compilador

lab.tab.c lab.tab.h: lab.y compilador.h
	bison -d lab.y

lex.yy.c: lab.l lab.tab.h compilador.h
	flex lab.l

compilador: lab.tab.c lex.yy.c
	$(CC) -Wall -o compilador lab.tab.c lex.yy.c

clean:
	rm -f compilador lab.tab.c lab.tab.h lex.yy.c
