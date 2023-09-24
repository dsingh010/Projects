CC = g++
CFLAGS = -g -std=c++11
INCLUDES = -I../Problem1
SRC_DIR = ../Problem1
SRCS = FindPath.cc $(SRC_DIR)/List.cc
TARGET = FindPath

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(INCLUDES) $^ -o $@

clean:
	rm -f $(TARGET)

.PHONY: all clean