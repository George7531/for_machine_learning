#include<iostream>

int main()
{
    double temperature_list[4] = {36.5,22.3,38,1.5};
    std::cout << "Before modification: " << temperature_list[1] << std::endl;
    temperature_list[1] = 18;
    std::cout << "After Modification: " << temperature_list[1] << std::endl;
    return 0;
}