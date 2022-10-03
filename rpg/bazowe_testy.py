def add(a, b):
    return a + b

def test_add_00():
    assert add(0,0) == 0

def test_add_01():
    assert add(0,1) == 1

def test_add_11():
    assert add(1,1) == 4

def test_add_22():
    assert add(2,2) == 4