//aca se va a explicar herencia y encapsulamiento
//se retomara el texto de POO1 de modificadores
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
//ENCAPSULAMIENTO
/*
 * Consiste en bloquear acceso a atributos de clases a otras clases externas
 * para acceder se usan metodos get y set
 * y en general para referenciar un elemento se usa this.elemento
 * p ej int private x
 * en los metodos se usa this.x para usar a x
 */
//HERENCIA
//NO HAY HERENCIA MULTPLE, solo se hereda de un padre
//Se heredan todos los metodos accesibles
public class POO2 {
    public static void main(String[] args){
        Clase1 O1 = new Clase1();
        Clase2 O2 = new Clase2();

        System.out.println(O1.Var1);
        //O1.Var2 = 5;
        //System.out.println(O1.Var2);
        //Al ser privada no se peude acceder DESDE FUERA
        //PAra acceder toca crear el metodo get y set
        int x = O1.getVar2();
        System.out.println(x);
        //accede al valor de Var1 y lo imprime, se puede poner x o directamente el getvar ya que es una variable

        O1.setVar2(169);
        //modifica el valor de Var2
        System.out.println(O1.getVar2());

        System.out.println(O1.getVar3());

        //////////////////////////////////////////////////////////7
        //Para herencia
        //los hijos no heredan las varaibles privadas, pero si heredan las protected
        //System.out.println(O2.Var2);
        System.out.println(O2.Var1);
        System.out.println(O2.Var3);
        int Aux = O2.Metodo3(15);
        System.out.println(Aux);
    
    }
    
}

class Clase1{
    int Var1;
    private int Var2;
    protected int Var3;
    //en este caso se definieron dos atributos, Var1 y Var2, el primero es publico y puede ser accesado sin ninguna restriccion desde cualquier metodo y clase no interna
    //el segundo es private, por lo que llamarlo desde otra clase o metodo, incluso creando un objeto no va a ser posible a menos que se usen accesores
    //se usan unos metodos especiales para obtener un atributo privado
    public Clase1(){
        Var1 = 11;
        this.Var2 = 69;
        this.Var3 = 73;
    }
    //voy a usar un generico aunque podria no usarlo
    public <T> int Metodo1(int x,T y){
        System.out.println(x);
        //No hay problema en mandar un print ya que no distingue el tipo de dato, tambien permite funciones con genericos
        //no es posible operar con genericos, por lo que es necesario definir la entrada
        x = x++;
        System.out.println("Se ejecuta el metodo1 de la clase1");
        return x ;
    }
    
    public int Metodo2(int a){
        //Es necesario especificar el tipo de dato de salida del metodo definiendo el metodo
        //Como se ve, no hay lio en acceder a la variable privada
        System.out.println("Se ejecuta el metodo2 de la clase");
        return a + this.Var2;
    }

    public int getVar2(){
        return Var2;
        //el getter es un metodo que se define con el mismo tipo de dato de la variable
    //Permite tener una lectura del valor desde el objeto
    //basicamente invoca a la variable y la retorna al objeto
    //la estrucutura es la misma, GetNombredevariable()
    }
    public void setVar2(int Var2){
        this.Var2 = Var2;
        //Eso es un setter, lo que permite es modificar el valor de la variable al invocarse
    //llama al valor con un this y luego lo sustituye por el colocado en la funcion (int Var1 en este caso)
    }

        //aca se creo unos getters y setters para Var3 que es protected
    public int getVar3(){
        return Var3;
    }
    public void setVar3(int Var3){
        this.Var3 = Var3;
    }

}

//la clase2 heredara los metodos de la clase1, por lo que los podra usar normalmente
//No se heredan los private, solo public y protected
class Clase2 extends Clase1{
    int Var4;
    private int Var5;

    public int Metodo3(int c){
        System.out.println("Metodo Clase2");
        int y = Var1 + this.Var3 + getVar2();
        System.out.println("Se ejecuta el metodo propio del hijo con atributos de padre e hijo");
        System.out.println(y);
        return y;
    }

}

