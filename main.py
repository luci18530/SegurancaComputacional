from Salt_Hash import *

def main():
    while True:
        print("\nEscolha uma opção:")
        print("1. Testar hash de senha sem salt")
        print("2. Testar hash de senha com dois salts diferentes")
        print("3. Sair")

        choice = input("Digite sua escolha (1/2/3): ")

        if choice == '1':
            input_string = input("Digite a senha que você deseja hash: ")
            hashed_string = hashing_input(input_string)
            print(f"Senha original: {input_string}")
            print(f"Hash: {hashed_string}")

        elif choice == '2':
            input_string = input("Digite a senha que você deseja hash: ")
            salt1 = generate_salt()
            salt2 = generate_salt()
            hashed_string_with_salt1 = hashing_input_with_salt(input_string, salt1)
            hashed_string_with_salt2 = hashing_input_with_salt(input_string, salt2)
            print(f"Senha original: {input_string}")
            print(f"Salt 1: {salt1}")
            print(f"Hash com Salt 1: {hashed_string_with_salt1}")
            print(f"Salt 2: {salt2}")
            print(f"Hash com Salt 2: {hashed_string_with_salt2}")

        elif choice == '3':
            print("Saindo...")
            break

        else:
            print("Escolha inválida. Tente novamente.")

if __name__ == "__main__":
    main()