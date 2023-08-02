import java.util.Scanner;




public class Basico {  //es la clase madre, debe coincidir el nombre del archivo con el de esta clase y debe guardarse con .java , no ser pendejo otra vez
// todo debe ir en un mugre objeto, asi sea un objeto sin instancia, solo pa meter codigo
    public static void main(String[] args){
        System.out.println("asdasdsadsasa"); //el metodo que imprime 

        //Estructuras de datos primitivas
        int Numero = 4;
        //float Numero2 = 5.66f; //debe tener ese sufijo XD, da pereza pero toca
        //char Letra = 'd'; //esta mmda toca con comillas simples
        //boolean DatoOnt = true; //van en minuscula
        //String Texto = "hola"; //con comillas y mayuscula

        System.out.println(Numero);//esta mmda solo imprime una cosa a la vez

        //Classes tambien es primitivo
        //Interface tambien es primitiva, se explica luego
        
        //No siempre es necesari odefinir un tipo de dato al inicio, al operar si, pero al inicio no, se usan genericos

        

        //Matematica basica
        //los operadores basicos mismo que en c++ 
        //aca se usan las librerias aunque no se les llama asi, siguen siendo objetos puros
        //aca para matematicas se usa math
        Math.abs(-4); //saca valor absoluto
        Math.random(); //sin parametros es entre 0  y 1, se supone que es una dsitribucion uniforme, osea, un espacio laplaciano 


        //condicionales iguales que en los demas lenguajes, solo que con {}, tanto for como if y while
        //tambien hay break y continue


        //////////////////////////////////////////////////////////////////////////////////////////////////////////////

        //para importar archivos se usa import java.apirequerida, .* importa todos los metodos

        //////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //ENtrada y salida de datos seria

        //salida es system.out, ya hay ejemplos
        //entrada es
        int Varentrada = 0;
        Scanner sc  = new Scanner(System.in);
        Varentrada = sc.nextInt();
        //para cada tipo de dato hay un next, donde en todos coincide excepto en string que es nextLine

        System.out.println("saca el varentrada");
        System.out.println(Varentrada);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
        //arreglos
        //aca tambien son arrays y son estaticos
        //son solo de un mismo tipo de dato
        int arreglo[] = new int[50]; //efectivamente esta mmda solo recibe enteros
        arreglo[0] = 5;
        arreglo[4] = 10;
        
        System.out.println(arreglo[4]); //no permite imprimir toda la matriz, toca usar un for xd, que pereza, con razon python es popular xd

        //aca no es neceasrio poner n arreglos en un arreglo para hacer una matriz, ya hay un primitivo con eso

        int matriz[][] = new int[4][5];
        matriz[2][2] = 77;

        System.out.println(matriz[2][2]);





    }

}
    
    