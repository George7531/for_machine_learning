#include<iostream>
#include<numeric>
#include<vector>

int main(){
    /*
    Ask from the user his Name and Age and print it out!!!
    */
    std::string user_name;
    int age;
    
    std::cout<<"Enter your Name: ";
    std::cin>>user_name;
    std::cout<<"Enter your Age: ";
    std::cin>>age;

    std::cout<<"Your Name is "<<user_name<<", and your Age is "<< age << "." << std::endl;

    /*
    Ask from the user 2 int numbers, add them and print it out!!!
    */

    int a,b;
    std::cout<<"Enter values for a & b: ";
    std::cin>>a>>b;
    std::cout<<"The sum of a and b is: "<<a+b<<"."<<std::endl;
    
    /*
    create a vector of 4 float numbers, compute the average and 
    print it.
    */
   double vector[] = {2.5,3.8,22.8,-2.8};
   double average;
   double sum = 0.0;
   int size = sizeof(vector)/sizeof(vector[0]); // sizeof(vector) gives total bytes. dividing this by bytes of a single element would give us the actual size of the array.
   sum = std::accumulate(std::begin(vector),std::end(vector),sum);
   average = sum/size;
   std::cout<<"The average of all elements in the vector is: "<<average<<"."<<std::endl;


   /*
    finding average for the second time but this time 
    with a newer technique
    */
   std::vector<double> list = {2.5,3.8,22.8,-2.8}; // first include the vector library on top of the program.
   double average;
   size_t size = list.size(); 
   double sum = accumulate(list.begin(),list.end(),0.0);
   average = sum/size;
   std::cout<<"The average of all elements in the vector is: "<<average<<"."<<std::endl;




   return 0;
}