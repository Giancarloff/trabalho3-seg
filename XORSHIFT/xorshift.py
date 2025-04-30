import math
import statistics
import time
import matplotlib.pyplot as plt

class Xorshift:
    
    MASK = 0xFFFFFFFF
    
    # Essa semente foi tirada diretamente do artigo do Marsaglia
    def __init__(self, word_size: int, seed: int = 2463534242):
        self.word_size = word_size
        self.state = seed
        self.lcm = math.lcm(word_size, 32)
        
    def next(self):
        
        # Gerando mmc (lcm) bits usando os parâmentros favoritos do Marsaglia para as palavras de 32 bits
        lcm_word = ""
        for _ in range(self.lcm // 32):
            # Temos que aplicar uma máscara pois o Python tem precisão arbitrária em inteiros,
            # e aqui queremos 32 bits.
            self.state ^= (self.state << 13) & Xorshift.MASK
            self.state = (self.state >> 17) & Xorshift.MASK
            self.state ^= (self.state << 5) & Xorshift.MASK
            word = self.state & Xorshift.MASK
            self.state &= Xorshift.MASK
            lcm_word += bin(word)[2:].zfill(32)
        
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
        Isso implica que o tamanho em bits verdadeiro N do número vai ser tal que N <= word_size.
        '''
        return int(self.next(), 2)
    
if __name__ == "__main__":
    # Gerando uma popualção de números
    words: dict[int, list] = {}
    numbers: dict[int, list] = {}
    generation_times: dict[int, list] = {} 

    word_sizes = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096] # Em bits

    num_amount = 100 # Quantos gerar
    for size in word_sizes:
        numbers[size] = []
        words[size] = []
        generation_times[size] = []
        xorshift = Xorshift(size)
        for _ in range(num_amount):
            start = time.time()
            new_word = xorshift.next()
            end = time.time()
            words[size].append(new_word)
            numbers[size].append(int(new_word, 2))

            dt = (end - start) * 1000  # Converte para milisegundos
            generation_times[size].append(dt) 

    # Estatísticas
    avg_time: dict[int, float] = {}
    stdev_time: dict[int, float] = {}

    for size in word_sizes:
        avg_time[size] = statistics.mean(generation_times[size])
        stdev_time[size] = statistics.stdev(generation_times[size])

    now = time.asctime()
    print(f"Teste feito {now}.")

    for k, v in numbers.items():
        print(f"Size: {k}, Average time: {avg_time[k]:.4f}ms for {num_amount} numbers.")

    # Gerando um gráfico
    x = word_sizes
    y = [avg_time[size] for size in word_sizes]
    yerr = [stdev_time[size] for size in word_sizes]

    plt.figure(figsize=(10,6))
    plt.errorbar(x, y, yerr=yerr, fmt='o-', capsize=5, ecolor='red', markerfacecolor='blue', markersize=5)

    # Estilo
    plt.title("Tempo médio (ms) vs. Tamanho da palavra")
    plt.xlabel("Tamanho da palavra")
    plt.ylabel("Tempo médio (ms)")
    plt.grid(True)
    plt.xscale("log")
    plt.xticks(word_sizes, word_sizes, rotation=45)
    plt.tight_layout()

    plt.savefig(f"xorshift_plot ({now}).pdf")

