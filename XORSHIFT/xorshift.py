import math

class Xorshift:
    
    MASK = 0xFFFFFFFF
    
    def __init__(self, word_size: int, seed: int = 2463534242):
        self.word_size = word_size
        self.state = seed
        self.lcm = math.lcm(word_size, 32)
        
    def next(self):
        
        # Gerando mmc (lcm) bits usando os parâmentros favoritos do Marsaglia para as palavras de 32 bits
        words_32b = []
        for _ in range(self.lcm // 32):
            # Temos que aplicar uma máscara pois o Python tem precisão arbitrária em inteiros,
            # e aqui queremos 32 bits.
            self.state ^= (self.state << 13) & Xorshift.MASK
            self.state = (self.state >> 17) & Xorshift.MASK
            word = self.state & Xorshift.MASK
            self.state ^= (self.state << 5) & Xorshift.MASK
            self.state &= Xorshift.MASK
            words_32b.append(bin(word)[2:].zfill(32))
        
        lcm_word = "".join(words_32b)
        
        # Considerando lcm/word_size palavras de tamanho word_size
        words_actual_size = [
            lcm_word[i:i + self.word_size]
            for i in range(0, len(lcm_word), self.word_size)
        ]
        
        final_num = 0
        for word in words_actual_size:
            final_num ^= int(word, 2)
        
        # Forçando o tamanho da palavra
        final_word = bin(final_num)[2:].zfill(self.word_size)
            
        return final_word
    
    def next_as_int(self):
        '''
        NOTE: Esse método converte a palavra gerada para um inteiro do Python, que na pŕatica remove zeros à esquerda.
        Isso implica que o tamanho verdadeiro N do número vai ser tal que N <= word_size.
        '''
        return int(self.next())
    

x40 = Xorshift(40)
N = x40.next()
print(N)
print(len(N))

x56 = Xorshift(56)
N2 = x56.next()
print(N2)
print(len(N2))

