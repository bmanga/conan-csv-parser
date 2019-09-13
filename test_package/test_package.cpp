#include <iostream>
#include "csv.hpp"

int main()
{
	csv::CSVField field("Bincrafters");
    std::cout << field.get<>() << "\n";
    return 0;
}
