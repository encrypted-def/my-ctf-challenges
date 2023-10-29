#include <iostream>
#include <fstream>
#include <string>
using namespace std;

unsigned long long a;

string readflag(){
  ifstream readfile;
  readfile.open("flag.txt");
  string flag;
  getline(readfile, flag);
  readfile.close();
  return flag;
}

bool sanity_check1(){
  cout << 42 / a << '\n'; // avoid a = 0
  return true;
}

double type_conversion(unsigned long long a){
  return *(double *)&a;
}

bool sanity_check2(){
  return a == type_conversion(a);
}

int main(){
  string flag = readflag();
  cin >> a;  
  if(!sanity_check1())
    return -1;
  if(!sanity_check2())
    return -1;
  cout << flag << '\n';
}