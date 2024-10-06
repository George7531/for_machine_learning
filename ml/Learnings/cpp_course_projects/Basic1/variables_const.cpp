#include<iostream>

int main()
{
    const double max_sys_temp = 76.5;
    const double min_water_level = 88.0;

    std::cout << "Max allowed temperature for the system to reach is: " << max_sys_temp << std::endl;
    std::cout << "Minimum water level to be maintained in the water tank to maintain the system's temperature is: " << min_water_level << std::endl;

    return 0;
}