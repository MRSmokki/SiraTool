import argparse
import os
import subprocess
import requests
from colorama import Fore, Style

def install_libraries():
    try:
        import colorama
        from tqdm import tqdm
    except ImportError:
        print("ERROR: Debe instalar las bibliotecas 'colorama' y 'tqdm' antes de continuar.")
        print("Puede instalarlas con 'pip install colorama tqdm'.")
        sys.exit()


def arp_scan():
    print("Realizando el arp-scan...")
    result = subprocess.run(["sudo", "arp-scan", "-l"], capture_output=True, text=True)
    print(Fore.GREEN + "Arp-scan completado exitosamente." + Style.RESET_ALL)
    return result.stdout.splitlines()[2:-3]

def show_hosts(hosts):
    print("Lista de hosts encontrados:")
    for i, host in enumerate(hosts):
        print(f"{i+1}. {host}")

def save_arp_scan(host):
    with open("resultado_final.txt", "a") as final_f:
        final_f.write("\n\n")
        final_f.write("=" * 50 + "\n")
        final_f.write("RESULTADOS DEL ARP-SCAN\n")
        final_f.write("=" * 50 + "\n")
        final_f.write(host + "\n")
    return host

def nmap_scan(host_ip):
    print("Realizando el nmap...")
    with open("resultado_final.txt", "a") as nmap_out:
        subprocess.run(["sudo", "nmap", "-sS", "-sV", "-T4", host_ip], stdout=nmap_out)
    print(Fore.GREEN + "Nmap completado exitosamente." + Style.RESET_ALL)


def nikto_scan(host_ip):
    print("Realizando el escaneo de servicios web...")
    with open("resultado_final.txt", "a") as nikto_out:
        subprocess.run(["sudo", "nikto", "-h", f"http://{host_ip}"], stdout=nikto_out)
    print(Fore.GREEN + "Escaneo de servicios web completado exitosamente." + Style.RESET_ALL)


def dirb_scan(host_ip):
    print("Buscando directorios...")
    with open("resultado_final.txt", "a") as dirb_out:
        subprocess.run(["sudo", "dirb", f"http://{host_ip}", "/usr/share/dirb/wordlists/common.txt"], stdout=dirb_out)
    print(Fore.GREEN + "Búsqueda de directorios completada exitosamente." + Style.RESET_ALL)


def save_results(host_ip):
    print(Fore.GREEN + f"Resultados guardados en archivo resultado_{host_ip}.txt" + Style.RESET_ALL)


def delete_temp_files(host_ip):
    try:
        os.remove(f"resultado_{host_ip}.txt")
    except FileNotFoundError:
        pass

def analyze_results_with_chatgpt():
    with open("resultado_final.txt", "r") as result_file:
        file_lines = result_file.readlines()

    # Definir palabras clave para filtrar información crítica
    keywords = ["CRITICAL", "WARNING", "VULNERABLE", "cve", "open"]

    # Filtrar las líneas que contengan al menos una palabra clave
    filtered_lines = [line for line in file_lines if any(keyword in line for keyword in keywords)]
    filtered_content = "".join(filtered_lines)

    url = "https://api.openai.com/v1/engines/text-davinci-002/completions"
    headers = {
        "Authorization": f"Bearer <YOUR API KEY>",
        "Content-Type": "application/json",
    }
    prompt = f"Analyze the following security scan results:\n{filtered_content}\nAnalysis:"

    data = {
        "prompt": prompt,
        "max_tokens": 1024,
        "n": 1,
        "stop": None,
        "temperature": 0.5,
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code == 200:
        analysis = response_json["choices"][0]["text"].strip()
    else:
        raise Exception(f"Error: {response_json}")

    with open("resultado_final.txt", "a") as result_file:
        result_file.write("\n\n")
        result_file.write("=" * 50 + "\n")
        result_file.write("ANÁLISIS DE CHATGPT\n")
        result_file.write("=" * 50 + "\n")
        result_file.write(analysis + "\n")

    print("El escaneo ha finalizado y ha sido analizado por ChatGPT. Puede encontrar los resultados y el análisis en el archivo resultado_final.txt.")


if __name__ == "__main__":
    install_libraries()
    hosts = arp_scan()
    show_hosts(hosts)
    selected_index = int(input("Seleccione una dirección IP de la lista: ")) - 1
    selected_host = hosts[selected_index].split()[0]
    save_arp_scan(selected_host)
    nmap_scan(selected_host)
    nikto_scan(selected_host)
    dirb_scan(selected_host)
    save_results(selected_host)
    delete_temp_files(selected_host)
    analyze_results_with_chatgpt()
