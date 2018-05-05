def raiser():
    raise "ERR"

def test():
    try:
        return raiser()
    except:
        print("err")
    else:
        print("else")
    finally:
        print("fin")

print(test())
