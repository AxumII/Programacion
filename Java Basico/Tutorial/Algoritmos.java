

import java.util.Scanner;



public class Algoritmos {

    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);

        EstructurasRepetitivas factorial = new EstructurasRepetitivas();

        int x;
        x = sc.nextInt();
        long startTime = System.nanoTime();

        System.out.println("Metodo recursivo");
        System.out.println(factorial.Recursion(x));

        long endTime = System.nanoTime() - startTime;
        System.out.print("Tiempo que demora en ejecutar");
        System.out.println(endTime);


        startTime = System.nanoTime();
        System.out.println("Metodo iterativo");
        System.out.println(factorial.Iteracion(x,1));
        endTime = System.nanoTime() - startTime;
        System.out.print("Tiempo que demora en ejecutar");
        System.out.println(endTime);
    }
}



class EstructurasRepetitivas{

    public int Recursion(int numero){
        
        if(numero <= 1){
            return 1;
        }
        else{
            int resultado = Recursion(numero - 1)*numero;
            
            return resultado;
        }
    }

    public int Iteracion(int numero,int d){
        int producto = 1;
        int aux;
        
        for(int x = 0; x < numero; x++){
            System.out.print("iteracion ");
            System.out.print("n = ");
            System.out.println(x);
            System.out.print("p = ");
            System.out.println(producto);

            aux = producto;
            producto = producto*(x+1);
            
            
            System.out.println("p(n+1) = ");
            System.out.print(aux);
            System.out.print("(");
            System.out.print(x);
            System.out.print("+1) = ");
            System.out.println(producto);
        }

        return producto;
    }
}


