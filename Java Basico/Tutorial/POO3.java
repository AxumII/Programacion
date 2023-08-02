//Aca se explica polimorfismo, excepciones
/*
 * Hay dos tipos de Polimorfismo, estatico y dinamico
 * Estatico: Consiste en crear n metodos con mismo nombre, pero distintos tipos de datos en las entradads, asi se sobrecarga el metodo
 * java identifica cual es cual de acuerdo al tipo de dato en las entradas, pueden ser el mismo numero de entradas o distinto
 * 
 * Dinamico:
 */
public class POO3 {
    public static void main(String[] args){
        Clase1 Objeto1 = new Clase1();
        float Aux1 = Objeto1.Metodo1(69.69f, 5.77f);
        int Aux2 = Objeto1.Metodo1(77, 13);
        System.out.println(Aux1);
        System.out.println(Aux2);
        //Se sobrecargo el metodo, es polimorfismo estatico

        ///////////////////////////////////////
        Clase2 Objeto2 = new Clase2();
        Clase3 Objeto3 = new Clase3();
        Objeto2.Metodo2(10);
        Objeto2.Metodo3();
        Objeto3.Metodo3();
        Objeto3.Metodo4(); 
        


    }

}

class Clase1{
    public int Metodo1(int x, int y){
        x = x + y;
        return x;
    }
    public float Metodo1(float x, float y){
        x = x + y;
        return x;
    }
    //aca se ve como es el mismo metodo pero con diferentes entradas 
}
///////////////////////////////////////////////////////////
//Clase padre
class Clase2{
    protected int Var1;
    public int Metodo2(int Var1){
        this.Var1 = Var1;
        return Var1;
    }
    void Metodo3(){
        System.out.println("Metodo 3 de la clase 2");
    }
}
//Clase Hija 1
class Clase3 extends Clase2{

    public void Metodo3(){
        System.out.println(this.Var1);
        System.out.println("Metodo 3 de la clase 3");
    }

    public void Metodo4(){
        super.Metodo3();
        System.out.println("Metodo4 de la clase 3, antes se llamo al metodo3 de la clase2, osea, la padre");
    }

}
