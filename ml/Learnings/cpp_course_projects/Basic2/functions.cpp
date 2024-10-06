#include <iostream>


void greet(std::string user_name,int age) // void_ if the function returns nothing
{
    std::cout<<"Hey Clown. Lets paint the wall Brown!!! "<<std::endl;
    std::cout<<"Hey " << user_name << " You are a son of a holy girl and your age is " << age << ". " << std::endl;
}

int main()
{
    greet("George",35); //call the function. // the order of the positional arguments matter.
    return 0;
}