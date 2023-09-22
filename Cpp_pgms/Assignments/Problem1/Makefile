# Define the C++ compiler and compiler flags
CXX = g++
CXXFLAGS = -std=c++11 -Wall

# Define the target executables and their corresponding source files
TARGET1 = testList
SOURCE1 = List.cc testList.cc

TARGET2 = Lex
SOURCE2 = Lex.cc List.cc

# Define a common rule to build C++ source files into executables
all: $(TARGET1) $(TARGET2)

$(TARGET1): $(SOURCE1)
	$(CXX) $(CXXFLAGS) -o $(TARGET1) $(SOURCE1)

$(TARGET2): $(SOURCE2)
	$(CXX) $(CXXFLAGS) -o $(TARGET2) $(SOURCE2)

# Define a rule to clean up object files and executables
clean:
	rm -f $(TARGET1) $(TARGET2)

# Specify that 'clean' is not a file target
.PHONY: clean