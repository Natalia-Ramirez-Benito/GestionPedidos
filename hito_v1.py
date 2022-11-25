import phonenumbers
from password_validator import PasswordValidator
from phonenumbers.phonenumberutil import region_code_for_number
import re
import csv

print('Bienvenido')


def phonenumber():
    contador = True
    while contador == True:
        number = input('Introduce número de teléfono (+** *********): ')
        try:
            phoneNumber = phonenumbers.parse(number)
            prefixSpain = region_code_for_number(phoneNumber) == 'ES'
            # print(region)
            contador = False
        except phonenumbers.NumberParseException:
            print('Has introducido un número inválido vuelva a intentarlo.')
            contador = True
        except UnboundLocalError:
            print('Has introducido un número inválido vuelva a intentarlo.')
            contador = True
    return number


def email():
    global emailVerify
    contador = -1
    while contador == -1:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        emailVerify = input('Introduce un email: ')
        if re.fullmatch(regex, emailVerify):
            # print("Valid email")
            contador = 0
        else:
            print("Invalid email")
    return emailVerify


def password():
    isValid = False
    password = 0
    while not isValid:
        password = input('introduce la contraseña: ')
        repeatPassword = False

        schema = PasswordValidator()

        # Añadir requisitos a la contraseña
        schema \
            .min(8) \
            .max(20) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits() \
            .has().symbols() \
            .has().no().spaces() \
            # comprueba que la contraseña sea válida
        isValid = schema.validate(password)
        if not isValid:
            print('La contraseña no es valida, debe tener mayúsculas, minúsculas, números, no debe contener '
                  'espacios y la longitud debe estar comprendida entre 8 y 20 carácteres')
        else:
            repeatPassword = input('Vuelve a introducir la contraseña: ')

        if repeatPassword != password:
            print('Las contraseñas no son iguales')
            isValid = False
    return password


def initialScreen():
    launcher = ''
    while launcher != 'si' and launcher != 'no':
        launcher = input('¿Estás registrado?: (si/no) ')
        if launcher == 'no':  # crear cuenta
            input('Introduce tu nombre y apellidos: ')
            print('\n Aviso: Si usted no ha introducido bien su domicilio al crear la cuenta, '
                  'no le llegarán los pedidos y la empresa no se hará responsable.')
            input('Introduce el domicilio: ')
            phonecsv = phonenumber()
            emailcsv = email()
            passwordcsv = password()
            with open('users.csv', mode='a', newline='', encoding="utf-8") as csv_file:

                fieldnames = ['email', 'password', 'prefixSpain']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({'email': emailcsv, 'password': passwordcsv, 'prefixSpain': phonecsv})

        elif launcher == 'si':  # inicio sesión
            cont = False
            while not cont:
                data = []
                with open('users.csv') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        data.append(row)
                # print(data)
                emailcheck = None
                passwordcheck = None
                global prefixSpaincheck
                prefixSpaincheck = None
                email_login = input('Introduce el correo electrónico: ')
                col = [x[0] for x in data]
                if email_login in col:
                    for i in range(0, len(data)):
                        if email_login == data[i][0]:
                            emailcheck = (data[i][0])
                            passwordcheck = (data[i][1])
                            prefixSpaincheck = (data[i][2])

                if email_login == emailcheck:
                    password_login = input('Introduce la contraseña: ')
                    if password_login == passwordcheck:
                        cont = True
                        print('Sesión iniciada.')
                    else:
                        print('Contraseña incorrecta. Vuelva a introducirla.')
                else:
                    cont = False
                    print('La cuenta no existe o has introducido algún dato mal. Vuelva a intentarlo.')
                    continue
                global phoneNumber
                global number
                global prefixSpain
                phoneNumber = phonenumbers.parse(prefixSpaincheck)
                prefixSpain = region_code_for_number(phoneNumber) == 'ES'

        else:
            print('Has introducido algún dato mal. Vuelva a intentarlo.')


initialScreen()


class Products:
    def __init__(self, idp, details, price):
        self.idp = idp
        self.details = details
        self.price = price

    def getPrice(self):
        return self.price * 1.21 if prefixSpain else self.price * 1.92


product1 = Products(1, 'Gato naranja', 80)
product2 = Products(2, 'Gato marrón', 40)
product3 = Products(3, 'Gato negro', 40)
product4 = Products(4, 'Gato blanco', 40)
product5 = Products(5, 'Comida para gato standard', 2.50)
product6 = Products(6, 'Comida para gato premium', 17.50)

products_dict = {
    str(product1.idp): product1,
    str(product2.idp): product2,
    str(product3.idp): product3,
    str(product4.idp): product4,
    str(product5.idp): product5,
    str(product6.idp): product6
}


def itemScreen():
    prod = 0
    userFav = []
    print('\n Aviso: Los productos selecionados como favoritos se añadirán automáticamente al carrito.')

    while prod != -1:
        if prod != 0:
            userFav.append(prod)
        for i in products_dict:
            if products_dict[i].idp in userFav:
                print(products_dict[i].idp, ':', products_dict[i].details, '*')
            else:
                print(products_dict[i].idp, ':', products_dict[i].details)

        prod = int(input('Elige el producto que quieras añadir a favoritos, si quieres parar pon -1: '))
        # sacar el precio de los productos seleccionados
    total = 0
    for i in userFav:
        total = total + products_dict[str(i)].getPrice()

    print(f'El precio total sería (iva incl.): {total}€')


itemScreen()


def payMethods():
    print('Seleccione método de pago: ')
    print('1. En efectivo.')
    print('2. Con tarjeta de crédito/débito.')
    print('3. Por transferencia bancaria')
    print('4. Con Paypal.')
    print('5. Con Bizum')
    choose = 0
    while 1 >= choose <= 5:
        try:
            choose = int(input('Para elegir, introduzca el número de la opción que prefiera (1-5) sin punto: '))
        except:
            print('No has introducido un valor válido. Vuelva a intentarlo.')
            continue
        if choose == 1:
            print('El cobro se realizará en la entrega del producto.')
            break
        if choose == 2:
            print('Redirigiendo a Redsys . . .')
            break
        if choose == 3:
            print('Deberá hacer una transferencia bancaria en un plazo de 7 días a la cuenta: 0049 1500 05 1234567892')
            break
        if choose == 4:
            print('Redirigiendo a Paypal . . .')
            break
        if choose == 5:
            print('Redirigiendo a Bizum . . .')
            break

    print('\n Pago finalizado. Se le enviará tanto al correo como al teléfono, por sms, el número de seguimiento '
          'además de la factura en pdf por correo.')
    print('\n Se le entregará el pedido en un plazo de 11 días laborables.')
    print('\n Si usted no ha introducido bien su domicilio al crear la cuenta, no le llegarán los pedidos y la empresa'
          'no se hará responsable.')
    print('\n Esperamos verle pronto. Un gato chocó. ¿Qué dijo? -"miaauuto!!"')


payMethods()
