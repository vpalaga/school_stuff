#include <iostream>
#include <string>
#include <cmath>
using namespace std;

int recursions = 0;

string con(int l){
    string ret;

    for (int i; i<l; i++){
        ret += "=";
    }
    return ret;
}


int fib(int a){
    recursions++;

    if (a <= 1){
        return a;
    }

    return fib(a - 1) + fib(a - 2);
}

int countRecurcions(int fibVal){
    recursions = 0; // reset the global var

    fib(fibVal); // run the fibbonati

    return recursions;
}

int main() {
    for (int i; i<=40; i++){
        int resInitial = countRecurcions(i);
        int res = log2(resInitial);
        cout << resInitial << con(res) << "\n";
    }
}
