// when you make a serie of division, you need to 
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;
public class RepeatAddtionQuiz 
{
    public static final double RATE = 0.07;
    public static final double TUITION_THIS_YEAR = 10000;
    public static final double TUITION_DOUBLED = TUITION_THIS_YEAR * 2;
    public static void main(String[] args)
    {
        System.out.println("Enter a string: ");
        Scanner sc = new Scanner(System.in);
        String str = sc.nextLine();
        int left = 0;
        int right = str.length()-1;

        while (left <= right)
        {
            if (str.charAt(left) != str.charAt(right))
            {
                System.out.println(str + " is not a palindrome");
                return;
                
            }
            left++;
            right--;
        }
        System.out.println(str + " is a palindrome");
    }

}
