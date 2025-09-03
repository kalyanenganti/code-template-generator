# -*- coding: utf-8 -*-
"""
Created on Wed Sep  3 15:58:23 2025

@author: kalyane
"""

import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main
from main import (
    Signature,
    Parameter,
    generate_python_template,
    generate_java_template,
    generate_cpp_template,
    generate_javascript_template,
)

# Fixture for syrupy snapshots (automatically handles .ambr files)
@pytest.fixture
def snapshot(snapshot):
    return snapshot

# Scenario 1: Single primitive input - Fibonacci(n: int) -> int
def test_fibonacci_python(snapshot):
    sig = Signature(
        function_name="fib",
        parameters=[Parameter(name="n", type="int")],
        returns={"type": "int"},
    )
    template = generate_python_template(sig)
    assert snapshot == template

def test_fibonacci_java(snapshot):
    sig = Signature(
        function_name="fib",
        parameters=[Parameter(name="n", type="int")],
        returns={"type": "int"},
    )
    template = generate_java_template(sig)
    assert snapshot == template

def test_fibonacci_cpp(snapshot):
    sig = Signature(
        function_name="fib",
        parameters=[Parameter(name="n", type="int")],
        returns={"type": "int"},
    )
    template = generate_cpp_template(sig)
    assert snapshot == template

def test_fibonacci_javascript(snapshot):
    sig = Signature(
        function_name="fib",
        parameters=[Parameter(name="n", type="int")],
        returns={"type": "int"},
    )
    template = generate_javascript_template(sig)
    assert snapshot == template

# Scenario 2: Multiple mixed inputs - MergeKLists(lists: List[] ) -> List
# Assuming array of linked lists for param
def test_merge_k_lists_python(snapshot):
    sig = Signature(
        function_name="mergeKLists",
        parameters=[Parameter(name="lists", type="List[]")],
        returns={"type": "List"},
    )
    template = generate_python_template(sig)
    assert snapshot == template

def test_merge_k_lists_java(snapshot):
    sig = Signature(
        function_name="mergeKLists",
        parameters=[Parameter(name="lists", type="List[]")],
        returns={"type": "List"},
    )
    template = generate_java_template(sig)
    assert snapshot == template

def test_merge_k_lists_cpp(snapshot):
    sig = Signature(
        function_name="mergeKLists",
        parameters=[Parameter(name="lists", type="List[]")],
        returns={"type": "List"},
    )
    template = generate_cpp_template(sig)
    assert snapshot == template

def test_merge_k_lists_javascript(snapshot):
    sig = Signature(
        function_name="mergeKLists",
        parameters=[Parameter(name="lists", type="List[]")],
        returns={"type": "List"},
    )
    template = generate_javascript_template(sig)
    assert snapshot == template

# Scenario 3: Custom object & multiple returns - LowestCommonAncestor(root: Tree, p: Tree, q: Tree) -> Tree
# Note: "multiple returns" in spec might be a typo, as schema has single return; testing as-is
def test_lowest_common_ancestor_python(snapshot):
    sig = Signature(
        function_name="lowestCommonAncestor",
        parameters=[
            Parameter(name="root", type="Tree"),
            Parameter(name="p", type="Tree"),
            Parameter(name="q", type="Tree"),
        ],
        returns={"type": "Tree"},
    )
    template = generate_python_template(sig)
    assert snapshot == template

def test_lowest_common_ancestor_java(snapshot):
    sig = Signature(
        function_name="lowestCommonAncestor",
        parameters=[
            Parameter(name="root", type="Tree"),
            Parameter(name="p", type="Tree"),
            Parameter(name="q", type="Tree"),
        ],
        returns={"type": "Tree"},
    )
    template = generate_java_template(sig)
    assert snapshot == template

def test_lowest_common_ancestor_cpp(snapshot):
    sig = Signature(
        function_name="lowestCommonAncestor",
        parameters=[
            Parameter(name="root", type="Tree"),
            Parameter(name="p", type="Tree"),
            Parameter(name="q", type="Tree"),
        ],
        returns={"type": "Tree"},
    )
    template = generate_cpp_template(sig)
    assert snapshot == template

def test_lowest_common_ancestor_javascript(snapshot):
    sig = Signature(
        function_name="lowestCommonAncestor",
        parameters=[
            Parameter(name="root", type="Tree"),
            Parameter(name="p", type="Tree"),
            Parameter(name="q", type="Tree"),
        ],
        returns={"type": "Tree"},
    )
    template = generate_javascript_template(sig)
    assert snapshot == template

# Scenario 4: Graph input - DetectCycle(graph: Graph) -> bool
def test_detect_cycle_python(snapshot):
    sig = Signature(
        function_name="detectCycle",
        parameters=[Parameter(name="graph", type="Graph")],
        returns={"type": "bool"},
    )
    template = generate_python_template(sig)
    assert snapshot == template

def test_detect_cycle_java(snapshot):
    sig = Signature(
        function_name="detectCycle",
        parameters=[Parameter(name="graph", type="Graph")],
        returns={"type": "bool"},
    )
    template = generate_java_template(sig)
    assert snapshot == template

def test_detect_cycle_cpp(snapshot):
    sig = Signature(
        function_name="detectCycle",
        parameters=[Parameter(name="graph", type="Graph")],
        returns={"type": "bool"},
    )
    template = generate_cpp_template(sig)
    assert snapshot == template

def test_detect_cycle_javascript(snapshot):
    sig = Signature(
        function_name="detectCycle",
        parameters=[Parameter(name="graph", type="Graph")],
        returns={"type": "bool"},
    )
    template = generate_javascript_template(sig)
    assert snapshot == template