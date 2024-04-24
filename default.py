
class LFSR:
    def __init__(self,size, status, xor_list, last_output=None):
        """
        args:
            - status: a string of bits (int of 0 and 1)
            - xor_list: a list (or tuple), indicating where XOR are
            - last_output: if you have already done an LFSR, you can start at a specific status -> 0 or 1
                          else None
        """
        # some asserts for "security"
        assert type(status) is int, "`status` should be of type int (bin)"
        assert status > 0, "There should be a 1 in the list `status`"
        assert type(size) is int and size>=status.bit_count(), "The size is wrong"

        self.size = size-1
        self.initial_status = status
        self.xor_list = []
        for el in xor_list:
            if el != 0:
                self.xor_list.append(el)
        self.xor_list.sort()

        self.current_status = self.initial_status
        self.last_output = last_output
        self.nb_iteration = 0
    
    def next(self):
        """Returns the next bit of the LFSR"""
        self.last_output = 0b1 & self.current_status
        tmp = self.last_output
        for i in self.xor_list:
            tmp = (self.current_status>>i & 0b1)^tmp # `^` is a XOR
        
        # shifting the list
        self.current_status = (self.current_status>>1) + tmp*(1 << self.size)
        self.nb_iteration += 1

        return self.last_output
    
    def reset(self):
        self.current_status = self.initial_status
        self.last_output = None
        self.nb_iteration = 0
    
    def check_duplicates(self):
        """
        Returns: Check if there is a cycle before 2^n - 1 iterations
        """
        # check duplicates
        old_last_output = self.last_output # we have to back up this
        start = self.current_status
        for i in range(2**(self.size+1) - 2): # First one is included
            self.next()
            if self.current_status == start:
                print("There is a duplicate at iteration number",i+1)
                print("start:", start)
                print("xor_list:", self.xor_list)
                print("current_status", self.current_status)
                # reset status
                self.last_output = old_last_output
                self.current_status = start
                self.nb_iteration -= i
                return False
        # reset status
        self.last_output = old_last_output
        self.current_status = start
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
    
    def next(self):
        """Returns the 8 next bits of the CSS as an int"""
        x = 0
        for i in range(8): x += self.lfsr1.next() << i
        y = 0
        for i in range(8): y += self.lfsr2.next() << i

        z = (x+y+self.c)%256

        self.c = 1 if x+y>255 else 0
        return z

    def encode(self, m):
        """
        `m` must be a string composed by numbers in hexadecimal (0<m<ff)
        AND len(m) must be even
        -
        It does not use `next` function, it's faster
        """
        res = 0 
        for i in range(len(m)//2):
            x = self.next()
            res = (res<<8) +x# self.next()

        self.reset()
        return hex(res^int(m,16))[2:]
    
    def decode(self, c):
        # It's symmetrical
        return self.encode(c)



######### TESTINT PART

def test0():
    # First example from the PDF (on 8 bits)
    start = 0b10010110
    xor_list = (2,3,4)
    l = LFSR(8,start, xor_list)
    l.check_duplicates()

def test1():
    """
    Example for an LFSR of 17 bits.
    This may take a bit of time.
    (question 1)
    """
    n = 17
    start = 1 << (n-1) #"1" + (n-1)*"0"
    xor_list = (14,0)

    l = LFSR(n, start, xor_list) 
    l.check_duplicates()

def test2():
    """
    Example for an LFSR of 25 bits.
    This may take even more time than for 17 bits.
    (question 2)
    """
    n = 25
    start = 1 << (n-1) 
    xor_list = (12,4,3,0)

    l = LFSR(n, start, xor_list) 
    l.check_duplicates()


def test3():
    """
    (question 3)
    """
    n = 17
    start = 1 << (n-1) 
    xor_list = (14,0)
    l1 = LFSR(n, start, xor_list) 

    n = 25
    start = 1 << (n-1) 
    xor_list = (12,4,3,0)
    l2 = LFSR(n, start, xor_list) 

    css = CSS(l1,l2)
    m = "ffffffffff"

    print(f"The message: {m}")

    c = css.encode(m)
    print(f"Encoded message: {c}")
    print(f"Decoding the encoded message: {css.decode(c)}") # verification

    
if __name__ == "__main__":
    # NOTE : not every LFSR have a "cycle" of 2^n - 1 iterations 

    # test0()
    # test1()
    # test2() # This test may take a bit of time
    # test3()

    pass