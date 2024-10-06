#include <iostream>
#include <cmath>

int square(int number) // this function returns a integer value
{
    return number*number;
}

double pow_(double number,double power) // this function returns a float value
{
    return std::pow(number,power);

}
int main(){
    std::cout<< " 4^2 " << square(4) << ". " << std::endl;
    std::cout<< " 4^3 = " << pow_(4.0,3.0) << "." << std::endl;
    return 0;

}
