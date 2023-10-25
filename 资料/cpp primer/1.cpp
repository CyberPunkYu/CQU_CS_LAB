#include <iostream>
#include <string>
using namespace std;
int main(){
		int n;
		cin >> n;
        if (n<5)
            cout<<0<<endl;
        else{
            int sum = 1;
            int m;
            string str;
            for(int i = 1 ; i <= n ; i++)
                sum *= i;
            str = to_string(sum);
            m = str.length();
            int count = 0;
            if (str[m-1]=='0')
                count = 1;
            cout << count <<endl;
    	}
    	return 0;
}