#include<iostream>    // attached a header file


int main()
{
	
	/* initialized variables */
	
	unsigned short int roll_num = 0;
	char name[32] = 'xxxxxx';
	
	/* taking user input */
	
	std::cout << "Hello World" << std::endl;
	std::cout << "Enter name :";
	std::cin.getline(name);
	std::cout << "Enter roll number :" << std::endl;
	std::cin >> roll_num;
	
	/* printing user input on standart output (console window) */
	
	std::cout << name << "your roll number is " << roll_num;
	return 0;
}
