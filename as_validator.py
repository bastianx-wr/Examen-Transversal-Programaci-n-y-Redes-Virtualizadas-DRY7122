# as_validator.py

def validar_as_bgp(as_number):
    if not isinstance(as_number, int) or as_number < 1 or as_number > 4294967295:
        return "Número de AS inválido. Debe ser un entero entre 1 y 4294967295."

    if (64512 <= as_number <= 65535) or \
       (4200000000 <= as_number <= 4294967295):
        return f"El AS {as_number} es un AS PRIVADO."
    else:
        return f"El AS {as_number} es un AS PÚBLICO."

if __name__ == "__main__":
    print("--- Validador de AS BGP ---")
    try:
        as_input = input("Por favor, introduce el número de AS de BGP: ")
        as_numero = int(as_input)
        resultado = validar_as_bgp(as_numero)
        print(resultado)
    except ValueError:
        print("Entrada inválida. Por favor, introduce solo números.")
    print("---------------------------")