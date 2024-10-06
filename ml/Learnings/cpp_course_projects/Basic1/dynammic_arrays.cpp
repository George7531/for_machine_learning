#include<iostream>
#include<vector>

int main()
{
    std::vector<double> temperatures = {4,28,32.5,43};
    std::cout << temperatures.at(0) << std::endl; // this is akin to indexation
    std::cout << temperatures.size() << std::endl; // len() in python
    temperatures.push_back(22.5); // append in python

    // accessing all the elements of the vector 'temperatures'
    for(size_t i=0; i<temperatures.size(); ++i){
        std::cout << "Element at index " << i << " is: " << temperatures[i] << std::endl; 
    }


    return 0;
}