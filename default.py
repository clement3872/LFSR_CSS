import random as rd

def xor(a,b):
    """
    args: a and b must be between 0 and 1
    Returns: a xor b
    """
    assert a in (0,1), "xor(a,b): a must be in (0,1)"
    assert b in (0,1), "xor(a,b): b must be in (0,1)"
    return (a+b)%2

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
        assert 1 in status, "There should be a 1 in the list `status`"
        assert len(status)==len(xor_list)+1, "LFSR: len(status) == len(xor_list)+1 should be true"
        # assert last_output in (None,0,1), "LFSR: last_output should be in (None,0,1)"
        for i in range(len(status)-1): 
            assert status[i] in (0,1), f"LFSR: status[{i}] should be in (0,1)"
            assert xor_list[i] in (False,True), f"LFSR: xor_list[{i}] should be in (0,1)"
        assert status[-1] in (0,1), f"LFSR: status[{len(status)}] should be in (0,1)"

        self.initial_status = status.copy()
        self.xor_list = xor_list.copy()

        self.current_status = status.copy()
        self.last_output = last_output
        self.nb_iteration = 0
    
    def next_status(self):
        """Returns the next bit of the LFSR"""
        self.last_output = self.current_status[-1]
        tmp = self.last_output
        for i in range(len(self.xor_list)):
            if self.xor_list[i] == 1:
                tmp = xor(self.current_status[i], tmp)
        
        # shifting the list
        self.last_output = self.current_status.pop()
        self.current_status = [tmp] + self.current_status
        self.nb_iteration += 1

        return self.last_output
    
    def reset(self):
        self.current_status = self.initial_status.copy()
        self.last_output = None
        self.nb_iteration = 0
    
    def check_duplicates(self):
        """
        Returns: Check if there are different values during the 2^n - 1 iterations
        """
        # check duplicates
        old_last_output = self.last_output # we have to back up this
        start = self.current_status.copy()
        l_iterations = []
        for i in range(2**len(self.initial_status) - 1):
            self.next_status()
            if self.current_status in l_iterations:
                print("There is a duplicate at iteration number",i+1)
                print("start:", start)
                print("xor_list:", self.xor_list)
                print("current_status", self.current_status)
                # reset status
                self.last_output = old_last_output
                self.current_status = start.copy()
                self.nb_iteration -= i
                return False
            else:
                l_iterations.append(self.current_status.copy())
        # reset status
        self.last_output = old_last_output
        self.current_status = start.copy()
        self.nb_iteration -= i
        return True

    


def test0():
    # First example from the PDF (on 8 bits)

    start = [1,0,0,1,0,1,1,0]
    xor_list = [0,0,0,1,1,1,0]
    l = LFSR(start, xor_list)
    l.check_duplicates()


def test1():
    """
    Example for an LFSR of 17 bits.
    This may take a bit of time.
    """
    n = 17
    start = [rd.randint(0,1) for _ in range(n)]
    while 1 not in start: start = [rd.randint(0,1) for _ in range(n)]
    xor_list = [rd.randint(0,1) for _ in range(n-1)]
    while True not in xor_list: xor_list = [rd.randint(0,1) for _ in range(n-1)]

    l = LFSR(start, xor_list) 
    l.check_duplicates()

def test2():
    """
    Example for an LFSR of 25 bits.
    This may take even more time than for 17 bits.
    """
    n = 25
    start = [rd.randint(0,1) for _ in range(n)]
    while 1 not in start: start = [rd.randint(0,1) for _ in range(n)]
    xor_list = [rd.randint(0,1) for _ in range(n-1)]
    while True not in xor_list: xor_list = [rd.randint(0,1) for _ in range(n-1)]

    l = LFSR(start, xor_list) 
    l.check_duplicates()



if __name__ == "__main__":
    # NOTE : not every LFSR have a "cycle" of 2^n - 1 iterations 

    # test0()
    # test1() # This test may take a bit of time
    # test2() # This will take even more time
    pass