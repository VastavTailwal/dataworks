#include<iostream>


int main()
{
	unsigned short int roll_num;
	char name[32];
	std::cout << "Hello World" << std::endl;
	std::cout << "Enter name :";
	std::cin.getline(name);
	std::cout << "Enter roll number :" << std::endl;
	std::cin >> roll_num;
	std::cout << name << "your roll number is " << roll_num;
	return 0;
}
