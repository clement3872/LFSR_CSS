import random as rd

def xor(a,b):
    """
    args: a and b must be between 0 and 1
    Returns a xor b
    """
    assert a in (0,1), "xor(a,b): a must be in (0,1)"
    assert b in (0,1), "xor(a,b): b must be in (0,1)"
    return 0 if a==b else max(a,b)

class LFSR:
    def __init__(self, status, xor_list, last_output=None):
        """
        args:
            - status: a list of bits (int of 0 and 1)
            - xor_list: a list of bool, should be the same size of status 
            - last_output: if you have already done an LFSR, you can start at a specific status -> 0 or 1
                          else None
        """
        # some asserts for "security"
        assert len(status)==len(xor_list), "LFSR: len(status) and len(xor_list) should be equal"
        # assert last_output in (None,0,1), "LFSR: last_output should be in (None,0,1)"
        for i in range(len(status)):
            assert status[i] in (0,1), f"LFSR: status[{i}] should be in (0,1)"
            assert xor_list[i] in (False,True), f"LFSR: xor_list[{i}] should be in (0,1)"

        self.start = status
        self.xor_list = xor_list

        self.current_status = status
        self.last_output = last_output
    
    def next_status(self):
        """ Returns the next bit of the LFSR"""
        self.last_output = self.current_status[-1]
        tmp = self.last_output
        for i in range(len(self.xor_list)):
            if xor_list[i]:
                tmp = xor(self.current_status[i], tmp)
        
        # shifting the list
        self.last_output = self.current_status.pop()
        self.current_status = [tmp] + self.current_status

        return self.last_output


if __name__ == "__main__":
    # here is an example of how to use it
    
    start = [1,0,0,1,0,1,1,0]
    xor_list = [False, False, False, True, True, True, False, False]
    
    l = LFSR(start, xor_list)
    for _ in range(8): 
        l.next_status()
        print(l.last_output, l.current_status)
