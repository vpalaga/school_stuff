#include <iostream>
#include <string>
using namespace std;

class Car{
public:
  string model;
  int prise;
  int year;

  Car(string modelCon, int priseCon, int yearCon){
    model = modelCon;
    prise = priseCon;
    year = yearCon;
  }

  void ret(){
    cout << model << " " << prise << " " << year << endl;
  }

};

int main(){
  Car car1("BMW", 49000, 1999);
  Car car2("Ford", 19000, 2001);

  car1.ret();
  car2.ret();

  return 0;
}
