CC = g++
CFLAGS = -g -std=c++11
INCLUDES = -I../Problem1
SRC_DIR = ../Problem1
SRCS = Graph.cc GraphTest.cc $(SRC_DIR)/List.cc
TARGET = GraphTest

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(INCLUDES) $^ -o $@

clean:
	rm -f $(TARGET)

.PHONY: all clean