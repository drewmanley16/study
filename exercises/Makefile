CC  = gcc
CXX = g++
CFLAGS   = -Wall -Wextra -g
CXXFLAGS = -Wall -Wextra -g -std=c++17

TARGETS = \
	01_pointers/pointers \
	02_memory/memory \
	03_structs/structs \
	04_classes/classes \
	05_copy_ctor/copy_ctor \
	06_operator_overload/operators \
	07_templates/templates \
	08_bst/bst \
	09_rbt/rbt \
	10_misc_c/misc

all: $(TARGETS)

01_pointers/pointers: 01_pointers/pointers.c
	$(CC) $(CFLAGS) -o $@ $< -lm

02_memory/memory: 02_memory/memory.c
	$(CC) $(CFLAGS) -o $@ $< -lm

03_structs/structs: 03_structs/structs.c
	$(CC) $(CFLAGS) -o $@ $< -lm

04_classes/classes: 04_classes/classes.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

05_copy_ctor/copy_ctor: 05_copy_ctor/copy_ctor.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

06_operator_overload/operators: 06_operator_overload/operators.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

07_templates/templates: 07_templates/templates.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

08_bst/bst: 08_bst/bst.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

09_rbt/rbt: 09_rbt/rbt.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

10_misc_c/misc: 10_misc_c/misc.c
	$(CC) $(CFLAGS) -o $@ $< -lm

# Run all tests
test: all
	@echo "\n=========================================="
	@echo "  CS 330 Exercise Test Suite"
	@echo "==========================================\n"
	@for t in $(TARGETS); do \
		echo "── $$t ──"; \
		./$$t; \
		echo ""; \
	done

# Run a single exercise, e.g.: make run EX=08_bst/bst
run: $(EX)
	./$(EX)

clean:
	rm -f $(TARGETS)

.PHONY: all test run clean
