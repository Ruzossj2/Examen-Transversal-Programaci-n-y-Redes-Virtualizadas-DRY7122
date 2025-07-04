vlan = int(input("Ingrese el número de VLAN: "))
if 1 <= vlan <= 1005:
    print("VLAN en rango normal.")
elif 1006 <= vlan <= 4094:
    print("VLAN en rango extendido.")
else:
    print("Número de VLAN no válido.")
