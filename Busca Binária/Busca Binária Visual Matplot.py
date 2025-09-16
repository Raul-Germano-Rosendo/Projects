import random
import time
import os
import math  # Usaremos math para calcular log2

def clear_screen():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def desenhar_array_visual(lista, esquerda, meio, direita, alvo, passo):
    """Desenha uma representação visual do array no console"""
    clear_screen()
    
    print("🔍 BUSCA BINÁRIA VISUAL")
    print("=" * 60)
    print(f"Alvo: {alvo} | Passo: {passo}")
    print(f"Intervalo: [{esquerda}, {direita}] | Ponto médio: {meio} (valor: {lista[meio]})")
    print("=" * 60)
    
    # Linha superior
    print(" " + "─" * (len(lista) * 4 - 1))
    
    # Valores
    linha_valores = "│"
    for i in range(len(lista)):
        if i == esquerda:
            linha_valores += "["
        else:
            linha_valores += " "
            
        if i == meio:
            if lista[i] == alvo:
                linha_valores += "🎯"
            else:
                linha_valores += " *"
            linha_valores += f"{lista[i]:2d}"
            if lista[i] == alvo:
                linha_valores += "🎯"
            else:
                linha_valores += "* "
        else:
            linha_valores += f"{lista[i]:3d} "
            
        if i == direita:
            linha_valores += "]"
        else:
            linha_valores += " "
    
    print(linha_valores + "│")
    
    # Linha inferior
    print(" " + "─" * (len(lista) * 4 - 1))
    
    # Índices
    linha_indices = " "
    for i in range(len(lista)):
        if i == meio:
            linha_indices += f" ⭐{i:2d} "
        else:
            linha_indices += f"  {i:2d} "
    print(linha_indices)
    
    print("=" * 60)
    print("Legenda: [ ] = Limites | * * = Ponto médio | 🎯 = Alvo encontrado")
    print("=" * 60)

def busca_binaria_console(lista, alvo):
    """Busca binária com visualização no console"""
    esquerda, direita = 0, len(lista) - 1
    passo = 0
    
    print("Array ordenado:", lista)
    print("Procurando alvo:", alvo)
    time.sleep(3)
    
    while esquerda <= direita:
        passo += 1
        meio = (esquerda + direita) // 2
        
        desenhar_array_visual(lista, esquerda, meio, direita, alvo, passo)
        
        if lista[meio] == alvo:
            print(f"✅ ALVO ENCONTRADO! Posição: {meio}")
            print(f"📊 Total de passos: {passo}")
            return meio
            
        elif lista[meio] < alvo:
            print(f"➡️  {alvo} > {lista[meio]} - Indo para DIREITA")
            esquerda = meio + 1
        else:
            print(f"⬅️  {alvo} < {lista[meio]} - Indo para ESQUERDA")
            direita = meio - 1
            
        time.sleep(2)
    
    print("❌ Alvo não encontrado")
    return -1

def calcular_maximo_passos(tamanho):
    """Calcula o máximo teórico de passos para busca binária"""
    return int(math.log2(tamanho)) + 1 if tamanho > 0 else 0

# Programa principal
if __name__ == "__main__":
    # Criar array ordenado
    tamanho = 15
    array = sorted(random.sample(range(1, 50), tamanho))
    alvo = random.choice(array)
    
    print("Iniciando busca binária visual...")
    time.sleep(3)
    
    resultado = busca_binaria_console(array, alvo)
    
    # Informações educacionais
    print(f"\n📚 INFORMAÇÕES EDUCACIONAIS:")
    print("=" * 50)
    print(f"• Tamanho do array: {tamanho}")
    print(f"• Complexidade: O(log n) = O(log₂{tamanho})")
    print(f"• Máximo de passos teórico: {calcular_maximo_passos(tamanho)}")
    print(f"• Passos executados: {resultado if resultado == -1 else 'Encontrado antes do máximo'}")
    print("• Eficiência: Divide o problema pela metade a cada passo!")
    print("=" * 50)
    
    # Demonstração de eficiência
    print("\n⚡ DEMONSTRAÇÃO DE EFICIÊNCIA:")
    tamanhos = [10, 100, 1000, 10000, 100000]
    for t in tamanhos:
        max_passos = calcular_maximo_passos(t)
        print(f"Array de {t:6d} elementos → Máximo {max_passos:2d} passos")
    
    print("\n" + "_" * 50)
    print("🎯 A busca binária é extremamente eficiente!")
    print("💡 Ela encontra elementos em arrays ordenados gigantescos em poucos passos!")
    print("_" * 50)