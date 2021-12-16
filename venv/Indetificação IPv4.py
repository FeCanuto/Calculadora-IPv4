import re
from netaddr import IPNetwork

ipv4 = input(
    "Digitar um IPv4 com máscara de rede na notação CIDR, Exemplo: 27.15.100.128 /17 \n>> ")  # ipv4 com máscara de
# rede na notação CIDR exemplo: 27.15.100.128/17

'''Listas Vazias'''
decmask = []
ip_dec = []
ip_hex = []
ip_bin = []
ip_rede = []
broadcast = []

parts = re.split("./", ipv4)  # utilização de uma expressão regular re.split para separar o IPv4 da máscara
CIDR = int(parts[1])  # Converter a máscara de string para inteiro
stroct = parts[0].split(".")  # Usando split para criar uma lista de strings contendo os 4 octetos

ip = IPNetwork(ipv4)
binmask = ip.netmask.bits().split(".")  # Conversão da máscara na notação cidr para binário


def convert_string_list(
        string_ip):  # Convertendo a lista de strings contendo os octetos em uma lista de int contendo os octetos
    for i in string_ip:
        ip_dec.append(int(i))


def format_binary(decimal):  # Formatando o binário para ter 8 digitos
    for j in decimal:
        ip_bin.append(format(j, "08b"))


def inttohex(decimal):
    for i in decimal:
        ip_hex.append(hex(i))


def broadcast_network_address(mask):
    for i in range(len(mask)):
        decmask.append(int(mask[i], 2))
        ip_rede.append(decmask[i] & ip_dec[i])  # Operação de AND lógico para encontrar o endereço da rede
        broadcast.append(
            (~decmask[i] & 0xff) | ip_dec[i])  # Operação NOT na máscara seguida de um AND com o hexa de 255,
        # o resutaldo dessa operação e um OR com o IP resulta no Broadcast


def amount_host(
        mask):  # Somando a quantidade de bits 0 na máscara, para indetificar a quantidade de hosts a posteriori
    amount = 0
    for i in range(len(mask)):
        for _ in range(1, 9):
            result = int(mask[i]) % 10
            if result == 0:
                amount += 1
    return amount


convert_string_list(stroct)
format_binary(ip_dec)
inttohex(ip_dec)
broadcast_network_address(binmask)
hosts = amount_host(binmask)

print("Máscara de rede notação CIDR: /" + str(CIDR))
print("Máscara de rede binário:", binmask)
print("Máscara de rede decimal:", decmask)
print("|----------------------------------------------------------------------------|")
print("IPv4 binário:", ip_bin)
print("IPv4 decimal:", ip_dec)
print("IPv4 Hexadecimal:", ip_hex)
print("IPv4 da rede:", ip_rede)
print("IPv4 Broadcast:", broadcast)

inicial = ip_rede
inicial[3] = ip_rede[3] + 1  # O intervalo de hosts inicia um endereço após o endereço da rede
final = broadcast
final[3] = broadcast[3] - 1  # O intervalo de hosts finaliza com um endereço antes do endereço broadcast

print("Intervalo de endereços de host:", inicial, "-", final)
print("Número de Hosts:", pow(2, hosts - 1))
print("Número de Hosts possíveis:", pow(2, hosts - 1) - 2)
