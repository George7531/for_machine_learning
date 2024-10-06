#include <iostream>

int main(){
    std::string user_name;
    int age;
    std::cout << "Enter your name: " << std::endl;
    std::cin  >> user_name;
    std::cout << "Enter your age: " << std::endl;
    std::cin >> age;
    
    if (age<18){
        std::cout << "Sorry " << user_name << ". You are not allowed to enter this Website!!!" << std::endl;
    }else{
        std:: cout << "Greetings " << user_name << "! Welcome to our Website. Have a blast..." << std::endl;
    }

    return 0;
}