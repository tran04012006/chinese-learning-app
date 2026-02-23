import java.io.*;
import java.util.*;

public class Main 
{
    public static void main(String[] args) 
    {
        Scanner sc = new Scanner(System.in);

        int x = sc.nextInt();
        int y = sc.nextInt();
        String c = sc.nextLine();
        float f = sc.nextFloat();
        double d = sc.nextDouble();

        // in dữ liệu
        System.out.println(x);
        System.out.println(y);
        System.out.println(c);

        System.out.printf("%.2f" , f);
        System.out.println();
        System.out.printf("%.9f" , d);
    }
}