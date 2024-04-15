import random as rd


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
                tmp = self.current_status[i]^tmp # `^` is a XOR
        
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
        Returns: Check if there is a cycle before 2^n - 1 iterations
        """
        # check duplicates
        old_last_output = self.last_output # we have to back up this
        start = self.current_status.copy()
        for i in range(2**len(self.initial_status) - 2): # First one is included
            self.next_status()
            if self.current_status == start:
                print("There is a duplicate at iteration number",i+1)
                print("start:", start)
                print("xor_list:", self.xor_list)
                print("current_status", self.current_status)
                # reset status
                self.last_output = old_last_output
                self.current_status = start.copy()
                self.nb_iteration -= i
                return False
        # reset status
        self.last_output = old_last_output
        self.current_status = start.copy()
        self.nb_iteration -= i
        return True


class CSS:
    def __init__(self, lfsr1, lfsr2):
        self.lfsr1 = lfsr1
        self.lfsr2 = lfsr2
        self.c = 0
    
    
    def reset(self):
        self.lfsr1.reset()
        self.lfsr2.reset()
        self.c = 0

    def encode(self, m):
        """
        `m` must be a string composed by numbers in hexadecimal (0<m<ff)
        AND len(m) must be even
        -
        Note: This function is very close of the algo that our teacher gave us.
        """
        s = ""
        for i in range(len(m)//2):
            x = ""
            for el in reversed([self.lfsr1.next_status() for _ in range(8)]):
                x += str(el)
            x = int(x, 2) 
            y = ""
            for el in reversed([self.lfsr2.next_status() for _ in range(8)]):
                y += str(el)
            y = int(y, 2)

            res = (x+y+self.c)%256
            tmp = int(m[2*i]+m[2*i+1], 16)
            s += hex(tmp^res)[2:]

            self.c = 1 if x+y>255 else 0
        self.reset()
        return s
    
    def decode(self, c):
        # It's symmetrical
        return self.encode(c)



######### TESTINT PART

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
    start = [0 for _ in range(n)]; start[16]=1; start.reverse()
    xor_list = [0 for _ in range(n)]; xor_list[14]=1; xor_list.reverse();xor_list.pop()

    l = LFSR(start, xor_list) 
    l.check_duplicates()

def test2():
    """
    Example for an LFSR of 25 bits.
    This may take even more time than for 17 bits.
    """
    n = 25
    start = [0 for _ in range(n)]; start[24]=1; start.reverse()
    xor_list = [0 for _ in range(n)]; xor_list[12]=1; xor_list[4]=1; xor_list[3]=1
    xor_list.reverse();xor_list.pop()

    l = LFSR(start, xor_list) 
    l.check_duplicates()


def test3():
    n = 17
    start = [0 for _ in range(n)]; start[16]=1; start.reverse()
    xor_list = [0 for _ in range(n)]; xor_list[14]=1; xor_list.reverse();xor_list.pop()
    l1 = LFSR(start, xor_list) 

    n = 25
    start = [0 for _ in range(n)]; start[24]=1; start.reverse()
    xor_list = [0 for _ in range(n)]; xor_list[12]=1; xor_list[4]=1; xor_list[3]=1
    xor_list.reverse();xor_list.pop()
    l2 = LFSR(start, xor_list) 

    css = CSS(l1,l2)
    m = "ffffffffff"

    print(f"The message: {m}")

    c = css.encode(m)
    print(f"Encoded message: {c}")
    print(f"Decoding the encoded message: {css.decode(c)}") # verification


if __name__ == "__main__":
    # NOTE : not every LFSR have a "cycle" of 2^n - 1 iterations 

    #test0()
    #test1()
    #test2() # This test may take a bit of time

    test3()
    pass