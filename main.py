#!/usr/bin/env python3
"""
Menu principal para operações com PDFs
"""

import os
import sys
from extract_page import extrair_paginas_pdf, parse_paginas
from merge_pdf import merge_pdfs
from rotate_pdf import rotate_pdf_pages, parse_paginas as parse_paginas_rotate


def ler_entrada(prompt):
    """Lê uma entrada do usuário"""
    return input(prompt).strip()


def validar_arquivo(caminho, deve_existir=True):
    """Valida se o arquivo existe (se deve_existir=True) ou se o diretório pai existe"""
    if deve_existir:
        if not os.path.exists(caminho):
            print(f"ERRO: Arquivo não encontrado: {caminho}")
            return False
    else:
        # Para arquivo de saída, verificar se o diretório pai existe
        diretorio_pai = os.path.dirname(caminho)
        if diretorio_pai and not os.path.exists(diretorio_pai):
            print(f"ERRO: Diretório não encontrado: {diretorio_pai}")
            return False
    return True


def extrair_paginas():
    """Menu para extrair páginas de um PDF"""
    print("\nEXTRAIR PÁGINAS DE PDF")
    print("=" * 40)
    
    # Entrada do PDF
    while True:
        input_pdf = ler_entrada("Caminho do PDF de entrada: ")
        if not input_pdf:
            print("ERRO: Caminho não pode estar vazio")
            continue
        if validar_arquivo(input_pdf):
            break
    
    # Saída do PDF
    while True:
        output_pdf = ler_entrada("Caminho do PDF de saída: ")
        if not output_pdf:
            print("ERRO: Caminho não pode estar vazio")
            continue
        if validar_arquivo(output_pdf, deve_existir=False):
            break
    
    # Páginas para extrair
    while True:
        paginas_str = ler_entrada("Páginas para extrair (ex: 1,2,5-8): ")
        if not paginas_str:
            print("ERRO: Páginas não podem estar vazias")
            continue
        
        paginas = parse_paginas(paginas_str)
        if not paginas:
            print("ERRO: Nenhuma página válida encontrada")
            continue
        break
    
    print(f"\nExtraindo páginas {paginas} de {os.path.basename(input_pdf)}...")
    try:
        extrair_paginas_pdf(input_pdf, output_pdf, paginas)
        print(f"SUCESSO! PDF salvo em: {output_pdf}")
    except Exception as e:
        print(f"ERRO ao extrair páginas: {e}")


def mesclar_pdfs():
    """Menu para mesclar múltiplos PDFs"""
    print("\nMESCLAR PDFs")
    print("=" * 40)
    
    pdfs = []
    print("Informe os caminhos dos PDFs (em ordem de mesclagem)")
    print("Digite uma linha vazia para finalizar")
    
    while True:
        pdf_path = ler_entrada(f"PDF #{len(pdfs) + 1}: ")
        if not pdf_path:
            break
        
        if validar_arquivo(pdf_path):
            pdfs.append(pdf_path)
            print(f"Adicionado: {os.path.basename(pdf_path)}")
    
    if not pdfs:
        print("ERRO: Nenhum PDF informado")
        return
    
    # Saída do PDF
    while True:
        output_pdf = ler_entrada("Caminho do PDF de saída: ")
        if not output_pdf:
            print("ERRO: Caminho não pode estar vazio")
            continue
        if validar_arquivo(output_pdf, deve_existir=False):
            break
    
    print(f"\nMesclando {len(pdfs)} PDFs...")
    try:
        merge_pdfs(pdfs, output_pdf)
        print(f"SUCESSO! PDF mesclado salvo em: {output_pdf}")
    except Exception as e:
        print(f"ERRO ao mesclar PDFs: {e}")


def rotacionar_pdf():
    """Menu para rotacionar páginas de um PDF"""
    print("\nROTACIONAR PÁGINAS DE PDF")
    print("=" * 40)
    
    # Entrada do PDF
    while True:
        input_pdf = ler_entrada("Caminho do PDF de entrada: ")
        if not input_pdf:
            print("ERRO: Caminho não pode estar vazio")
            continue
        if validar_arquivo(input_pdf):
            break
    
    # Páginas para rotacionar
    while True:
        paginas_str = ler_entrada("Páginas para rotacionar (ex: 1,2,5-8): ")
        if not paginas_str:
            print("ERRO: Páginas não podem estar vazias")
            continue
        
        paginas = parse_paginas_rotate(paginas_str)
        if not paginas:
            print("ERRO: Nenhuma página válida encontrada")
            continue
        break
    
    # Graus de rotação
    while True:
        try:
            graus = int(ler_entrada("Graus para rotacionar (90, 180, 270, -90, -180, -270): "))
            if graus % 90 != 0:
                print("ERRO: Graus deve ser múltiplo de 90")
                continue
            break
        except ValueError:
            print("ERRO: Digite um número válido")
    
    # Saída do PDF (opcional)
    output_pdf = ler_entrada("Caminho do PDF de saída (vazio para automático): ")
    if output_pdf and not validar_arquivo(output_pdf, deve_existir=False):
        return
    
    print(f"\nRotacionando páginas {paginas} em {graus}° de {os.path.basename(input_pdf)}...")
    try:
        resultado = rotate_pdf_pages(input_pdf, paginas, graus, output_pdf if output_pdf else None)
        print(f"SUCESSO! PDF salvo em: {resultado}")
    except Exception as e:
        print(f"ERRO ao rotacionar PDF: {e}")


def mostrar_menu():
    """Mostra o menu principal"""
    print("\n" + "=" * 50)
    print("UTILITÁRIOS DE PDF")
    print("=" * 50)
    print("1. Extrair páginas de um PDF")
    print("2. Mesclar (merge) vários PDFs")
    print("3. Rotacionar páginas de um PDF")
    print("0. Sair")
    print("=" * 50)


def main():
    """Função principal"""
    while True:
        mostrar_menu()
        
        opcao = ler_entrada("Escolha uma opção (0-3): ")
        
        if opcao == "0":
            print("👋 Até logo!")
            break
        elif opcao == "1":
            extrair_paginas()
        elif opcao == "2":
            mesclar_pdfs()
        elif opcao == "3":
            rotacionar_pdf()
        else:
            print("ERRO: Opção inválida! Tente novamente.")
        
        # Pausa antes de mostrar o menu novamente
        if opcao in ["1", "2", "3"]:
            ler_entrada("\nPressione Enter para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário. Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"\nERRO inesperado: {e}")
        sys.exit(1)
