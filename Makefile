CC=g++
CFLAGS=-c -Wall
LDFLAGS=
SOURCES=src/main.cpp src/bronnen/Bron.cpp src/bronnen/Afval.cpp
OBJECTS=$(SOURCES:.cpp=.o)
EXECUTABLE=Goedemorgen

all: $(SOURCES) $(EXECUTABLE)
	
$(EXECUTABLE): $(OBJECTS) 
	$(CC) $(LDFLAGS) $(OBJECTS) -o $@

.cpp.o:
	$(CC) $(CFLAGS) $< -o $@


#all:
#	g++ src/main.cpp src/Transactie.cpp src/ExportLocator.cpp -o importer