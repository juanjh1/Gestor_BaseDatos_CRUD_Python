import psycopg2
import os 

DROP_USERS_TABLE = "DROP TABLE IF EXISTS users"
USERS_TABLE = """  CREATE TABLE users (
   id  SERIAL,
   username VARCHAR(50) NOT NULL,
   email VARCHAR(50) NOT NULL,
   create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
)
""" #--> crea una query

def sistem_clear(funcion):
   def wrapper (*args, **kargs):
      os.system('cls')

      funcion(*args, **kargs)

      input('')

      os.system('cls')
   wrapper.__doc__ = funcion.__doc__
   return wrapper


def user_exist(funcition):

   def wrapper(*args,**kargs):


      id = input('[o] Ingresa id del usuario  : ')
      query = "SELECT * FROM users WHERE id = %s"
      if id in ['abcdefgh1jklmnopqrstwxyz']:
         print('solo valores numericos')
         
      
      cursor.execute(query,(id,))
      user = cursor.fetchone()
      if user:
         funcition(id,cursor, connect)
      else:
         print('No existe usuario con este id')
   wrapper.__doc__ = funcition.__doc__
   return wrapper 

      



@sistem_clear
def create_user(cursor, connect):
   """"A) Crear usuario"""

   username = input('[o] ingresa tu username: ')
   email = input('[o] ingresa tu email: ')

   query = "INSERT INTO users (username, email) VALUES (%s, %s)"
   values = (username, email)
   cursor.execute(query,values)
   connect.commit()
   print('>>>> usuario creado exitosamente!  \n\n')
   pass


@sistem_clear
@user_exist
def delete_user(id,cursor, connect):
   
   """"B) Eliminar usuario"""
  
   #print('[-] el valor ingresado debe ser numerico')
      
   
   
   query = "DELETE FROM users where id=%s"
   
   cursor.execute(query,(id,))
   
   connect.commit()
   print(' >>> usuario eliminado  con exito \n\n')
   
   pass



@sistem_clear
@user_exist
def update_user(id,cursor, connect):
   """"C) Actualizar usuario"""
   
   campo = input('[o] ingresa el campo de cambio : ')

   nuevo_valor = input('[o] ingresa tu nuevo valor : ')
   
   if campo in ['username', 'email']:
      query = f"UPDATE users SET {campo} = '{nuevo_valor}' WHERE id = {id}"
      cursor.execute(query)
      connect.commit()
      print('>>> usuario actualizado con exito \n\n')

   else:
      print('[-]. el campo ingresado no es correcto')

  
   pass



@sistem_clear
def list_user(cursor, connect):
   """"D) listar usuarios"""

   print('>>> lista de usuarios \n')

   query = "SELECT id,username, email FROM users"
   cursor.execute(query)
   for user in cursor.fetchall():
      print('-->', user)
   connect.commit()
   
   
   pass

@sistem_clear
def default(*args):
   print('[-] La opcion no es valida')


if __name__ == '__main__':
   options= {
      'a':create_user,
      'b':delete_user,
      'c':update_user,
      'd':list_user
   }
   try:
      connect = psycopg2.connect("postgresql://postgres:123456789@localhost/project_pythondb") # Crea conexion 


      with connect.cursor() as cursor: # --> Crea un cursor 
         #cursor.execute(DROP_USERS_TABLE)  --> Ejecuta una  query
         #cursor.execute(USERS_TABLE) 
         connect.commit()  # ---> envia los cambios 
        

         while True:
            for function in options.values():
               print(function.__doc__)
      
            print('[o] quit para salir')
            option = input('[+] Seleccione una opccion valida: ').lower()

            if option == 'quit' or  option == 'q':
               break
            function = options.get(option,default)
            function(cursor, connect)
   except psycopg2.OperationalError as err:
      print ( '[-] No fue posible realizar la conexion')
      connect.close