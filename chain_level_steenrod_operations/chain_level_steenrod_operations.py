from collections import Counter

#_________________________________79_characters________________________________

# ## Modules over the ring integers

class int_comb(Counter):
    '''...'''
    
    def __init__(*args, **kwds):
        '''...'''
        self, *args = args
        super(int_comb, self).__init__(*args, **kwds)
        
        if not all( [type(v) is int for v in self.values()] ):
            raise TypeError('values must be integers')

    def reduce_rep(self):
        '''deletes keys with 0 value'''
        zeros = [k for k,v in self.items() if not v]
        for key in zeros:
            del self[key]
    
    def __add__(self, other):
        '''...'''
        answer = int_comb(self)
        answer.update(other)
        return int_comb( {k:v for k,v in answer.items() if v} )
    
    def __sub__(self, other):
        '''...'''
        answer = int_comb(self)
        answer.subtract(other)
        return int_comb( {k:-v for k,v in answer.items() if v} )
    
    def __mod__(self, p):
        '''...'''
        return int_comb( {k:v%p for k,v in self.items() if v % p} )
    
    def __neg__(self):
        '''...'''
        return int_comb( {k:-v for k,v in self.items() if v} )
    
    def __rmul__(self, c):
        '''...'''
        if type(c) is int:
            for key, value in self.items():
                self[key] = value*c
            return self
        else:
            raise TypeError('can scale by integers only')
    
    def __iadd__(self, other):
        '''...'''
        self.update(other)
        self.remove_zeros()
        return self
    
    def __isub__(self, other):
        '''...'''
        self.subtract(other)
        self.remove_zeros()
        return self
    
    def __imod__(self, p):
        '''...'''
        for key, value in self.items():
            self[key] = value % p
            
        return self
    
    def __str__(self):
        '''...'''
        self.reduce_rep()
        if not self:
            return '0'
        else:
            answer = '' 
            for key, value in self.items():
                if value < 0:
                    answer += f'{value}{key}'
                elif value == 1:
                    answer += f'+{key}'
                elif value > 1:
                    answer += f'+{value}{key}'    
            if answer[0] == '+':
                answer = answer[1:]

            return answer


print('1st)', int_comb({'a':4, 'should be zero':0}), '\n')

#_________________________________79_characters________________________________

# ## Modules over the ring modulor integers

class mod_p_comb(int_comb):
    '''...'''
    
    prime = 3
    
    def __init__(*args, **kwds):
        '''...'''
        self, *args = args
        super(mod_p_comb, self).__init__(*args, **kwds)
        self.reduce_rep()
        
    def reduce_rep(self):
        '''reduces mod p the values and deletes keys with 0 value'''
        super().__imod__(self.prime)
        super().reduce_rep()
        
    def __add__(self, other):
        '''...'''
        if self.prime != other.prime:
            raise ValueError('same prime for both')
            
        return mod_p_comb( super().__add__(other) )
    
    def __sub__(self, other):
        '''...'''
        if self.prime != other.prime:
            raise ValueError('same prime for both')
            
        return mod_p_comb( super().__sub__(other) )
    
    def __neg__(self):
        '''...'''
        return mod_p_comb( {k:-v for k,v in self.items() if v} )
    
    def __rmul__(self, c):
        '''...'''
        super().__rmul__(c)
        self.reduce_rep()

print('2nd)', mod_p_comb({'a':4, 'should be 0':0}),'\n')

#_________________________________79_characters________________________________

# ## Integral bar resolutions

class bar_cpx_elmt(int_comb):
    '''...'''
    
    def __init__(*args, **kwds):
        '''...'''
        self, *args = args
        super(bar_cpx_elmt, self).__init__(*args, **kwds)
        if not all([isinstance(x,tuple) for x in self.keys()]):
            raise TypeError('keys must be tuples')
        self.reduce_rep()

    def reduce_rep(self):
        '''deletes keys with 0 value or which are degenerate'''
        for simplex,v in self.items():
            if _is_degenerate(simplex):
                self[simplex] = 0
        super().reduce_rep()        
    
    def boundary(self):
        '''...'''
        bdry = bar_cpx_elmt()
        for spx, coeff in self.items():
            for i in range(len(spx)):
                i_face = tuple(spx[:i]+spx[i+1:])
                i_coeff = coeff*((-1)**i)
                bdry += bar_cpx_elmt({i_face: i_coeff})
        return bdry
    
def _is_degenerate(simplex):
    '''returns True if the simplex is non-degenerate and False otherwise'''
    if not type(simplex) is tuple:
        raise TypeError('simplex must be a tuple')
    for i in range(len(simplex)-1):
        if simplex[i] == simplex[i+1]:
            return True
    return False

print('3er) bar_cpx_elmt:', bar_cpx_elmt({(1,2):3, (1,1):1, (2,3):1}), '\n')    
#_________________________________79_characters________________________________

# ## Bar resolution of Z_p[C_p]

class cyclic_bar_cpx_elmt(mod_p_comb, bar_cpx_elmt):
    '''...'''
    def reduce_rep(self):
        '''reduces mod p the keys and values and deletes keys with 0 value 
        or which are degenerate'''
        aux = list(self.items())
        self.clear()
        for x, v in aux:
            y = tuple(i % 3 for i in x)
            self[y] += v
        super().reduce_rep()

    def __repr__(self):
        '''...'''
        s = super().__repr__()
        if self:
            return s.replace('})',f'}}, p={self.prime})')
        if not self:
            return s.replace('()', f'({{}}, p={self.prime})')
        
    def __str__(self):
        '''...'''
        s = super().__str__()
        s = s.replace(', ', ',')
        return s.replace('(','a^(')

print('4th) cyclic_bar_cpx_elmt:', 
    cyclic_bar_cpx_elmt({(1,5):3, (1,1):1, (2,4):1}), '\n')

#_________________________________79_characters________________________________

# ## Z_p[C_p]

class cyclic_mod_p_alg_elmt(mod_p_comb):
    '''...'''
    
    def __init__(*args, **kwds):
        '''...'''
        self, *args = args
        super(cyclic_mod_p_alg_elmt, self).__init__(*args, **kwds)
        if not all([isinstance(k,int) for k in self.keys()]):
            raise TypeError('keys must be integers')
        self.reduce_rep()
    
    def reduce_rep(self):
        '''in place mod p reduction of the keys'''
        aux = list(self.items())
        self.clear()
        for k,v in aux:
            self[k%self.prime] += v
        super().reduce_rep()

    def __add__(self, other):
        '''...'''
        if self.prime != other.prime:
            raise ValueError('same prime for both')
            
        return cyclic_mod_p_alg_elmt( super().__add__(other) )
    
    def __sub__(self, other):
        '''...'''
        if self.prime != other.prime:
            raise ValueError('same prime for both')
            
        return cyclic_mod_p_alg_elmt( super().__sub__(other) )
    
    def __neg__(self):
        '''...'''
        return cyclic_mod_p_alg_elmt( {k:-v for k,v in self.items() if v} )
            
    def __mul__(self, other):
        '''...'''
        if self.prime != other.prime:
            raise ValueError('same prime for both')
        answer = cyclic_mod_p_alg_elmt()
        for k1,v1 in self.items():
            for k2,v2 in other.items():
                answer[k1+k2] += v1*v2
        answer.reduce_rep()
        
        return answer
        
    def __call__(self, other):
        '''...'''
        if isinstance(other, cyclic_mod_p_alg_elmt):
            return self*other
        if isinstance(other, cyclic_bar_cpx_elmt):
            if self.prime != other.prime:
                raise ValueError('same prime for both')  
            answer = Counter()
            for k,v1 in self.items():
                for x,v2 in other.items():
                    y = tuple(k+i % self.prime for i in x)
                    answer[y] += v1*v2
            return cyclic_bar_cpx_elmt(answer)
    
    def __repr__(self):
        '''...'''
        s = super().__repr__()
        if self:
            return s.replace('})',f'}}, p={self.prime})')
        if not self:
            return s.replace('()', f'({{}}, p={self.prime})')
    
    def __str__(self):
        '''...'''
        self.reduce_rep()
        print(repr(self))
        if not self:
            return '0'
        else:
            answer = '' 
            for exponent, coefficient in self.items():
                if coefficient != 1:
                    answer += f'+{coefficient}a^{exponent}'
                if coefficient == 1:
                    answer += f'+a^{exponent}'    
            if answer[0] == '+':
                answer = answer[1:]

            return answer.replace('a^0','').replace('a^1','a')
        
    @staticmethod
    def norm_elmt():
        '''...'''
        elmt = {i:1 for i in range(mod_p_comb.prime)}
        return cyclic_mod_p_alg_elmt(elmt)
    
    @staticmethod
    def transpo_elmt():
        '''...'''
        elmt = {1:1, 0:-1}
        return cyclic_mod_p_alg_elmt(elmt)
    
    @staticmethod
    def all_elmts():
        '''...'''
        p = mod_p_comb.prime
        return ( cyclic_mod_p_alg_elmt( dict(zip(range(p), coeffs)) ) 
                 for coeffs in product(range(p),repeat=p) )

print('5th) cyclic_mod_p_alg_elmt:', cyclic_mod_p_alg_elmt({2:4}), '\n')

#_________________________________79_characters________________________________

## Reusable code

def get_basis(n):
    '''Returns the preferred basis of $\mathcal E(\pi)_n$'''
    basis = [group_element for group_element 
             in product((0,1,2), repeat=n+1) 
             if nondegenerate(group_element)]
    
    return basis

def join(simplex, counter):
    '''Returns the Counter resulting from changing the 
    keys of counter via the join with simplex'''
    counter = Counter({simplex + elmt: coeff 
                       for elmt, coeff in counter.items()})
    
    return clean(counter)
