import re

def filter_no_characters(input):
    no_spechar_str = re.sub('[-,./:;]', "", input).strip()
    return no_spechar_str

macaddress_source = filter_no_characters(input("Введите source MAC-адрес "))
macaddress_destination = filter_no_characters(input("Введите destionation MAC-адрес "))
ip_source = filter_no_characters(input("Введите source IP адрес "))
ip_destination = filter_no_characters(input("Введите destination IP адрес "))
slave_count = int(filter_no_characters(input("Введите кол-во интерфейсов в бонде: ")))

ip_source_10x = int(ip_source,10)
ip_destination_10x = int(ip_destination, 10)

macaddress_source_16x = int(macaddress_source, 16)
macaddress_destination_16x = int(macaddress_destination, 16)

macaddress_source_10x = int(str(macaddress_source_16x),10)
macaddress_destination_10x = int(str(macaddress_destination_16x),10)

# 0xffff это 16ричная система в десятичной будет 65535 это reserved ethertype
# (((source IP XOR dest IP) AND 0xffff) XOR ( source MAC XOR destination MAC )) modulo slave count

interface = (((ip_source_10x ^ ip_destination_10x) & 65535) ^ (macaddress_source_10x ^ macaddress_destination_10x))% slave_count
print("По первой формуле трафик будет идти по интерфейсу с порядковым номером: " + str(interface))


# hash1 = source MAC XOR destination MAC XOR packet type ID считается для хэша л2
# (ГДЕ ПАКЕТ АЙДИ ЭТО h_proto в ethernet frame https://www.iana.org/assignments/ieee-802-numbers/ieee-802-numbers.xhtml)
# hash2 = hash1 XOR source IP XOR destination IP
# hash3 = hash2 XOR (hash2 RSHIFT 16)
# hash4 = hash3 XOR (hash3 RSHIFT 8)

# в качестве пакет айди использую не зарезервированный, ethertype для ip 0x0800
packet_type_ID = 2048

hash1 = macaddress_source_10x ^ macaddress_destination_10x ^ packet_type_ID
hash2 = ip_source_10x ^ ip_destination_10x
hash3 = hash2 ^ (hash2 >> 16)
hash4 = hash3 ^ (hash3 >> 8)
interface = hash4 % slave_count

print("По второй формуле трафик будет идти по интерфейсу с порядковым номером: " + str(interface))