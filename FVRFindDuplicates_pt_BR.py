import os # Módulo para interagir com o sistema operacional, como navegar em diretórios e verificar a existência de arquivos e diretórios.
import hashlib # Módulo para cálculo de hashes (no código, é usado para calcular o hash SHA-256 dos arquivos).
import shutil # Módulo para operações de alto nível em arquivos e diretórios, como copiar e remover.
import win32com.client # Módulo para acessar objetos COM no Windows (no código, é usado para criar atalhos no sistema).
import re  # Módulo para trabalhar com expressões regulares, usado para limpar nomes de arquivos.
import keyboard # Módulo para monitorar eventos de teclado, usado para aguardar a tecla Enter ser pressionada no final.
from colorama import Fore, Back, Style, init # Módulo que fornece funcionalidades para colorir a saída no console.

# Inicializa o módulo colorama com a opção autoreset=True, o que significa que as configurações de cores são redefinidas automaticamente após cada saída colorida.
init(autoreset=True)

# Arte do cabeçalho do programa. Ele é uma string multilinha que será impressa no início do programa.
header_text = """
                                                      
        :==:                              :==:        
     =********=                        :********+     
    ************                      ************.   
   +*************                    +************=   
   +*************+                  =*************+   
   .**************-                :**************:   
    .**************-              :**************:    
     :**************:            :**************-     
      =**************            **************+      
       =**************.         ***************       
        ***************        ***************        
         ***************      ***************         
          ***************    +**************          
          .**************=  :**************.          
            **************=:**************:           
            :****************************:            
             -***************###########=             
              -***************#########=              
               ***************%%%%%%%%*               
                ***************%%%%%%*                
                 *############**%%%%*                 
                 .*#############*%%#.     Viappz.com           
                   *##############%.        by Fernando VR          
                   :#############*:                   
                    :############=                    
                     :##########-                     
                       =*#####=                       
                                                      
"""

# Imprima o cabeçalho colorido
print(Fore.GREEN + Back.BLACK + header_text)

# Obtém a largura do terminal em colunas, que será usada posteriormente para limitar o tamanho de algumas saídas de texto.
largura_terminal = shutil.get_terminal_size().columns

# Essa função verifica o tamanho do texto e, se for maior que a largura do terminal, trunca e adiciona "..." no final.
def limitar_tamanho_texto(texto):
    if len(texto) > largura_terminal:
        return texto[:largura_terminal - 3] + "..."  # Trunca o texto e adiciona "..."
    return texto

# Essa função limpa a linha atual no console, preenchendo-a com espaços em branco.
def limpar_linha():
    print(" " * largura_terminal, end="\r")

# Essa função calcula o hash SHA-256 de um arquivo.
def calcular_hash_arquivo(arquivo):
    # Cria um objeto hash
    sha256 = hashlib.sha256()

    # Lê o arquivo em pedaços para evitar consumo excessivo de memória
    with open(arquivo, "rb") as f:
        while True:
            bloco = f.read(4096)
            if not bloco:
                break
            sha256.update(bloco)

    # Retorna o hash calculado
    return sha256.hexdigest()

# Essa função encontra arquivos duplicados em um diretório e seus subdiretórios.
def encontrar_arquivos_duplicados(diretorio):
    # Dicionário para armazenar os hashes e os arquivos correspondentes
    hash_arquivos = {}

    for pasta_raiz, subdiretorios, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            caminho_completo = os.path.join(pasta_raiz, arquivo)
            hash_arquivo = calcular_hash_arquivo(caminho_completo)

            if hash_arquivo in hash_arquivos:
                hash_arquivos[hash_arquivo].append(caminho_completo)
            else:
                hash_arquivos[hash_arquivo] = [caminho_completo]
                
            # Limpa a linha atual no console
            limpar_linha()
            
            nome_arquivo_limitado = limitar_tamanho_texto(f"Analisando: {arquivo}")
            
            # Exibe o arquivo que está sendo analisado
            print(Fore.CYAN + nome_arquivo_limitado, end="\r")
                
    limpar_linha()
    print(Fore.GREEN + "Análise concluída.")
    
    # Retorna os arquivos duplicados
    return {hash: arquivos for hash, arquivos in hash_arquivos.items() if len(arquivos) > 1}

# Essa função limpa o nome de um arquivo removendo caracteres especiais e limitando o tamanho a 50 caracteres.
def limpar_nome_arquivo(arquivo_original):
    nome_arquivo = os.path.splitext(os.path.basename(arquivo_original))[0] # Pega o nome do arquivo sem a extenção
    nome_arquivo = re.sub(r"[^\w\s]", "", nome_arquivo)  # Remove caracteres especiais utiliando expressões regulares
    nome_arquivo = nome_arquivo.strip()[:50]  # Limita a 50 caracteres
    return nome_arquivo

# Essa função cria um nome para um atalho baseado no arquivo original e contadores.
def criar_nome_atalho(arquivo_original, pasta_destino, contador_geral, contador_duplicados):
    _, extensao = os.path.splitext(arquivo_original)
    
    # Remove caracteres especiais do nome do arquivo e limita a 50 caracteres
    nome_arquivo = limpar_nome_arquivo(arquivo_original)
    
    # Formata o nome adicionando uma contagem geral de 5 digitos, e outra de 3 digitos para cada arquivo duplicado do mesmo tipo
    nome_atalho = f"{contador_geral:05d}-{contador_duplicados:03d}-{nome_arquivo}{extensao}"
    return nome_atalho
    
# Essa função cria um atalho no Windows para um arquivo original.
def criar_atalho_windows(arquivo_original, pasta_destino, contador_geral, contador_duplicados):
    shell = win32com.client.Dispatch("WScript.Shell")
    nome_atalho = criar_nome_atalho(arquivo_original, pasta_destino, contador_geral, contador_duplicados)
    atalho = shell.CreateShortCut(os.path.join(pasta_destino, nome_atalho + ".lnk"))
    atalho.TargetPath = arquivo_original
    atalho.save()
    
# Essa função solicita ao usuário um caminho de diretório válido e garante que ele seja válido. 
def obter_diretorio_valido():
    while True:
        diretorio_base = input("Informe o caminho do diretório a ser pesquisado: ")
        if not diretorio_base:
            print(Fore.YELLOW + "O campo não pode estar em branco. Por favor, informe um diretório válido.")
        elif not os.path.exists(diretorio_base):
            print(Fore.RED + f"O diretório '{diretorio_base}' não existe. Por favor, informe um diretório válido.")
        else:
            return diretorio_base

# Bloco principal do programa       
# O bloco principal do programa é executado apenas se o código for executado como um script, não se for importado como um módulo.   
if __name__ == "__main__":
    
    # Obtém o diretório base a ser pesquisado a partir da função obter_diretorio_valido.
    diretorio_base = obter_diretorio_valido()
    
    if diretorio_base is None:
        # Executa caso o diretorio_base não seja informado.
        # Provavelmente essa linha nunca será executada, mas criei só por garantia para não retornar nenhum erro no projeto.
        # Pensei em criar aqui uma monitoração para quando o usuario apertar o botão ESC no teclado e finalizar o programa, mas teria que criar um novo thread, então desisti para não deixar o programa mais pesado só por causa de uma tecla, sendo que o usuário pode finalizar fechando o terminal. 
        print("Programa finalizado.")
    else:
        # Chama a função encontrar_arquivos_duplicados para encontrar arquivos duplicados no diretório base.
        arquivos_duplicados = encontrar_arquivos_duplicados(diretorio_base)

    # Cria uma pasta de destino para os atalhos, se ela ainda não existir.
    pasta_destino = "Atalhos_Duplicados"
    if not os.path.exists(pasta_destino):
        os.mkdir(pasta_destino)

    # Em um loop, itera sobre os arquivos duplicados encontrados e cria atalhos para eles.
    contador_geral = 1
    for hash, arquivos in arquivos_duplicados.items():
        contador_duplicados = 1
        for arquivo in arquivos:
            print(Fore.RED + f"Arquivo duplicado com hash {hash}:")
            print(Fore.MAGENTA + f"  {arquivo}")
            criar_atalho_windows(arquivo, pasta_destino, contador_geral, contador_duplicados)
            contador_duplicados += 1
        contador_geral += 1
    
    # Imprime uma mensagem indicando que os atalhos foram criados com sucesso.
    print(Fore.GREEN + f"Atalhos dos arquivos duplicados foram criados em {os.path.abspath(pasta_destino)}")
    
    # Exibe uma mensagem de conclusão e aguarda que o usuário pressione a tecla Enter para encerrar o programa.
    print(Fore.YELLOW + "Finalizado. Pressione ENTER para encerrar.")
    keyboard.wait("enter")