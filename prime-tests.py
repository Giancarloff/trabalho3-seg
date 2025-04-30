import random
import time
import sympy
import BBS.bbs as bbs
import XORSHIFT.xorshift as xs

random.seed("TRABALHO 3") 

class PrimeTests:

    '''
    Implementação básica de Miller-Rabin conforme material de aula
    '''
    def miller_rabin(n: int, num_tests: int = 10) -> bool:

        if n == 2:
            return True
        elif n == 1:
            return False
        elif n % 2 == 0:
            return False # Claramente não é primo
        
        # Escrevendo n-1 como 2^k * m
        k = 0
        m = n - 1
        while m % 2 == 0:
            m = m // 2
            k += 1

        # Testando alguns valores de 'a'
        outcomes = []
        for _ in range(num_tests):
            returned = False # Se fosse uma única execução, essa variável controla se o miller-rabin já teria retornado "Provavelmente primo"
            a = random.randrange(2, n - 1)
            if (a**m) % n == 1:
                outcomes.append(True)
                returned = True
            else:
                for i in range(k):
                    if (a**((2**i)*m) % n == n - 1):
                        outcomes.append(True)
                        returned = True
            
            if not returned: # Se não teria retornado "provavelmente primo", então retornaria composto
                outcomes.append(False)
        
        return all(outcomes) # Se todas as testemunhas disseram que é provavelmente primo, diz que o é e reporta a chance esperada de erro.


    def solovay_strassen(n: int, num_tests: int = 10) -> bool:
        if n == 2:
            return True
        elif n == 1:
            return False
        elif n % 2 == 0:
            return False # Claramente não é primo
        
        for _ in range(num_tests):
            a = random.randrange(2, n-1)
            x = sympy.jacobi_symbol(a, n)
            if x == 0 or pow(a, (n - 1) // 2, n) != x % n:
                return False

        return True

if __name__ == "__main__":
    word_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096] # Em bits
    # Gerando primos com xorshift + miller-rabin
    xs_mr_times: dict[int, float] = {}
    xs_mr_primes: dict[int, int] = {}
    for w in word_sizes:
        print(f"Doing word size {w}.")
        start = time.time()
        xorshift = xs.Xorshift(w)
        n = xorshift.next_as_int()
        if n % 2 == 0:
            n += 1

        print(f"Have {n}.")
        
        prime = PrimeTests.miller_rabin(n)
        while not prime: # Como o xorshift é rápido eu apenas gero outro número
            n += 2
            prime = PrimeTests.miller_rabin(n)
        
        end = time.time()

        dt = (end - start) * 1000 # milisegundos

        xs_mr_times[w] = dt
        xs_mr_primes[w] = n
        print(f"Word size {w} done.")

    for k in xs_mr_times.keys():
        print(f"{hex(xs_mr_primes[k])} : {xs_mr_times[k]}")

    # Xorshift + Solovay-Strassen
    xs_ss_times: dict[int, float] = {}
    xs_ss_primes: dict[int, int] = {}
    for w in word_sizes:
        print(f"Doing word size {w}.")
        start = time.time()
        xorshift = xs.Xorshift(w)
        n = xorshift.next_as_int()
        if n % 2 == 0:
            n += 1

        print(f"Have {n}.")
        
        prime = PrimeTests.solovay_strassen(n)
        while not prime: 
            n += 2
            prime = PrimeTests.solovay_strassen(n)
        
        end = time.time()

        dt = (end - start) * 1000 # milisegundos

        xs_ss_times[w] = dt
        xs_ss_primes[w] = n
        print(f"Word size {w} done.")

    for k in xs_ss_times.keys():
        print(f"{hex(xs_ss_primes[k])} : {xs_ss_times[k]}")

    # BBS + Miller-Rabin
    bbs_mr_times: dict[int, float] = {}
    bbs_mr_primes: dict[int, int] = {}
    for w in word_sizes:
        print(f"Doing word size {w}.")
        start = time.time()
        bbsrng = bbs.BBS(w)
        n = bbsrng.get()
        if n % 2 == 0:
            n += 1

        print(f"Have {n}.")
        
        prime = PrimeTests.miller_rabin(n)
        while not prime: 
            n += 2
            prime = PrimeTests.miller_rabin(n)
        
        end = time.time()

        dt = (end - start) * 1000 # milisegundos

        bbs_mr_times[w] = dt
        bbs_mr_primes[w] = n
        print(f"Word size {w} done.")

    for k in bbs_mr_times.keys():
        print(f"{hex(bbs_mr_primes[k])} : {bbs_mr_times[k]}")

    # BBS + Solovay-Strassen
    bbs_ss_times: dict[int, float] = {}
    bbs_ss_primes: dict[int, int] = {}
    for w in word_sizes:
        print(f"Doing word size {w}.")
        start = time.time()
        bbsrng = bbs.BBS(w)
        n = bbsrng.get()
        if n % 2 == 0:
            n += 1

        print(f"Have {n}.")
        
        prime = PrimeTests.solovay_strassen(n)
        while not prime: 
            n += 2
            prime = PrimeTests.solovay_strassen(n)
        
        end = time.time()

        dt = (end - start) * 1000 # milisegundos

        bbs_ss_times[w] = dt
        bbs_ss_primes[w] = n
        print(f"Word size {w} done.")

    for k in bbs_ss_times.keys():
        print(f"{hex(bbs_ss_primes[k])} : {bbs_ss_times[k]}")