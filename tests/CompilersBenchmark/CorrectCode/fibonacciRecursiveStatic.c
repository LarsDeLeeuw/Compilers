
#include <stdio.h>

int f(int a) {
	if (a<2) {
		return a;
	}
	else {
		return f(a-1) + f(a-2);
	}
}

// Recursive fibonnaci
int main(){
	int n = 10;
    printf("Enter a number:");
	// scanf("%d",&n);
	int i = 1;
	while(i++ <= n){
		printf("fib(%d)  = %d;\n", i, f(i));
	}
	return 0;
}
