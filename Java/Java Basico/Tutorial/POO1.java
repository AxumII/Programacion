public class POO1{//recordar que siempre debe coincidir el nombre de larchivo con el objeto main
    //Todos los programas en java tienen una clase principal
    //Toda clase en java puede contener mas clases
    //En general solo se crea la clase y  en otro java se crea el ejecutable

    //RECORDAR QUE ACA SOLO SE HEREDA 1 CLASE Y PARA USAR LOS METODOS SE LLAMA A UN OBJETO

//MODIFICADORES 
    /* Estos son caracteristicas de metodos y clases que dan o quitan acceso y mas propiedades
     * TODOS VAN EN MINUSCULA
     * 
     * ACCESO
     * PARA CLASES:
     * Public: Permite acceder desde cualquier otra clase
     * Default: osea, no lleva nada, esto sol oaccede desde el mismo package, osea la principal
     * 
     * PARA METODOS
     * Public: Accesible desde cualquier clase
     * Private: Accesible solo desde la clase que la crea a menos que use getters y setters
     * Protected: Accesible solo desde la clase y subclases
     * 
     * NO ACCESO
     * PARA CLASES:
     * Final: No hereda
     * Interface: Es una clase que solo tiene metodos abstractos y publicos
     * Abstract: Es una clase que puede tener metodos abstractos y definidos
     * https://www.w3schools.com/java/java_modifiers.asp
     * 
     * PARA METODOS
     * Final: Metodos inmodificables
     * Static: Se puede llamar sin crear un objeto, el public toca crear el objeto
     * los static al heredarse no permiten sobreescritura ni ser sobrecargados
     * Abstract: Metodo que debe ser vacio, solo tiene el nombre y las propiedades propias del metodo(modificadores)
     * Void: Estos son metodos que no permiten return, solo ejecutan funciones
     * Genericos: Estos permiten entrada y salida de datos, con return y tambien funcionan como voids
     * tambien hay clases genericas que son las que permiten que el objeto como tal tenga valores y el metodo funcione como una funcion
     * Void: Estos son metodos que no permiten return, solo ejecutan funciones
     * Genericos: Estos permiten entrada y salida de datos, con return y tambien funcionan como voids
     * tambien hay clases genericas que son las que permiten que el objeto como tal tenga valores y el metodo funcione como una funcion con cualquier entrada
     * Las no genericas tambien retornan pero solo ese tipo de dat oespecifico
    */

    
    public static void ExternoV(){
        System.out.println("Este es el metodo void de la clase externa");
    }
    

    public <T> String ExternoG(T x){
        System.out.println("Este es el metodo generico de la clase externa");
        String a = "cambio";
        return a;
    }
    //Metodos genericos
    /*
     * Tienen la ventaja que no es necesario definir el tipo de dato en las entradas, SOLO DEFINIR EN SALIDAS
     * En metodos no genericos es necesario definir la entrada
     * un metodo generico debe tener la estructura
     * 
     * EN EL METODO
     * Modificadores <TipoVargenericaentrada> TipoVarSalida Metodo(TipoVargenericaentrada Varentrada){
     * CODIGO
     * return VarSalida 
     * }
     * 
     * EL RETURN NO REQUIERE EL TIPO DE DATO, NO CONFUNDIR CON OTRAS COSAS
     * 
     * EN EL EXE
     * 
     * TipoSalida VarSalidaexe = Metodo(dato de entrada sin especificar);
     * 
     */


    public class ClaseInterna{
        //Esta es una clase interna, cualquier clase interna hereda los metodos de la externa

        public ClaseInterna(){
            //Esto es un csntructor, lo ideal es definir los atributos aca, para tener una globalidad local
            //Es posible sobrecargar cosntructores, puedo tener otro igual y definir otros atributos que igual funciona
            //int Var1 = 77;
        }


        public void Metodo(){
            System.out.println("este es el 1 metodo");
            ExternoV();
        }
        //Ahi se define el primer metodo, nada raro, tambien llama al metodo ExternoV

    }


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Para ejecutar programas se necesita del main, aunque claro, tambien se puede exportar y ejecutar en otro lado
public static void main(String[] args){
    //Aca se van a crear los objetos ya que es el ejecutable
    POO1 Objeto = new POO1();
    //Este es un ojbeto, se creo en base a la clase Externa, al ser generica toca definir el tipo de dato a usar(no con primitivas si no con las clases de las primitivas)
    //En este caso no se usa ls clase  como generico, aunque podria usarse
    ExternoV(); //Es estatico, no necesita el objeto para ser llamado
    String Var2 = Objeto.ExternoG(5); //No es estatico, es generico asi que solo le interesa la salida que coincida
    System.out.println(Var2);


    POO1.ClaseInterna Objeto2 = Objeto.new ClaseInterna();
        System.out.println(Objeto2); // Con un metodo tostring imprimiria todo el objeto pero requiere muchcas cosas
        Objeto2.Metodo();
        //String Var3 = Objeto2.ExternoG(10);
        //System.out.println(Var3);

        

    }
   


    
}
