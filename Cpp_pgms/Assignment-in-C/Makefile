CC = gcc
CFLAGS = -g -std=c17 -Wall

SOURCE1 = Lex.c List.c
SOURCE2 = ListTest.c List.c

OBJ1 = $(SOURCE1:.c=.o)
OBJ2 = $(SOURCE2:.c=.o)

OUTPUT1 = Lex
OUTPUT2 = ListTest

all: $(OUTPUT1) $(OUTPUT2)

$(OUTPUT1): $(SOURCE1)
	$(CC) $(CFLAGS) -o $(OUTPUT1) $(SOURCE1)

$(OUTPUT2): $(SOURCE2)
	$(CC) $(CFLAGS) -o $(OUTPUT2) $(SOURCE2)

clean:
	rm -f $(OBJ1) $(OBJ2) $(OUTPUT1) $(OUTPUT2)