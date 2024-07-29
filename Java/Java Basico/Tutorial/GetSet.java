public class GetSet {
    private int Var1;
    //Declaro una variable privada, al ser privada, el objeto no tiene acceso a ella


    public GetSet(){
        //int Var1 = 7;
    }
    //NO es necesario el constructor ya que ya se inicializo la variable como private, por lo que no va a tomar el valor de 7

    public int getVar1(){
        return Var1;
    }
    //el getter es un metodo que se define con el mismo tipo de dato de la variable
    //Permite tener una lectura del valor desde el objeto
    //basicamente invoca a la variable y la retorna al objeto
    //la estrucutura es la misma, GetNombredevariable()

    public void setVar1(int Var1){
        this.Var1 = Var1;
    }
    //Eso es un setter, lo que permite es modificar el valor de la variable al invocarse
    //llama al valor con un this y luego lo sustituye por el colocado en la funcion (int Var1 en este caso)

    public void print(){
        System.out.println(Var1);
    }

    public static void main(String[] args){

        GetSet Objeto1 = new GetSet();
        //cree un objeto que hereda los metodos
        //System.out.println(GetSet.Var1);
        //Al ser privada no se puede acceder a: System.out.println(Var1);

        int x = Objeto1.getVar1();
        System.out.println(x);
        //accede al valor de Var1 y lo imprime, se puede poner x o directamente el getvar

        Objeto1.setVar1(69);
        System.out.println(Objeto1.getVar1());

        


        

        


    }
}
