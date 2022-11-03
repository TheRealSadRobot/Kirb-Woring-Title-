/*
Filename: Cupcakery.java
Author(s): Christopher Haldeman, Kathryn McMillan, Taliesin Reese
Version: 1.2, last updated by T
Date: 10/29/2022
Purpose: Back when I was making the lemonade program, I was able to put a really funny lemon quote up here. I can't think of any funny cupcake quotes, though. What a shame.
*/
import java.lang.Math;

 // import scanner library for input

 import java.util.Scanner;

    
 

 public class Cupcakery{

    static double cupcakesCount = 0;
    //add bulk pricing later
    double cupcakesPrice = 2.0;
    double orderTotal = 0.0;

    public static void main(String[] args){
        // Declare scanner object and initialize with
        // predefined standard input object system in
        Scanner keyboard = new Scanner(System.in);
        double coupcakesCount;
        double cupcakesPrice = 2;
        

        // Start the while loop
        while (true) {
            // Create the menu
            System.out.println(" **                  ** ");
            System.out.println("*  *                *  *");
            System.out.println("|__| Cupcakery Menu |__|");
            System.out.println("PRICE: $2.00 per Cupcake");
            System.out.println("1: Order Quantity");
            System.out.println("6: Make Purchase");
            System.out.println("9: Exit Program");
            System.out.println("Enter your choice: ");
            // Listen for user input
            double choice = keyboard.nextDouble();

            // if statements to call the different menu options
            if (choice == 1) {
                cupcakesCount = get_quantity(keyboard);
                continue;
            }
            else if (choice == 6) {
                display_purchase(cupcakesCount, cupcakesPrice);
                continue;
            }   
            else if (choice == 9) {
                keyboard.close();
                break;
            }
            // If someone enters a choice that isn't on the menu ask them
            // To enter one of the menu choices and restart the loop.
            else{
                System.out.println("Please enter one of the choices below");
                continue;
            }
        }
    }

    static double get_quantity(Scanner keyboard){
        System.out.print("Enter the number of cupcakes you'd like to order: ");
        double choice = keyboard.nextDouble();
        double cupcakesCount = choice;
        return cupcakesCount;
        

    }

    static void display_purchase(double cupcakesCount, double cupcakesPrice){

        double orderTotal = cupcakesCount * cupcakesPrice;
        System.out.println("You have currently ordered " + cupcakesCount + " cupcakes!");
        System.out.println("The cost of your current order is: " + orderTotal );

    }
 }