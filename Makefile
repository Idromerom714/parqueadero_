# Makefile para compilar el módulo de parqueadero

CXX = g++
PYTHON = python3
CXXFLAGS = -O3 -Wall -shared -std=c++11 -fPIC
INCLUDES = $(shell $(PYTHON) -m pybind11 --includes) -Icpp
SUFFIX = $(shell $(PYTHON)-config --extension-suffix)

TARGET = parqueadero_cpp$(SUFFIX)
SOURCES = cpp/parqueadero.cpp cpp/bindings.cpp

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SOURCES) -o $(TARGET)

clean:
	rm -f $(TARGET)

test: $(TARGET)
	$(PYTHON) -c "import parqueadero_cpp; p = parqueadero_cpp.Parqueadero(10, 20); print('Módulo compilado correctamente')"

run: $(TARGET)
	$(PYTHON) app.py

.PHONY: all clean test run