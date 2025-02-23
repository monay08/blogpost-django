def test_addition():
    assert 1 + 1 == 2

def test_subtraction():
    assert 5 - 3 == 2

def test_multiplication():
    assert 3 * 4 == 12

def test_division():
    assert 10 / 2 == 5

def test_string_concatenation():
    assert "Hello " + "World" == "Hello World"

def test_list_append():
    my_list = [1, 2, 3]
    my_list.append(4)
    assert my_list == [1, 2, 3, 4]